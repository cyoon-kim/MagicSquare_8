"""RED-BND-OUT-002 — AC-22 invalid domain coordinates (FR-05b)."""

from __future__ import annotations

import pytest

from boundary.models import ErrorResponse
from boundary.result_formatter import ResultFormatter
from constants import OUTPUT_FORMAT_INVALID_CODE


@pytest.mark.boundary
@pytest.mark.p0
class TestRedBndOut002FormatInvalidCoords:
    """AC-22 — domain r/c fields must be 0-index in range 0..3."""

    def test_red_bnd_out_002_out_of_range_column_returns_output_format_invalid(
        self,
    ) -> None:
        """RED-BND-OUT-002 — c=5 in domain payload → OUTPUT_FORMAT_INVALID."""
        formatter = ResultFormatter()
        out_of_range = [1, 5, 3, 2, 4, 13]

        result = formatter.format(out_of_range)

        assert isinstance(result, ErrorResponse)
        assert result.error.code == OUTPUT_FORMAT_INVALID_CODE

    def test_red_bnd_out_002_out_of_range_row_returns_output_format_invalid(
        self,
    ) -> None:
        """RED-BND-OUT-002 — r=4 in domain payload → OUTPUT_FORMAT_INVALID."""
        formatter = ResultFormatter()
        out_of_range = [4, 2, 3, 1, 4, 13]

        result = formatter.format(out_of_range)

        assert isinstance(result, ErrorResponse)
        assert result.error.code == OUTPUT_FORMAT_INVALID_CODE
