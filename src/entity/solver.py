"""Solver — FR-05a two-cell magic square assignment."""

from __future__ import annotations

from copy import deepcopy

from contracts.errors import (
    DOMAIN_BLANK_COUNT_CODE,
    DOMAIN_BLANK_COUNT_MESSAGE,
    DOMAIN_MISSING_COUNT_CODE,
    DOMAIN_MISSING_COUNT_MESSAGE,
    DOMAIN_NO_MAGIC_ASSIGNMENT_CODE,
    DOMAIN_NO_MAGIC_ASSIGNMENT_MESSAGE,
    ErrorDetail,
    ErrorResponse,
)
from entity.blank_finder import BlankFinder
from entity.magic_square_validator import MagicSquareValidator
from entity.missing_number_finder import MissingNumberFinder


def _domain_error(code: str, message: str) -> ErrorResponse:
    return ErrorResponse(error=ErrorDetail(code=code, message=message))


class Solver:
    """Tries two assignment orders for two blanks; returns int[6] 0-index."""

    def __init__(self) -> None:
        self._blank_finder = BlankFinder()
        self._missing_finder = MissingNumberFinder()
        self._validator = MagicSquareValidator()

    def solve(self, matrix: list[list[int]]) -> list[int] | ErrorResponse:
        """Solve two-cell assignment or return a §13 domain error object.

        Args:
            matrix: Validated 4×4 grid with exactly two blanks.

        Returns:
            Domain success ``int[6]`` (0-index) or ``ErrorResponse``.
        """
        blanks = self._blank_finder.find(matrix)
        if len(blanks) != 2:
            return _domain_error(DOMAIN_BLANK_COUNT_CODE, DOMAIN_BLANK_COUNT_MESSAGE)
        missing = self._missing_finder.find(matrix)
        if len(missing) != 2:
            return _domain_error(
                DOMAIN_MISSING_COUNT_CODE,
                DOMAIN_MISSING_COUNT_MESSAGE,
            )
        attempts = [
            (missing[0], missing[1]),
            (missing[1], missing[0]),
        ]
        for first, second in attempts:
            payload = self._try_assignment(matrix, blanks, first, second)
            if payload is not None:
                return payload
        return _domain_error(
            DOMAIN_NO_MAGIC_ASSIGNMENT_CODE,
            DOMAIN_NO_MAGIC_ASSIGNMENT_MESSAGE,
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
