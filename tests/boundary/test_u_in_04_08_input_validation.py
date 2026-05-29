"""Track A — U-IN-04~08 input validation RED skeletons (FR-01 AC-02~04).

U-IN-01~03: covered by Report/08 Full RED (test_fr01_ac01_*) — do not duplicate.
"""

from __future__ import annotations

import pytest

# from boundary.input_validator import InputValidator
# from boundary.models import ErrorResponse


@pytest.mark.boundary
@pytest.mark.p0
class TestUIn04Through08InputValidation:
    """FR-01 Boundary input contract — value range, blank count, duplicate."""

    def test_u_in_04_negative_value_returns_e004(self) -> None:
        """U-IN-04 — value -1 returns INPUT_VALUE_RANGE_INVALID (E004)."""
        # Given: 4x4 G1-like grid with -1 at (3,3) 1-index
        # matrix = [
        #     [16, 3, 2, 13],
        #     [5, 0, 11, 8],
        #     [9, 6, 0, 12],
        #     [4, 15, 14, -1],
        # ]
        # validator = InputValidator()
        # When: validator.validate(matrix)
        pytest.fail("RED: U-IN-04 — -1 cell returns E004 INPUT_VALUE_RANGE_INVALID")

    def test_u_in_05_value_17_returns_e004(self) -> None:
        """U-IN-05 — value 17 returns INPUT_VALUE_RANGE_INVALID (E004)."""
        # Given: 4x4, two blanks, one cell is 17 (TD-05)
        # validator = InputValidator()
        # When: validator.validate(matrix)
        pytest.fail("RED: U-IN-05 — 17 cell returns E004 INPUT_VALUE_RANGE_INVALID")

    def test_u_in_06_duplicate_non_zero_returns_e005(self) -> None:
        """U-IN-06 — duplicate non-zero returns INPUT_DUPLICATE_NON_ZERO (E005)."""
        # Given: 4x4, two blanks, 8 appears twice (TD-06)
        # matrix = [
        #     [16, 3, 2, 13],
        #     [5, 0, 11, 8],
        #     [9, 6, 0, 12],
        #     [4, 15, 14, 8],
        # ]
        # validator = InputValidator()
        # When: validator.validate(matrix)
        pytest.fail("RED: U-IN-06 — duplicate 8 returns E005 INPUT_DUPLICATE_NON_ZERO")

    def test_u_in_07_zero_blank_cells_returns_e002(self) -> None:
        """U-IN-07 — no blanks (G0) returns INPUT_BLANK_COUNT_INVALID (E002)."""
        # Given: G0 complete grid (zero blanks)
        # validator = InputValidator()
        # When: validator.validate(matrix)
        pytest.fail("RED: U-IN-07 — G0 zero blanks returns E002 INPUT_BLANK_COUNT_INVALID")

    def test_u_in_08_three_blanks_returns_e002(self) -> None:
        """U-IN-08 — three zeros returns INPUT_BLANK_COUNT_INVALID (E002)."""
        # Given: 4x4 with three 0 cells
        # matrix = [[0, 0, 0, 1], [2, 3, 4, 5], [6, 7, 8, 9], [10, 11, 12, 13]]
        # validator = InputValidator()
        # When: validator.validate(matrix)
        pytest.fail("RED: U-IN-08 — three blanks returns E002 INPUT_BLANK_COUNT_INVALID")
