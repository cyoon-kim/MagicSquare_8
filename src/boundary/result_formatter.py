"""ResultFormatter — FR-05b success output contract."""

from __future__ import annotations

from contracts.errors import (
    ErrorDetail,
    ErrorResponse,
    OUTPUT_FORMAT_INVALID_CODE,
    OUTPUT_FORMAT_INVALID_MESSAGE,
)
from entity.constants import MATRIX_ORDER_4X4, MAX_CELL_VALUE, MIN_CELL_VALUE

_COORD_INDICES = (0, 1, 3, 4)
_VALUE_INDICES = (2, 5)


def _output_format_invalid_response() -> ErrorResponse:
    return ErrorResponse(
        error=ErrorDetail(
            code=OUTPUT_FORMAT_INVALID_CODE,
            message=OUTPUT_FORMAT_INVALID_MESSAGE,
        )
    )


class ResultFormatter:
    """Formats domain success payload to int[6] (1-index coordinates)."""

    def format(self, result: list[int] | ErrorResponse) -> list[int] | ErrorResponse:
        """Validate domain payload and convert 0-index coords to external int[6].

        Args:
            result: Domain success ``int[6]`` (0-index) or ``ErrorResponse``.

        Returns:
            External ``int[6]`` with 1-index coordinates, pass-through error,
            or ``OUTPUT_FORMAT_INVALID`` when AC-19~21 are violated.
        """
        if isinstance(result, ErrorResponse):
            return result
        if len(result) != 6:
            return _output_format_invalid_response()

        max_zero_index = MATRIX_ORDER_4X4 - 1
        for index in _COORD_INDICES:
            if not 0 <= result[index] <= max_zero_index:
                return _output_format_invalid_response()
        for index in _VALUE_INDICES:
            if not MIN_CELL_VALUE <= result[index] <= MAX_CELL_VALUE:
                return _output_format_invalid_response()

        r1, c1, n1, r2, c2, n2 = result
        return [r1 + 1, c1 + 1, n1, r2 + 1, c2 + 1, n2]
