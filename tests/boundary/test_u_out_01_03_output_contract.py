"""Track A — U-OUT-01~03 output contract (FR-05b / FR-06 success path)."""

from __future__ import annotations

import pytest

from control.solve_magic_square_use_case import SolveMagicSquareUseCase
from grids import G1_EXPECTED_STEP_A, G1_MATRIX


@pytest.mark.boundary
@pytest.mark.p0
class TestUOut01Through03OutputContract:
    """External int[6] success contract — length, 1-index coords, G1 payload."""

    def test_u_out_01_success_result_length_is_six(
        self,
        solve_use_case: SolveMagicSquareUseCase,
    ) -> None:
        result = solve_use_case.execute(G1_MATRIX)

        assert isinstance(result, list)
        assert len(result) == 6

    def test_u_out_02_coordinates_are_one_indexed_in_range(
        self,
        solve_use_case: SolveMagicSquareUseCase,
    ) -> None:
        result = solve_use_case.execute(G1_MATRIX)

        assert isinstance(result, list)
        for idx in (0, 1, 3, 4):
            assert 1 <= result[idx] <= 4

    def test_u_out_03_g1_step_a_success_payload(
        self,
        solve_use_case: SolveMagicSquareUseCase,
    ) -> None:
        result = solve_use_case.execute(G1_MATRIX)

        assert result == G1_EXPECTED_STEP_A
