"""Golden Master input scenarios for Magic Square Solver (GM-1)."""

from __future__ import annotations

from dataclasses import dataclass

from grids import G0_MATRIX, G2_MATRIX, G3_MATRIX


@dataclass(frozen=True)
class GoldenMasterScenario:
    """Single scenario definition for golden master capture.

    Attributes:
        name: Section key used in ``golden_master_expected.txt``.
        grid: 4×4 integer matrix passed to ``SolveMagicSquareUseCase.execute``.
        description: Human-readable note for design docs.
    """

    name: str
    grid: list[list[int]]
    description: str


# Step B-only success — small-first fails, reverse succeeds
_GRID_NORMAL_SUCCESS = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 0],
]

# PRD TD-02 / G2 — Attempt 1 fails, Attempt 2 (reverse) succeeds
_GRID_REVERSE_SUCCESS = G2_MATRIX

# PRD G0 — zero empty cells → INPUT_BLANK_COUNT_INVALID
_GRID_INVALID_BLANK_COUNT = G0_MATRIX

# U-IN-06 — duplicate non-zero value → INPUT_DUPLICATE_NON_ZERO
_GRID_DUPLICATE_NUMBER = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 8],
]

# PRD G3 — both combinations invalid → DOMAIN_NO_MAGIC_ASSIGNMENT
_GRID_NO_VALID_SOLUTION = G3_MATRIX

GOLDEN_MASTER_SCENARIOS: tuple[GoldenMasterScenario, ...] = (
    GoldenMasterScenario(
        name="normal_success",
        grid=_GRID_NORMAL_SUCCESS,
        description="Valid partial grid — reverse combination success",
    ),
    GoldenMasterScenario(
        name="reverse_success",
        grid=_GRID_REVERSE_SUCCESS,
        description="PRD TD-02 / G2 — Attempt 2 reverse path success",
    ),
    GoldenMasterScenario(
        name="invalid_blank_count",
        grid=_GRID_INVALID_BLANK_COUNT,
        description="Complete grid with zero blanks — INPUT_BLANK_COUNT_INVALID",
    ),
    GoldenMasterScenario(
        name="duplicate_number",
        grid=_GRID_DUPLICATE_NUMBER,
        description="Duplicate non-zero value — INPUT_DUPLICATE_NON_ZERO",
    ),
    GoldenMasterScenario(
        name="no_valid_solution",
        grid=_GRID_NO_VALID_SOLUTION,
        description="Both combinations invalid — DOMAIN_NO_MAGIC_ASSIGNMENT",
    ),
)
