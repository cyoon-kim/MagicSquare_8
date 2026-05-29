"""NFR-04 — input matrix must remain unchanged after UseCase execute (BR-14)."""

from __future__ import annotations

import copy

import pytest

from control.factory import build_solve_magic_square_use_case
from control.solve_magic_square_use_case import SolveMagicSquareUseCase
from grids import G1_MATRIX, G3_MATRIX


def _build_use_case() -> SolveMagicSquareUseCase:
    return build_solve_magic_square_use_case()


@pytest.mark.control
@pytest.mark.p0
class TestNfr04MatrixImmutability:
    """FR-06 — execute must not mutate the input matrix (success or failure)."""

    def test_nfr_04_success_path_matrix_unchanged(self) -> None:
        """NFR-04 / EX-09 — G1 success leaves original matrix intact."""
        use_case = _build_use_case()
        matrix = copy.deepcopy(G1_MATRIX)
        snapshot = copy.deepcopy(matrix)

        use_case.execute(matrix)

        assert matrix == snapshot

    def test_nfr_04_failure_path_matrix_unchanged(self) -> None:
        """NFR-04 / EX-09 — G3 failure leaves original matrix intact."""
        use_case = _build_use_case()
        matrix = copy.deepcopy(G3_MATRIX)
        snapshot = copy.deepcopy(matrix)

        use_case.execute(matrix)

        assert matrix == snapshot
