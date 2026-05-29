"""NFR-04 — input matrix must remain unchanged after UseCase execute (BR-14)."""

from __future__ import annotations

import copy

import pytest

from control.solve_magic_square_use_case import SolveMagicSquareUseCase
from grids import G1_MATRIX, G3_MATRIX


@pytest.mark.control
@pytest.mark.p0
class TestNfr04MatrixImmutability:
    """FR-06 — execute must not mutate the input matrix (success or failure)."""

    def test_nfr_04_success_path_matrix_unchanged(
        self,
        solve_use_case: SolveMagicSquareUseCase,
    ) -> None:
        """NFR-04 / EX-09 — G1 success leaves original matrix intact."""
        matrix = copy.deepcopy(G1_MATRIX)
        snapshot = copy.deepcopy(matrix)

        solve_use_case.execute(matrix)

        assert matrix == snapshot

    def test_nfr_04_failure_path_matrix_unchanged(
        self,
        solve_use_case: SolveMagicSquareUseCase,
    ) -> None:
        """NFR-04 / EX-09 — G3 failure leaves original matrix intact."""
        matrix = copy.deepcopy(G3_MATRIX)
        snapshot = copy.deepcopy(matrix)

        solve_use_case.execute(matrix)

        assert matrix == snapshot
