"""Boundary validation helpers (FR-01)."""

from __future__ import annotations

from entity.constants import MAX_CELL_VALUE, MIN_CELL_VALUE


def is_matrix_4x4(matrix: list[list[int]], order: int) -> bool:
    """Return True when matrix has ``order`` rows each with ``order`` columns.

    Args:
        matrix: Candidate input grid.
        order: Expected row and column count.

    Returns:
        True if dimensions match ``order x order``.
    """
    if len(matrix) != order:
        return False
    return all(len(row) == order for row in matrix)


def count_blanks(matrix: list[list[int]]) -> int:
    """Count cells equal to zero (blank placeholders).

    Args:
        matrix: Input grid.

    Returns:
        Number of zero-valued cells.
    """
    return sum(1 for row in matrix for cell in row if cell == 0)


def has_invalid_value_range(matrix: list[list[int]]) -> bool:
    """Return True when a non-zero cell is outside ``MIN..MAX`` cell values.

    Args:
        matrix: Input grid.

    Returns:
        True if any non-zero value violates the allowed range.
    """
    for row in matrix:
        for cell in row:
            if cell != 0 and not (MIN_CELL_VALUE <= cell <= MAX_CELL_VALUE):
                return True
    return False


def has_duplicate_non_zero(matrix: list[list[int]]) -> bool:
    """Return True when non-zero values appear more than once.

    Args:
        matrix: Input grid.

    Returns:
        True if duplicate non-zero values exist.
    """
    seen: set[int] = set()
    for row in matrix:
        for cell in row:
            if cell == 0:
                continue
            if cell in seen:
                return True
            seen.add(cell)
    return False
