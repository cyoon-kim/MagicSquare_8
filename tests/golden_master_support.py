"""Approve-pattern utilities for Magic Square Golden Master tests (GM-1)."""

from __future__ import annotations

import difflib
from pathlib import Path

from boundary.boundary_validator import BoundaryValidator
from boundary.models import ErrorResponse
from boundary.result_formatter import ResultFormatter
from control.solve_magic_square_use_case import SolveMagicSquareUseCase
from entity.blank_finder import BlankFinder
from entity.magic_square_validator import MagicSquareValidator
from entity.missing_number_finder import MissingNumberFinder
from entity.solver import Solver

from golden_master_scenarios import GOLDEN_MASTER_SCENARIOS, GoldenMasterScenario

DEFAULT_GOLDEN_MASTER_PATH = (
    Path(__file__).resolve().parent / "golden_master_expected.txt"
)
SECTION_SEPARATOR = "________________________________________"


def build_use_case() -> SolveMagicSquareUseCase:
    """Real orchestration stack for end-to-end golden master capture."""
    return SolveMagicSquareUseCase(
        boundary_validator=BoundaryValidator(),
        blank_finder=BlankFinder(),
        missing_number_finder=MissingNumberFinder(),
        magic_square_validator=MagicSquareValidator(),
        solver=Solver(),
        result_formatter=ResultFormatter(),
    )


def format_grid(grid: list[list[int]]) -> str:
    """Render a 4×4 grid as space-separated rows for golden master files."""
    return "\n".join(" ".join(str(cell) for cell in row) for row in grid)


def format_output_data(data: list[int]) -> str:
    """Serialize success ``int[6]`` in canonical comma-separated form."""
    return "[" + ",".join(str(value) for value in data) + "]"


def serialize_result(result: list[int] | ErrorResponse) -> str:
    """Serialize UseCase result DTO to golden master Output/Error block body."""
    if isinstance(result, ErrorResponse):
        return f"Error:\n{result.error.code}"
    return f"Output:\n{format_output_data(result)}"


def capture_scenario_section(
    use_case: SolveMagicSquareUseCase, scenario: GoldenMasterScenario
) -> str:
    """Capture one scenario's Input/Output or Input/Error block."""
    input_block = f"Input:\n{format_grid(scenario.grid)}"
    result = use_case.execute(scenario.grid)
    return f"{input_block}\n{serialize_result(result)}"


def build_golden_master_document(use_case: SolveMagicSquareUseCase) -> str:
    """Build the full golden master expected file from all scenarios."""
    sections: list[str] = []
    for index, scenario in enumerate(GOLDEN_MASTER_SCENARIOS):
        body = capture_scenario_section(use_case, scenario)
        sections.append(f"[{scenario.name}]\n{body}")
        if index < len(GOLDEN_MASTER_SCENARIOS) - 1:
            sections.append(SECTION_SEPARATOR)
    return "\n\n".join(sections) + "\n"


def approve_golden_master(
    actual: str,
    expected_path: Path,
    *,
    auto_create: bool = True,
    force_update: bool = False,
) -> str:
    """Compare or create golden master baseline using the approve pattern.

    Returns ``"matched"``, ``"created"``, or ``"updated"``.
    Raises ``AssertionError`` with unified diff on mismatch.
    """
    existed = expected_path.exists()
    if force_update or (not existed and auto_create):
        expected_path.write_text(actual, encoding="utf-8")
        if force_update and existed:
            return "updated"
        return "created"

    if not expected_path.exists():
        raise FileNotFoundError(
            f"Golden master baseline not found: {expected_path}. "
            "Run with --approve-golden or scripts/generate_golden_master.py."
        )

    expected = expected_path.read_text(encoding="utf-8")
    if actual == expected:
        return "matched"

    diff = difflib.unified_diff(
        expected.splitlines(keepends=True),
        actual.splitlines(keepends=True),
        fromfile=str(expected_path),
        tofile="actual",
    )
    raise AssertionError(
        "Golden master mismatch — run approve to update baseline:\n"
        + "".join(diff)
    )
