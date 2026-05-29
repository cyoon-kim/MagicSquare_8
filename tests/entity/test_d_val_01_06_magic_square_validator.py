"""Track B — D-VAL-01~06 magic square validation (FR-04)."""

from __future__ import annotations

import pytest

from entity.magic_square_validator import MagicSquareValidator
from grids import G0_MATRIX


@pytest.mark.domain
@pytest.mark.p0
class TestDVal01Through06MagicSquareValidator:
    """D-VAL — MagicSquareValidator.is_valid."""

    def test_d_val_01_g0_complete_grid_returns_true(self) -> None:
        validator = MagicSquareValidator()

        assert validator.is_valid(G0_MATRIX) is True

    def test_d_val_02_row_sum_mismatch_returns_false(self) -> None:
        matrix = [row[:] for row in G0_MATRIX]
        matrix[0][0] = 17
        validator = MagicSquareValidator()

        assert validator.is_valid(matrix) is False

    def test_d_val_03_column_sum_mismatch_returns_false(self) -> None:
        matrix = [row[:] for row in G0_MATRIX]
        matrix[0][3] = 20
        validator = MagicSquareValidator()

        assert validator.is_valid(matrix) is False

    def test_d_val_04_diagonal_sum_mismatch_returns_false(self) -> None:
        matrix = [row[:] for row in G0_MATRIX]
        matrix[0][0] = 1
        validator = MagicSquareValidator()

        assert validator.is_valid(matrix) is False

    def test_d_val_04_anti_diagonal_mismatch_returns_false(self) -> None:
        matrix = [row[:] for row in G0_MATRIX]
        matrix[0][3] = 12
        matrix[3][0] = 5
        validator = MagicSquareValidator()

        assert validator.is_valid(matrix) is False

    def test_d_val_05_duplicate_values_returns_false(self) -> None:
        matrix = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 8],
        ]
        validator = MagicSquareValidator()

        assert validator.is_valid(matrix) is False

    def test_d_val_06_zero_in_candidate_grid_returns_false(self) -> None:
        matrix = [row[:] for row in G0_MATRIX]
        matrix[0][0] = 0
        validator = MagicSquareValidator()

        assert validator.is_valid(matrix) is False
