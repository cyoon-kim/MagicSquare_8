"""RED-BND-OUT-001 — AC-22 malformed output length (FR-05b)."""

from __future__ import annotations

import pytest

from boundary.models import ErrorResponse
from boundary.result_formatter import ResultFormatter
from constants import OUTPUT_FORMAT_INVALID_CODE


@pytest.mark.boundary
@pytest.mark.p0
class TestRedBndOut001FormatInvalidLength:
    """AC-22 — int array length must be 6."""

    def test_red_bnd_out_001_length_five_returns_output_format_invalid(self) -> None:
        """RED-BND-OUT-001 — len=5 payload → OUTPUT_FORMAT_INVALID."""
        formatter = ResultFormatter()
        malformed = [1, 2, 3, 1, 4]

        result = formatter.format(malformed)

        assert isinstance(result, ErrorResponse)
        assert result.error.code == OUTPUT_FORMAT_INVALID_CODE

    def test_red_bnd_out_001_length_seven_returns_output_format_invalid(self) -> None:
        """RED-BND-OUT-001 — len=7 payload → OUTPUT_FORMAT_INVALID."""
        formatter = ResultFormatter()
        malformed = [1, 2, 3, 1, 4, 13, 99]

        result = formatter.format(malformed)

        assert isinstance(result, ErrorResponse)
        assert result.error.code == OUTPUT_FORMAT_INVALID_CODE
