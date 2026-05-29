"""Track B — D-SOL-01~04 two-cell solver (FR-05a)."""

from __future__ import annotations

import pytest

from boundary.models import DOMAIN_NO_MAGIC_ASSIGNMENT_CODE, ErrorResponse
from entity.exceptions import UnsolvableDomainError
from entity.solver import Solver
from grids import G0_MATRIX, G1_EXPECTED_STEP_A, G1_MATRIX, G2_MATRIX, G3_MATRIX


@pytest.mark.domain
@pytest.mark.p0
class TestDSol01Through04TwoCellSolver:
    """D-SOL — Solver.solve -> int[6] 1-index or domain failure."""

    def test_d_sol_01_g1_step_a_success_int_six(self) -> None:
        solver = Solver()

        result = solver.solve(G1_MATRIX)

        assert result == G1_EXPECTED_STEP_A

    def test_d_sol_02_g2_step_b_reverse_success(self) -> None:
        solver = Solver()

        result = solver.solve(G2_MATRIX)

        assert result == [1, 1, 16, 1, 2, 3]

    def test_d_sol_03_g3_dual_fail_unsolvable(self) -> None:
        solver = Solver()

        with pytest.raises(UnsolvableDomainError):
            solver.solve(G3_MATRIX)

    def test_d_sol_03_solve_or_error_returns_domain_error(self) -> None:
        solver = Solver()

        result = solver.solve_or_error(G3_MATRIX)

        assert isinstance(result, ErrorResponse)
        assert result.error.code == DOMAIN_NO_MAGIC_ASSIGNMENT_CODE

    def test_d_sol_blank_count_not_two_raises(self) -> None:
        solver = Solver()
        matrix = [row[:] for row in G0_MATRIX]

        with pytest.raises(UnsolvableDomainError):
            solver.solve(matrix)

    def test_d_sol_04_g1_result_length_six(self) -> None:
        solver = Solver()

        result = solver.solve(G1_MATRIX)

        assert isinstance(result, list)
        assert len(result) == 6
