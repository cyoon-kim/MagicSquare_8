"""R6 — UseCase delegates domain work solely to Solver."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from boundary.boundary_validator import BoundaryValidator
from boundary.result_formatter import ResultFormatter
from control.solve_magic_square_use_case import SolveMagicSquareUseCase
from entity.solver import Solver
from grids import G1_MATRIX


@pytest.mark.control
@pytest.mark.p0
class TestR6UseCaseOrchestration:
    """FR-06 — no redundant blank/missing finder calls at use case layer."""

    def test_r6_success_path_calls_solver_once_only(self) -> None:
        """R6 — execute invokes Solver.solve exactly once on success path."""
        solver = MagicMock(spec=Solver)
        solver.solve.return_value = [0, 1, 3, 0, 3, 13]
        use_case = SolveMagicSquareUseCase(
            boundary_validator=BoundaryValidator(),
            solver=solver,
            result_formatter=ResultFormatter(),
        )

        use_case.execute(G1_MATRIX)

        solver.solve.assert_called_once_with(G1_MATRIX)
