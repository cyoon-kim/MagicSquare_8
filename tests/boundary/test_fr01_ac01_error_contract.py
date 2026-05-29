"""FR-01 AC-01 — standard error schema RED tests.

AC-01, PRD §13 { error: { code, message } } via Pydantic ErrorResponse.
"""

from __future__ import annotations

import pytest

from boundary.boundary_validator import BoundaryValidator
from boundary.models import ErrorResponse


@pytest.mark.boundary
@pytest.mark.p0
class TestFr01Ac01ErrorContract:
    """FR-01 AC-01 — §13 error envelope contract."""

    def test_matrix_none_error_matches_prd_section_13_schema(
        self,
    ) -> None:
        """AC-01, PRD §13 — ErrorResponse model_dump shape."""
        # Given: matrix is None
        validator = BoundaryValidator()
        matrix = None

        # When: Boundary validates the matrix
        result = validator.validate(matrix)

        # Then: AC-01
        assert result is not None
        parsed = ErrorResponse.model_validate(result.model_dump())
        assert parsed.error.code == "INPUT_SIZE_INVALID"
        assert parsed.error.message == "Input matrix must be 4x4."
        dumped = parsed.model_dump()
        assert dumped == {
            "error": {
                "code": "INPUT_SIZE_INVALID",
                "message": "Input matrix must be 4x4.",
            }
        }
