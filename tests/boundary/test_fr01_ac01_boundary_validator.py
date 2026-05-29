"""FR-01 AC-01 — BoundaryValidator size validation RED tests.

AC-01, PRD §13 INPUT_SIZE_INVALID / Input matrix must be 4x4.
Scope: AC-01 only. AC-02~04 and FR-02~05a excluded.
"""

from __future__ import annotations

import pytest

from boundary.boundary_validator import BoundaryValidator
from boundary.models import ErrorResponse


@pytest.mark.boundary
@pytest.mark.p0
class TestFr01Ac01BoundaryValidator:
    """FR-01 AC-01 — 4x4 size contract at Boundary layer."""

    def test_matrix_none_returns_input_size_invalid_code(
        self,
        input_size_invalid_code: str,
    ) -> None:
        """AC-01, PRD §13 INPUT_SIZE_INVALID — null matrix failure code."""
        # Given: matrix is explicitly None (BV-01)
        validator = BoundaryValidator()
        matrix = None

        # When: Boundary validates the matrix
        result = validator.validate(matrix)

        # Then: AC-01
        assert result is not None
        assert isinstance(result, ErrorResponse)
        assert result.error.code == input_size_invalid_code

    def test_matrix_none_message_matches_prd_section_13_exactly(
        self,
        input_size_invalid_message: str,
    ) -> None:
        """AC-01, PRD §13 INPUT_SIZE_INVALID — message character-level match."""
        # Given: matrix is None and PRD §13 fixed message is defined
        validator = BoundaryValidator()
        matrix = None

        # When: Boundary validates the matrix
        result = validator.validate(matrix)

        # Then: AC-01
        assert result is not None
        assert result.error.message == input_size_invalid_message

    def test_matrix_none_returns_error_without_exception(
        self,
    ) -> None:
        """AC-01, FR-01 Error Policy — business failure returns object, no throw."""
        # Given: matrix is None
        validator = BoundaryValidator()
        matrix = None

        # When / Then: AC-01 — must not raise; returns ErrorResponse
        result = validator.validate(matrix)
        assert result is not None
        assert isinstance(result, ErrorResponse)

    @pytest.mark.parametrize(
        "matrix",
        [
            pytest.param([], id="BV-02-empty"),
            pytest.param([[], [], [], []], id="BV-03-four-empty-rows"),
            pytest.param(
                [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],
                id="BV-04-3x4",
            ),
            pytest.param(
                [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]],
                id="BV-05-4x3",
            ),
            pytest.param([[0] * 5 for _ in range(5)], id="BV-06-5x5"),
            pytest.param([[1, 2], [3, 4]], id="TD-03-2x2"),
        ],
    )
    def test_invalid_size_matrices_return_input_size_invalid_code(
        self,
        matrix: list[list[int]] | None,
        input_size_invalid_code: str,
    ) -> None:
        """AC-01, PRD §13 — boundary value size violations."""
        # Given: matrix violates 4x4 contract
        validator = BoundaryValidator()

        # When: Boundary validates the matrix
        result = validator.validate(matrix)

        # Then: AC-01
        assert result is not None
        assert result.error.code == input_size_invalid_code
