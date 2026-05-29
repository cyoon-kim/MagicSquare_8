"""Track A — U-IN-04~08 input validation (FR-01 AC-02~04)."""

from __future__ import annotations

import pytest

from boundary.boundary_validator import BoundaryValidator
from boundary.models import ErrorResponse
from grids import G0_MATRIX


@pytest.mark.boundary
@pytest.mark.p0
class TestUIn04Through08InputValidation:
    """FR-01 Boundary input contract — value range, blank count, duplicate."""

    def test_u_in_04_negative_value_returns_e004(self) -> None:
        """U-IN-04 — value -1 returns INPUT_VALUE_RANGE_INVALID."""
        matrix = [
            [16, 3, 2, 13],
            [5, 0, 11, 8],
            [9, 6, 0, 12],
            [4, 15, 14, -1],
        ]
        validator = BoundaryValidator()

        result = validator.validate(matrix)

        assert result is not None
        assert isinstance(result, ErrorResponse)
        assert result.error.code == "INPUT_VALUE_RANGE_INVALID"

    def test_u_in_05_value_17_returns_e004(self) -> None:
        """U-IN-05 — value 17 returns INPUT_VALUE_RANGE_INVALID."""
        matrix = [
            [16, 3, 2, 13],
            [5, 0, 11, 8],
            [9, 6, 0, 12],
            [4, 15, 14, 17],
        ]
        validator = BoundaryValidator()

        result = validator.validate(matrix)

        assert result is not None
        assert result.error.code == "INPUT_VALUE_RANGE_INVALID"

    def test_u_in_06_duplicate_non_zero_returns_e005(self) -> None:
        """U-IN-06 — duplicate non-zero returns INPUT_DUPLICATE_NON_ZERO."""
        matrix = [
            [16, 3, 2, 13],
            [5, 0, 11, 8],
            [9, 6, 0, 12],
            [4, 15, 14, 8],
        ]
        validator = BoundaryValidator()

        result = validator.validate(matrix)

        assert result is not None
        assert result.error.code == "INPUT_DUPLICATE_NON_ZERO"

    def test_u_in_07_zero_blank_cells_returns_e002(self) -> None:
        """U-IN-07 — no blanks (G0) returns INPUT_BLANK_COUNT_INVALID."""
        validator = BoundaryValidator()

        result = validator.validate(G0_MATRIX)

        assert result is not None
        assert result.error.code == "INPUT_BLANK_COUNT_INVALID"

    def test_u_in_08_three_blanks_returns_e002(self) -> None:
        """U-IN-08 — three zeros returns INPUT_BLANK_COUNT_INVALID."""
        matrix = [[0, 0, 0, 1], [2, 3, 4, 5], [6, 7, 8, 9], [10, 11, 12, 13]]
        validator = BoundaryValidator()

        result = validator.validate(matrix)

        assert result is not None
        assert result.error.code == "INPUT_BLANK_COUNT_INVALID"
