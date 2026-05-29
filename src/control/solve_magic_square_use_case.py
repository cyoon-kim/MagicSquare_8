"""SolveMagicSquareUseCase — FR-06 orchestration."""

from __future__ import annotations

from boundary.boundary_validator import BoundaryValidator
from boundary.models import ErrorResponse
from boundary.result_formatter import ResultFormatter
from entity.blank_finder import BlankFinder
from entity.magic_square_validator import MagicSquareValidator
from entity.missing_number_finder import MissingNumberFinder
from entity.solver import Solver


class SolveMagicSquareUseCase:
    """Boundary → Domain chain → ResultFormatter."""

    def __init__(
        self,
        boundary_validator: BoundaryValidator,
        blank_finder: BlankFinder,
        missing_number_finder: MissingNumberFinder,
        magic_square_validator: MagicSquareValidator,
        solver: Solver,
        result_formatter: ResultFormatter,
    ) -> None:
        self._boundary_validator = boundary_validator
        self._blank_finder = blank_finder
        self._missing_number_finder = missing_number_finder
        self._magic_square_validator = magic_square_validator
        self._solver = solver
        self._result_formatter = result_formatter

    def execute(
        self, matrix: list[list[int]] | None
    ) -> list[int] | ErrorResponse:
        validation_error = self._boundary_validator.validate(matrix)
        if validation_error is not None:
            return validation_error

        assert matrix is not None
        self._blank_finder.find(matrix)
        self._missing_number_finder.find(matrix)
        solve_result = self._solver.solve_or_error(matrix)
        if isinstance(solve_result, ErrorResponse):
            return solve_result
        formatted = self._result_formatter.format(solve_result)
        return formatted
