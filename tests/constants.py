"""PRD §13 error constants for RED tests (no src dependency)."""

from __future__ import annotations

INPUT_SIZE_INVALID_CODE: str = "INPUT_SIZE_INVALID"
INPUT_SIZE_INVALID_MESSAGE: str = "Input matrix must be 4x4."
INPUT_BLANK_COUNT_INVALID_CODE: str = "INPUT_BLANK_COUNT_INVALID"
INPUT_BLANK_COUNT_INVALID_MESSAGE: str = "Input must contain exactly two blanks (0)."
INPUT_VALUE_RANGE_INVALID_CODE: str = "INPUT_VALUE_RANGE_INVALID"
INPUT_VALUE_RANGE_INVALID_MESSAGE: str = "Input values must be 0 or between 1 and 16."
INPUT_DUPLICATE_NON_ZERO_CODE: str = "INPUT_DUPLICATE_NON_ZERO"
INPUT_DUPLICATE_NON_ZERO_MESSAGE: str = "Non-zero values must be unique."
OUTPUT_FORMAT_INVALID_CODE: str = "OUTPUT_FORMAT_INVALID"
OUTPUT_FORMAT_INVALID_MESSAGE: str = (
    "Output must be an int array of length 6 with 1-index coordinates."
)
DOMAIN_NO_MAGIC_ASSIGNMENT_CODE: str = "DOMAIN_NO_MAGIC_ASSIGNMENT"
DOMAIN_BLANK_COUNT_CODE: str = "DOMAIN_BLANK_COUNT"
DOMAIN_BLANK_COUNT_MESSAGE: str = "Domain blank count invariant violated."
DOMAIN_MISSING_COUNT_CODE: str = "DOMAIN_MISSING_COUNT"
DOMAIN_MISSING_COUNT_MESSAGE: str = "Domain missing number count invariant violated."
