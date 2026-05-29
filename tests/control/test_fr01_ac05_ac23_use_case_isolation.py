"""FR-01 AC-05 / FR-06 AC-23 — Domain chain isolation tests.

AC-05, AC-23: FR-01 failure must not invoke Domain or ResultFormatter.
PRD §13 INPUT_SIZE_INVALID on size-invalid matrix.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from boundary.boundary_validator import BoundaryValidator
from boundary.result_formatter import ResultFormatter
from control.solve_magic_square_use_case import SolveMagicSquareUseCase
from entity.solver import Solver


@pytest.mark.control
@pytest.mark.p0
class TestFr01Ac05Ac23UseCaseIsolation:
    """FR-06 orchestration — no Solver/Formatter on FR-01 fail."""

    @staticmethod
    def _build_use_case_with_mocks() -> tuple[SolveMagicSquareUseCase, dict[str, MagicMock]]:
        """Arrange collaborators as MagicMock for call-count verification."""
        mocks = {
            "solver": MagicMock(spec=Solver),
            "result_formatter": MagicMock(spec=ResultFormatter),
        }
        use_case = SolveMagicSquareUseCase(
            boundary_validator=BoundaryValidator(),
            solver=mocks["solver"],
            result_formatter=mocks["result_formatter"],
        )
        return use_case, mocks

    def test_matrix_none_domain_chain_called_zero_times(
        self,
        input_size_invalid_code: str,
    ) -> None:
        """AC-05, AC-23 — Solver not called when matrix is None."""
        use_case, mocks = self._build_use_case_with_mocks()
        matrix = None

        result = use_case.execute(matrix)

        mocks["solver"].solve.assert_not_called()
        assert result is not None
        assert result.error.code == input_size_invalid_code

    def test_matrix_none_result_formatter_called_zero_times(
        self,
    ) -> None:
        """AC-23 — ResultFormatter must not run when FR-01 fails."""
        use_case, mocks = self._build_use_case_with_mocks()
        matrix = None

        use_case.execute(matrix)

        mocks["result_formatter"].format.assert_not_called()

    @pytest.mark.parametrize(
        "matrix",
        [
            pytest.param(None, id="BV-01-none"),
            pytest.param([], id="BV-02-empty"),
            pytest.param([[], [], [], []], id="BV-03-four-empty-rows"),
        ],
    )
    def test_invalid_size_matrix_domain_chain_never_invoked(
        self,
        matrix: list[list[int]] | None,
    ) -> None:
        """AC-05, AC-23 — isolation holds for all AC-01 boundary inputs."""
        use_case, mocks = self._build_use_case_with_mocks()

        use_case.execute(matrix)

        mocks["solver"].solve.assert_not_called()
        mocks["result_formatter"].format.assert_not_called()
