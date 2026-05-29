"""Boundary validation helpers (FR-01)."""

from __future__ import annotations

from entity.constants import MAX_CELL_VALUE, MIN_CELL_VALUE


def is_matrix_4x4(matrix: list[list[int]], order: int) -> bool:
    if len(matrix) != order:
        return False
    return all(len(row) == order for row in matrix)


def count_blanks(matrix: list[list[int]]) -> int:
    return sum(1 for row in matrix for cell in row if cell == 0)


def has_invalid_value_range(matrix: list[list[int]]) -> bool:
    for row in matrix:
        for cell in row:
            if cell != 0 and not (MIN_CELL_VALUE <= cell <= MAX_CELL_VALUE):
                return True
    return False


def has_duplicate_non_zero(matrix: list[list[int]]) -> bool:
    seen: set[int] = set()
    for row in matrix:
        for cell in row:
            if cell == 0:
                continue
            if cell in seen:
                return True
            seen.add(cell)
    return False
