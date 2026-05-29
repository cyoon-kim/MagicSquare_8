"""GM-1 — Magic Square Solver Golden Master regression tests.

Run:
    pytest tests/test_gm_01_magic_square_golden_master.py -v
    pytest tests/test_gm_01_magic_square_golden_master.py --approve-golden -v
"""

from __future__ import annotations

from pathlib import Path

import pytest

from control.solve_magic_square_use_case import SolveMagicSquareUseCase
from golden_master_scenarios import SCENARIO_BY_TEST_CASE_ID, GoldenMasterScenario
from golden_master_support import (
    approve_golden_master,
    build_golden_master_document,
    build_use_case,
    run_scenario_golden_master,
)


@pytest.fixture
def golden_master_use_case() -> SolveMagicSquareUseCase:
    """Real UseCase stack for end-to-end output capture."""
    return build_use_case()


def _assert_scenario(
    scenario: GoldenMasterScenario,
    golden_master_use_case: SolveMagicSquareUseCase,
    golden_master_path: Path,
    approve_golden: bool,
) -> None:
    status = run_scenario_golden_master(
        golden_master_use_case,
        scenario,
        golden_master_path,
        approve_golden=approve_golden,
    )
    assert status in {"matched", "created", "updated"}


@pytest.mark.golden_master
@pytest.mark.p0
class TestGoldenMasterMagicSquare:
    """GM-1 — approve-pattern regression against ``golden_master_expected.txt``."""

    def test_gm_tc_01_normal_combination_success(
        self,
        golden_master_use_case: SolveMagicSquareUseCase,
        golden_master_path: Path,
        approve_golden: bool,
    ) -> None:
        """GM-TC-01 — small-first combination success, int[6] 1-index contract."""
        _assert_scenario(
            SCENARIO_BY_TEST_CASE_ID["GM-TC-01"],
            golden_master_use_case,
            golden_master_path,
            approve_golden,
        )

    def test_gm_tc_02_reverse_combination_success(
        self,
        golden_master_use_case: SolveMagicSquareUseCase,
        golden_master_path: Path,
        approve_golden: bool,
    ) -> None:
        """GM-TC-02 — reverse fallback success after small-first failure."""
        _assert_scenario(
            SCENARIO_BY_TEST_CASE_ID["GM-TC-02"],
            golden_master_use_case,
            golden_master_path,
            approve_golden,
        )

    def test_gm_tc_03_invalid_blank_count(
        self,
        golden_master_use_case: SolveMagicSquareUseCase,
        golden_master_path: Path,
        approve_golden: bool,
    ) -> None:
        """GM-TC-03 — INPUT_BLANK_COUNT_INVALID error contract."""
        _assert_scenario(
            SCENARIO_BY_TEST_CASE_ID["GM-TC-03"],
            golden_master_use_case,
            golden_master_path,
            approve_golden,
        )

    def test_gm_tc_04_duplicate_number(
        self,
        golden_master_use_case: SolveMagicSquareUseCase,
        golden_master_path: Path,
        approve_golden: bool,
    ) -> None:
        """GM-TC-04 — INPUT_DUPLICATE_NON_ZERO error contract."""
        _assert_scenario(
            SCENARIO_BY_TEST_CASE_ID["GM-TC-04"],
            golden_master_use_case,
            golden_master_path,
            approve_golden,
        )

    def test_gm_tc_05_no_valid_magic_square(
        self,
        golden_master_use_case: SolveMagicSquareUseCase,
        golden_master_path: Path,
        approve_golden: bool,
    ) -> None:
        """GM-TC-05 — DOMAIN_NO_MAGIC_ASSIGNMENT error contract."""
        _assert_scenario(
            SCENARIO_BY_TEST_CASE_ID["GM-TC-05"],
            golden_master_use_case,
            golden_master_path,
            approve_golden,
        )

    def test_gm_full_baseline_document(
        self,
        golden_master_use_case: SolveMagicSquareUseCase,
        golden_master_path: Path,
        approve_golden: bool,
    ) -> None:
        """GM-1 — full ``golden_master_expected.txt`` holistic regression."""
        actual = build_golden_master_document(golden_master_use_case)
        status = approve_golden_master(
            actual,
            golden_master_path,
            auto_create=True,
            force_update=approve_golden,
        )
        assert status in {"matched", "created", "updated"}
