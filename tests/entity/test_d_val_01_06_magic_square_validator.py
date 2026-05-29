"""Track B — D-VAL-01~06 magic square validation RED skeletons (FR-04).

Domain Mock forbidden. M=34 (MAGIC_CONSTANT_4X4).
"""

from __future__ import annotations

import pytest

# from entity.magic_square_validator import MagicSquareValidator
# from entity.services.magic_square_validator import is_magic_square


@pytest.mark.domain
@pytest.mark.p0
class TestDVal01Through06MagicSquareValidator:
    """D-VAL — is_magic_square / MagicSquareValidator.is_valid."""

    def test_d_val_01_g0_complete_grid_returns_true(self) -> None:
        """D-VAL-01 — G0 full magic square."""
        # Given: G0_MATRIX
        # validator = MagicSquareValidator()
        # When: validator.is_valid(g0_matrix)
        pytest.fail("RED: D-VAL-01 — G0 complete grid is_magic_square True")

    def test_d_val_02_row_sum_mismatch_returns_false(self) -> None:
        """D-VAL-02 — G0 with (0,0) 16->17 breaks row sum."""
        # Given: mutated G0 row 0
        # When: validator.is_valid(matrix)
        pytest.fail("RED: D-VAL-02 — row sum mismatch returns False")

    def test_d_val_03_column_sum_mismatch_returns_false(self) -> None:
        """D-VAL-03 — G0 with (0,3) 13->20 breaks column 4."""
        # Given: mutated G0
        # When: validator.is_valid(matrix)
        pytest.fail("RED: D-VAL-03 — column sum mismatch returns False")

    def test_d_val_04_diagonal_sum_mismatch_returns_false(self) -> None:
        """D-VAL-04 — main diagonal sum != 34."""
        # Given: G0 with single main-diagonal cell mutation
        # When: validator.is_valid(matrix)
        pytest.fail("RED: D-VAL-04 — diagonal sum mismatch returns False")

    def test_d_val_05_duplicate_values_returns_false(self) -> None:
        """D-VAL-05 — filled grid with duplicate 8."""
        # Given: 4x4 no zeros, 8 twice
        # When: validator.is_valid(matrix)
        pytest.fail("RED: D-VAL-05 — duplicate 1..16 set returns False")

    def test_d_val_06_zero_in_candidate_grid_returns_false(self) -> None:
        """D-VAL-06 — grid containing 0 is not checkable (AC-15)."""
        # Given: G0 with one cell replaced by 0
        # When: validator.is_valid(matrix)
        pytest.fail("RED: D-VAL-06 — zero in candidate grid returns False")
