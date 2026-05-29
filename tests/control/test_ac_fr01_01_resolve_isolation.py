"""FR-01 AC-FR-01-01 — Domain resolve() isolation RED tests (Control).

AC-FR-01-01, PRD §8.1 INVALID_SIZE — resolve() must not run on size failure.
Scope: AC-FR-01-01 only. AC-FR-01-02~05 and FR-02~05 excluded.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from boundary.models import INVALID_SIZE_CODE
from control.magic_square_service import MagicSquareService


class TestAcFr0101ResolveIsolation:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — resolve() call-count isolation."""

    def test_grid_none_resolve_called_zero_times(
        self,
        invalid_size_code: str,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — resolve() spy must stay at 0."""
        # Given: grid is None and resolve is spied via mock
        service = MagicSquareService()
        grid = None

        # When: service executes with invalid grid
        with patch.object(service, "resolve", wraps=service.resolve) as resolve_spy:
            result = service.execute(grid)

        # AC-FR-01-01
        assert resolve_spy.call_count == 0
        assert result is not None
        assert hasattr(result, "error")
        assert result.error.code == INVALID_SIZE_CODE

    def test_grid_none_does_not_invoke_domain_resolve_via_mock_injection(
        self,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — mock resolve never receives None grid."""
        # Given: resolve replaced with MagicMock to detect any Domain entry
        service = MagicSquareService()
        service.resolve = MagicMock()  # type: ignore[method-assign]
        grid = None

        # When: service executes with None grid
        service.execute(grid)

        # AC-FR-01-01
        service.resolve.assert_not_called()
