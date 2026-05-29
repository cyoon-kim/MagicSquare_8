"""SolveMagicSquareUseCase — FR-06 orchestration."""

from __future__ import annotations

from contracts.errors import ErrorResponse
from control.ports import MatrixValidatorPort, ResultFormatterPort
from entity.solver import Solver


class SolveMagicSquareUseCase:
    """Boundary validation → Domain solver → ResultFormatter."""

    def __init__(
        self,
        boundary_validator: MatrixValidatorPort,
        solver: Solver,
        result_formatter: ResultFormatterPort,
    ) -> None:
        self._boundary_validator = boundary_validator
        self._solver = solver
        self._result_formatter = result_formatter

    def execute(
        self, matrix: list[list[int]] | None
    ) -> list[int] | ErrorResponse:
        validation_error = self._boundary_validator.validate(matrix)
        if validation_error is not None:
            return validation_error

        assert matrix is not None
        solve_result = self._solver.solve(matrix)
        if isinstance(solve_result, ErrorResponse):
            return solve_result
        formatted = self._result_formatter.format(solve_result)
        return formatted
