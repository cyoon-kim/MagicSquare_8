"""Golden Master input scenarios for Magic Square Solver (GM-1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from grids import G0_MATRIX, G1_MATRIX, G2_MATRIX, G3_MATRIX

CombinationRule = Literal["small_first", "reverse"]


@dataclass(frozen=True)
class GoldenMasterScenario:
    """Single scenario definition for golden master capture.

    Attributes:
        test_case_id: Traceability ID (GM-TC-01 … GM-TC-05).
        name: Section key used in ``golden_master_expected.txt``.
        grid: 4×4 integer matrix passed to ``SolveMagicSquareUseCase.execute``.
        description: Human-readable note for design docs.
        expected_error_code: PRD §13 code when the scenario must fail.
        combination_rule: Success-path solver rule under verification.
    """

    test_case_id: str
    name: str
    grid: list[list[int]]
    description: str
    expected_error_code: str | None = None
    combination_rule: CombinationRule | None = None


GOLDEN_MASTER_SCENARIOS: tuple[GoldenMasterScenario, ...] = (
    GoldenMasterScenario(
        test_case_id="GM-TC-01",
        name="normal_success",
        grid=G1_MATRIX,
        description="PRD TD-01 / G1 — small-first (Attempt 1) success",
        combination_rule="small_first",
    ),
    GoldenMasterScenario(
        test_case_id="GM-TC-02",
        name="reverse_success",
        grid=G2_MATRIX,
        description="PRD TD-02 / G2 — Attempt 1 fails, Attempt 2 reverse success",
        combination_rule="reverse",
    ),
    GoldenMasterScenario(
        test_case_id="GM-TC-03",
        name="invalid_blank_count",
        grid=G0_MATRIX,
        description="Complete grid with zero blanks — INPUT_BLANK_COUNT_INVALID",
        expected_error_code="INPUT_BLANK_COUNT_INVALID",
    ),
    GoldenMasterScenario(
        test_case_id="GM-TC-04",
        name="duplicate_number",
        grid=[
            [16, 3, 2, 13],
            [5, 0, 11, 8],
            [9, 6, 0, 12],
            [4, 15, 14, 8],
        ],
        description="Duplicate non-zero value — INPUT_DUPLICATE_NON_ZERO",
        expected_error_code="INPUT_DUPLICATE_NON_ZERO",
    ),
    GoldenMasterScenario(
        test_case_id="GM-TC-05",
        name="no_valid_solution",
        grid=G3_MATRIX,
        description="Both combinations invalid — DOMAIN_NO_MAGIC_ASSIGNMENT",
        expected_error_code="DOMAIN_NO_MAGIC_ASSIGNMENT",
    ),
)

SCENARIO_BY_TEST_CASE_ID: dict[str, GoldenMasterScenario] = {
    scenario.test_case_id: scenario for scenario in GOLDEN_MASTER_SCENARIOS
}
