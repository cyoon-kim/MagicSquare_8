"""Track B — D-SOL-01~04 two-cell solver (FR-05a)."""

from __future__ import annotations

import pytest

from boundary.models import (
    DOMAIN_BLANK_COUNT_CODE,
    DOMAIN_MISSING_COUNT_CODE,
    DOMAIN_NO_MAGIC_ASSIGNMENT_CODE,
    ErrorResponse,
)
from entity.solver import Solver
from grids import (
    G0_MATRIX,
    G1_EXPECTED_DOMAIN_STEP_A,
    G1_MATRIX,
    G2_EXPECTED_DOMAIN_STEP_B,
    G2_MATRIX,
    G3_MATRIX,
)


@pytest.mark.domain
@pytest.mark.p0
class TestDSol01Through04TwoCellSolver:
    """D-SOL — Solver.solve returns int[6] 0-index or ErrorResponse."""

    def test_d_sol_01_g1_step_a_success_int_six(self) -> None:
        solver = Solver()

        result = solver.solve(G1_MATRIX)

        assert result == G1_EXPECTED_DOMAIN_STEP_A

    def test_d_sol_02_g2_step_b_reverse_success(self) -> None:
        solver = Solver()

        result = solver.solve(G2_MATRIX)

        assert result == G2_EXPECTED_DOMAIN_STEP_B

    def test_d_sol_03_g3_dual_fail_returns_domain_error(self) -> None:
        solver = Solver()

        result = solver.solve(G3_MATRIX)

        assert isinstance(result, ErrorResponse)
        assert result.error.code == DOMAIN_NO_MAGIC_ASSIGNMENT_CODE

    def test_d_sol_blank_count_returns_domain_blank_count_error(self) -> None:
        solver = Solver()
        matrix = [row[:] for row in G0_MATRIX]

        result = solver.solve(matrix)

        assert isinstance(result, ErrorResponse)
        assert result.error.code == DOMAIN_BLANK_COUNT_CODE

    def test_d_sol_missing_count_returns_domain_missing_count_error(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        solver = Solver()
        monkeypatch.setattr(
            solver._missing_finder,
            "find",
            lambda _matrix: [3],
        )

        result = solver.solve(G1_MATRIX)

        assert isinstance(result, ErrorResponse)
        assert result.error.code == DOMAIN_MISSING_COUNT_CODE

    def test_d_sol_04_g1_result_length_six(self) -> None:
        solver = Solver()

        result = solver.solve(G1_MATRIX)

        assert isinstance(result, list)
        assert len(result) == 6
