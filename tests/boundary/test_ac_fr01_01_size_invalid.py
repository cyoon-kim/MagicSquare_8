"""FR-01 AC-FR-01-01 — input size validation RED tests (Boundary).

AC-FR-01-01, PRD §8.1 INVALID_SIZE / Grid must be 4x4.
Scope: size-only failures. AC-FR-01-02~05 and FR-02~05 excluded.
"""

from __future__ import annotations

from boundary.boundary_validator import BoundaryValidator
from boundary.models import ErrorResponse, INVALID_SIZE_CODE


class TestAcFr0101SizeInvalidBoundary:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — Boundary validate() failures."""

    def test_grid_none_returns_invalid_size_error_code(
        self,
        invalid_size_code: str,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — null grid failure code."""
        # Given: grid is explicitly None (BV-01)



    def test_grid_none_message_matches_prd_section_8_1_exactly(
        self,
        invalid_size_message: str,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — message character-level match."""
        # Given: grid is None and PRD §8.1 fixed message is defined
        validator = BoundaryValidator()
        grid = None
        expected_message = "Grid must be 4x4."

        # When: Boundary validates the grid
        result = validator.validate(grid)

        # AC-FR-01-01
        assert result is not None
        assert result.error.message == invalid_size_message
        assert result.error.message == expected_message

    def test_grid_empty_list_returns_invalid_size_error_code(
        self,
        invalid_size_code: str,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — empty list boundary."""
        # Given: grid is an empty list (BV-02)
        validator = BoundaryValidator()
        grid: list[list[int]] = []

        # When: Boundary validates the grid
        result = validator.validate(grid)

        # AC-FR-01-01
        assert result is not None
        assert result.error.code == invalid_size_code

    def test_grid_four_empty_rows_returns_invalid_size_error_code(
        self,
        invalid_size_code: str,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — rows present, zero columns."""
        # Given: grid has four rows but each row is empty (BV-03)
        validator = BoundaryValidator()
        grid: list[list[int]] = [[]] * 4

        # When: Boundary validates the grid
        result = validator.validate(grid)

        # AC-FR-01-01
        assert result is not None
        assert result.error.code == invalid_size_code

    def test_grid_3x4_returns_invalid_size_error_code(
        self,
        grid_3x4: list[list[int]],
        invalid_size_code: str,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — row count mismatch (3×4)."""
        # Given: grid is 3 rows × 4 columns (BV-04)
        validator = BoundaryValidator()

        # When: Boundary validates the grid
        result = validator.validate(grid_3x4)

        # AC-FR-01-01
        assert result is not None
        assert result.error.code == invalid_size_code
