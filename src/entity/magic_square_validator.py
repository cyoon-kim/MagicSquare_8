"""MagicSquareValidator — FR-04 magic square validation."""

from __future__ import annotations

from entity.constants import MAGIC_CONSTANT_4X4, MATRIX_ORDER_4X4


class MagicSquareValidator:
    """Validates a complete 4x4 grid (no zeros) against magic square rules."""

    def is_valid(self, matrix: list[list[int]]) -> bool:
        if any(cell == 0 for row in matrix for cell in row):
            return False
        order = MATRIX_ORDER_4X4
        values = [cell for row in matrix for cell in row]
        if len(values) != len(set(values)):
            return False
        target = MAGIC_CONSTANT_4X4
        for row in matrix:
            if sum(row) != target:
                return False
        for col in range(order):
            if sum(matrix[row][col] for row in range(order)) != target:
                return False
        if sum(matrix[i][i] for i in range(order)) != target:
            return False
        if sum(matrix[i][order - 1 - i] for i in range(order)) != target:
            return False
        return True
