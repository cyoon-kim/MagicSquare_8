"""RED-BND-OUT-002 — AC-22 invalid 1-index coordinates (FR-05b).

Fails until R4: ResultFormatter must return OUTPUT_FORMAT_INVALID when
coordinate fields are not in 1..4 (includes 0-index leakage).
Excluded from p0 gate via red_bnd_out marker (intentional RED until slice B).
"""

from __future__ import annotations

import pytest

from boundary.models import ErrorResponse
from boundary.result_formatter import ResultFormatter
from constants import OUTPUT_FORMAT_INVALID_CODE


@pytest.mark.boundary
@pytest.mark.red_bnd_out
class TestRedBndOut002FormatInvalidCoords:
    """AC-22 — r/c fields must be 1-index in range 1..4."""

    def test_red_bnd_out_002_zero_index_row_returns_output_format_invalid(
        self,
    ) -> None:
        """RED-BND-OUT-002 — r=0 (0-index) → OUTPUT_FORMAT_INVALID."""
        formatter = ResultFormatter()
        zero_index_row = [0, 2, 3, 1, 4, 13]

        result = formatter.format(zero_index_row)

        assert isinstance(result, ErrorResponse)
        assert result.error.code == OUTPUT_FORMAT_INVALID_CODE

    def test_red_bnd_out_002_out_of_range_column_returns_output_format_invalid(
        self,
    ) -> None:
        """RED-BND-OUT-002 — c=5 → OUTPUT_FORMAT_INVALID."""
        formatter = ResultFormatter()
        out_of_range = [1, 5, 3, 2, 4, 13]

        result = formatter.format(out_of_range)

        assert isinstance(result, ErrorResponse)
        assert result.error.code == OUTPUT_FORMAT_INVALID_CODE
