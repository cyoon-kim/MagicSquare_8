"""Shared error DTO and §13 error codes (PRD schema SSOT)."""

from __future__ import annotations

from pydantic import BaseModel

INPUT_SIZE_INVALID_CODE = "INPUT_SIZE_INVALID"
INPUT_SIZE_INVALID_MESSAGE = "Input matrix must be 4x4."
INPUT_BLANK_COUNT_INVALID_CODE = "INPUT_BLANK_COUNT_INVALID"
INPUT_BLANK_COUNT_INVALID_MESSAGE = "Input must contain exactly two blanks (0)."
INPUT_VALUE_RANGE_INVALID_CODE = "INPUT_VALUE_RANGE_INVALID"
INPUT_VALUE_RANGE_INVALID_MESSAGE = "Input values must be 0 or between 1 and 16."
INPUT_DUPLICATE_NON_ZERO_CODE = "INPUT_DUPLICATE_NON_ZERO"
INPUT_DUPLICATE_NON_ZERO_MESSAGE = "Non-zero values must be unique."
DOMAIN_NO_MAGIC_ASSIGNMENT_CODE = "DOMAIN_NO_MAGIC_ASSIGNMENT"
DOMAIN_NO_MAGIC_ASSIGNMENT_MESSAGE = (
    "No valid magic-square assignment exists for the two missing numbers."
)


class ErrorDetail(BaseModel):
    """Single error entry in the §13 response schema."""

    code: str
    message: str


class ErrorResponse(BaseModel):
    """Standard business-error envelope (PRD §13)."""

    error: ErrorDetail
