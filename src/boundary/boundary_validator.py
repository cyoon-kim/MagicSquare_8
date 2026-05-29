"""BoundaryValidator — FR-01 AC-01~04 size and input contract."""

from __future__ import annotations

from contracts.errors import (
    ErrorDetail,
    ErrorResponse,
    INPUT_BLANK_COUNT_INVALID_CODE,
    INPUT_BLANK_COUNT_INVALID_MESSAGE,
    INPUT_DUPLICATE_NON_ZERO_CODE,
    INPUT_DUPLICATE_NON_ZERO_MESSAGE,
    INPUT_SIZE_INVALID_CODE,
    INPUT_SIZE_INVALID_MESSAGE,
    INPUT_VALUE_RANGE_INVALID_CODE,
    INPUT_VALUE_RANGE_INVALID_MESSAGE,
)
from boundary.validation import (
    count_blanks,
    has_duplicate_non_zero,
    has_invalid_value_range,
    is_matrix_4x4,
)

MATRIX_ORDER_4X4: int = 4
REQUIRED_BLANK_COUNT: int = 2


def _error_response(code: str, message: str) -> ErrorResponse:
    return ErrorResponse(error=ErrorDetail(code=code, message=message))


def _input_size_invalid_response() -> ErrorResponse:
    return _error_response(INPUT_SIZE_INVALID_CODE, INPUT_SIZE_INVALID_MESSAGE)


class BoundaryValidator:
    """Validates matrix input at the Boundary layer."""

    def validate(
        self, matrix: list[list[int]] | None
    ) -> ErrorResponse | None:
        if matrix is None:
            return _input_size_invalid_response()
        if not is_matrix_4x4(matrix, MATRIX_ORDER_4X4):
            return _input_size_invalid_response()
        if count_blanks(matrix) != REQUIRED_BLANK_COUNT:
            return _error_response(
                INPUT_BLANK_COUNT_INVALID_CODE,
                INPUT_BLANK_COUNT_INVALID_MESSAGE,
            )
        if has_invalid_value_range(matrix):
            return _error_response(
                INPUT_VALUE_RANGE_INVALID_CODE,
                INPUT_VALUE_RANGE_INVALID_MESSAGE,
            )
        if has_duplicate_non_zero(matrix):
            return _error_response(
                INPUT_DUPLICATE_NON_ZERO_CODE,
                INPUT_DUPLICATE_NON_ZERO_MESSAGE,
            )
        return None
