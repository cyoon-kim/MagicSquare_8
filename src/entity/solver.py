"""Solver — FR-05a two-cell magic square assignment."""

from __future__ import annotations

from copy import deepcopy

from contracts.errors import (
    DOMAIN_NO_MAGIC_ASSIGNMENT_CODE,
    DOMAIN_NO_MAGIC_ASSIGNMENT_MESSAGE,
    ErrorDetail,
    ErrorResponse,
)
from entity.blank_finder import BlankFinder
from entity.exceptions import UnsolvableDomainError
from entity.magic_square_validator import MagicSquareValidator
from entity.missing_number_finder import MissingNumberFinder


class Solver:
    """Tries two assignment orders for two blanks; returns int[6] 0-index."""

    def __init__(self) -> None:
        self._blank_finder = BlankFinder()
        self._missing_finder = MissingNumberFinder()
        self._validator = MagicSquareValidator()

    def solve(self, matrix: list[list[int]]) -> list[int] | ErrorResponse:
        blanks = self._blank_finder.find(matrix)
        if len(blanks) != 2:
            raise UnsolvableDomainError("Expected exactly two blanks")
        missing = self._missing_finder.find(matrix)
        if len(missing) != 2:
            raise UnsolvableDomainError("Expected exactly two missing numbers")
        attempts = [
            (missing[0], missing[1]),
            (missing[1], missing[0]),
        ]
        for first, second in attempts:
            payload = self._try_assignment(matrix, blanks, first, second)
            if payload is not None:
                return payload
        raise UnsolvableDomainError(DOMAIN_NO_MAGIC_ASSIGNMENT_MESSAGE)

    def solve_or_error(self, matrix: list[list[int]]) -> list[int] | ErrorResponse:
        try:
            return self.solve(matrix)
        except UnsolvableDomainError:
            return ErrorResponse(
                error=ErrorDetail(
                    code=DOMAIN_NO_MAGIC_ASSIGNMENT_CODE,
                    message=DOMAIN_NO_MAGIC_ASSIGNMENT_MESSAGE,
                )
            )

    def _try_assignment(
        self,
        matrix: list[list[int]],
        blanks: list[tuple[int, int]],
        first_value: int,
        second_value: int,
    ) -> list[int] | None:
        (r1, c1), (r2, c2) = blanks
        candidate = deepcopy(matrix)
        candidate[r1][c1] = first_value
        candidate[r2][c2] = second_value
        if not self._validator.is_valid(candidate):
            return None
        return [r1, c1, first_value, r2, c2, second_value]
