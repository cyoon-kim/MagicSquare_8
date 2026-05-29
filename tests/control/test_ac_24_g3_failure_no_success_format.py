"""AC-24 — FR-05a failure must not return int[6] success format (FR-06)."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from boundary.boundary_validator import BoundaryValidator
from boundary.models import ErrorResponse
from boundary.result_formatter import ResultFormatter
from control.factory import build_solve_magic_square_use_case
from control.solve_magic_square_use_case import SolveMagicSquareUseCase
from entity.solver import Solver
from grids import G3_MATRIX
from constants import DOMAIN_NO_MAGIC_ASSIGNMENT_CODE


@pytest.mark.control
@pytest.mark.p0
class TestAc24G3FailureNoSuccessFormat:
    """AC-24 — dual-fail domain path returns ErrorResponse, not int[6]."""

    def test_ac_24_g3_execute_returns_domain_error_not_list(self) -> None:
        """AC-24 — G3 (TD-07) → ErrorResponse, never int[6]."""
        use_case = build_solve_magic_square_use_case()

        result = use_case.execute(G3_MATRIX)

        assert isinstance(result, ErrorResponse)
        assert not isinstance(result, list)
        assert result.error.code == DOMAIN_NO_MAGIC_ASSIGNMENT_CODE

    def test_ac_24_g3_result_formatter_not_called_on_domain_failure(self) -> None:
        """AC-24 — ResultFormatter must not run when solver returns error."""
        formatter = MagicMock(spec=ResultFormatter)
        use_case = SolveMagicSquareUseCase(
            boundary_validator=BoundaryValidator(),
            solver=Solver(),
            result_formatter=formatter,
        )

        result = use_case.execute(G3_MATRIX)

        assert isinstance(result, ErrorResponse)
        formatter.format.assert_not_called()
