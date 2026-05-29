"""GM-1 — Magic Square Solver Golden Master regression test."""

from __future__ import annotations

from pathlib import Path

import pytest

from golden_master_support import (
    DEFAULT_GOLDEN_MASTER_PATH,
    approve_golden_master,
    build_golden_master_document,
    build_use_case,
)
from control.solve_magic_square_use_case import SolveMagicSquareUseCase


@pytest.fixture
def golden_master_use_case() -> SolveMagicSquareUseCase:
    """Real UseCase stack for end-to-end output capture."""
    return build_use_case()


@pytest.mark.p0
class TestGoldenMasterMagicSquare:
    """GM-1 — approve-pattern regression against ``golden_master_expected.txt``."""

    def test_gm_01_solver_output_matches_golden_master(
        self,
        golden_master_use_case: SolveMagicSquareUseCase,
        golden_master_path: Path,
        approve_golden: bool,
    ) -> None:
        """GM-1 — capture UseCase DTO output and compare to baseline."""
        actual = build_golden_master_document(golden_master_use_case)

        status = approve_golden_master(
            actual,
            golden_master_path,
            auto_create=True,
            force_update=approve_golden,
        )

        assert status in {"matched", "created", "updated"}
