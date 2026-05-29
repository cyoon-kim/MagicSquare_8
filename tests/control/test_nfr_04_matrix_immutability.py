"""NFR-04 — input matrix must remain unchanged after UseCase execute (BR-14)."""

from __future__ import annotations

import copy

import pytest

from boundary.boundary_validator import BoundaryValidator
from boundary.result_formatter import ResultFormatter
from control.solve_magic_square_use_case import SolveMagicSquareUseCase
from entity.blank_finder import BlankFinder
from entity.magic_square_validator import MagicSquareValidator
from entity.missing_number_finder import MissingNumberFinder
from entity.solver import Solver
from grids import G1_MATRIX, G3_MATRIX


def _build_use_case() -> SolveMagicSquareUseCase:
    return SolveMagicSquareUseCase(
        boundary_validator=BoundaryValidator(),
        blank_finder=BlankFinder(),
        missing_number_finder=MissingNumberFinder(),
        magic_square_validator=MagicSquareValidator(),
        solver=Solver(),
        result_formatter=ResultFormatter(),
    )


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
