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

from golden_master_scenarios import (
    GOLDEN_MASTER_SCENARIOS,
    GoldenMasterScenario,
)

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


def format_scenario_document(scenario: GoldenMasterScenario, body: str) -> str:
    """Wrap a scenario body with its section header."""
    return f"[{scenario.name}]\n{body}"


def build_golden_master_document(use_case: SolveMagicSquareUseCase) -> str:
    """Build the full golden master expected file from all scenarios."""
    sections: list[str] = []
    for index, scenario in enumerate(GOLDEN_MASTER_SCENARIOS):
        body = capture_scenario_section(use_case, scenario)
        sections.append(format_scenario_document(scenario, body))
        if index < len(GOLDEN_MASTER_SCENARIOS) - 1:
            sections.append(SECTION_SEPARATOR)
    return "\n\n".join(sections) + "\n"


def parse_golden_master_sections(content: str) -> dict[str, str]:
    """Parse ``golden_master_expected.txt`` into section-name → body map."""
    sections: dict[str, str] = {}
    normalized = content.strip()
    if not normalized:
        return sections

    blocks = normalized.split(f"\n\n{SECTION_SEPARATOR}\n\n")
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        lines = block.splitlines()
        header = lines[0].strip()
        if not (header.startswith("[") and header.endswith("]")):
            raise ValueError(f"Invalid golden master section header: {header!r}")
        name = header[1:-1]
        body = "\n".join(lines[1:]).strip("\n")
        sections[name] = body
    return sections


def load_expected_section(expected_path: Path, section_name: str) -> str | None:
    """Load one scenario body from the baseline file."""
    if not expected_path.exists():
        return None
    return parse_golden_master_sections(
        expected_path.read_text(encoding="utf-8")
    ).get(section_name)


def format_unified_diff(expected: str, actual: str) -> str:
    """Render --- expected / +++ actual unified diff for failure output."""
    diff_lines = difflib.unified_diff(
        expected.splitlines(keepends=True),
        actual.splitlines(keepends=True),
        fromfile="expected",
        tofile="actual",
    )
    return "".join(diff_lines)


def assert_golden_master_match(
    expected: str,
    actual: str,
    *,
    context: str,
) -> None:
    """Compare strings and raise with unified diff on mismatch."""
    if expected == actual:
        return
    diff = format_unified_diff(expected, actual)
    raise AssertionError(
        f"Golden master mismatch ({context}) — run approve to update baseline:\n"
        f"{diff}"
    )


def approve_golden_master(
    actual: str,
    expected_path: Path,
    *,
    auto_create: bool = True,
    force_update: bool = False,
) -> str:
    """Compare or create golden master baseline using the approve pattern."""
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
    assert_golden_master_match(
        expected,
        actual,
        context=str(expected_path),
    )
    return "matched"


def approve_scenario_section(
    actual_body: str,
    expected_path: Path,
    scenario: GoldenMasterScenario,
    use_case: SolveMagicSquareUseCase,
    *,
    auto_create: bool = True,
    force_update: bool = False,
) -> str:
    """Compare one scenario against baseline; refresh full file on approve."""
    expected_body = load_expected_section(expected_path, scenario.name)

    if force_update or (expected_body is None and auto_create):
        document = build_golden_master_document(use_case)
        expected_path.write_text(document, encoding="utf-8")
        return "updated" if expected_body is not None else "created"

    if expected_body is None:
        raise FileNotFoundError(
            f"Golden master section [{scenario.name}] not found in {expected_path}."
        )

    assert_golden_master_match(
        expected_body,
        actual_body,
        context=f"{scenario.test_case_id} [{scenario.name}]",
    )
    return "matched"


def assert_int6_output_contract(result: list[int]) -> None:
    """Verify FR-05b external ``int[6]`` shape and 1-index coordinate range."""
    assert isinstance(result, list), "Success result must be list[int]"
    assert len(result) == 6, "Success result must have length 6"
    for index in (0, 1, 3, 4):
        assert 1 <= result[index] <= 4, (
            f"Coordinate at index {index} must be 1-index in 1..4, got {result[index]}"
        )


def assert_row_major_blank_order(
    grid: list[list[int]], result: list[int]
) -> None:
    """Verify blank coordinates follow row-major order (BR-05)."""
    blanks = BlankFinder().find(grid)
    assert len(blanks) == 2
    (row0, col0), (row1, col1) = blanks
    assert result[0] == row0 + 1 and result[1] == col0 + 1
    assert result[3] == row1 + 1 and result[4] == col1 + 1


def assert_small_first_combination(
    grid: list[list[int]], result: list[int]
) -> None:
    """Verify Attempt 1: smaller missing number → first blank (BR-10)."""
    missing = MissingNumberFinder().find(grid)
    blanks = BlankFinder().find(grid)
    assert len(missing) == 2 and len(blanks) == 2
    small, large = missing[0], missing[1]
    (row0, col0), (row1, col1) = blanks
    assert result == [row0 + 1, col0 + 1, small, row1 + 1, col1 + 1, large]


def assert_reverse_fallback_combination(
    grid: list[list[int]], result: list[int]
) -> None:
    """Verify Attempt 2: reverse order succeeds when small-first fails (BR-11)."""
    missing = MissingNumberFinder().find(grid)
    blanks = BlankFinder().find(grid)
    assert len(missing) == 2 and len(blanks) == 2
    small, large = missing[0], missing[1]
    (row0, col0), (row1, col1) = blanks

    small_first = [row0 + 1, col0 + 1, small, row1 + 1, col1 + 1, large]
    reverse = [row0 + 1, col0 + 1, large, row1 + 1, col1 + 1, small]
    assert result == reverse
    assert result != small_first

    candidate_small_first = _apply_assignment(grid, blanks, small, large)
    assert not MagicSquareValidator().is_valid(candidate_small_first)


def assert_error_contract(result: ErrorResponse, expected_code: str) -> None:
    """Verify PRD §13 ErrorResponse schema and machine-readable code."""
    assert isinstance(result, ErrorResponse)
    assert result.error.code == expected_code
    assert isinstance(result.error.message, str) and result.error.message


def assert_scenario_contracts(
    scenario: GoldenMasterScenario,
    result: list[int] | ErrorResponse,
) -> None:
    """Apply domain/boundary contract checks before golden master compare."""
    if scenario.expected_error_code is not None:
        assert isinstance(result, ErrorResponse)
        assert_error_contract(result, scenario.expected_error_code)
        return

    assert isinstance(result, list)
    assert_int6_output_contract(result)
    assert_row_major_blank_order(scenario.grid, result)

    if scenario.combination_rule == "small_first":
        assert_small_first_combination(scenario.grid, result)
    elif scenario.combination_rule == "reverse":
        assert_reverse_fallback_combination(scenario.grid, result)


def _apply_assignment(
    matrix: list[list[int]],
    blanks: list[tuple[int, int]],
    first_value: int,
    second_value: int,
) -> list[list[int]]:
    """Build candidate grid for combination rule verification."""
    from copy import deepcopy

    (row0, col0), (row1, col1) = blanks
    candidate = deepcopy(matrix)
    candidate[row0][col0] = first_value
    candidate[row1][col1] = second_value
    return candidate


def run_scenario_golden_master(
    use_case: SolveMagicSquareUseCase,
    scenario: GoldenMasterScenario,
    expected_path: Path,
    *,
    approve_golden: bool,
) -> str:
    """Execute contract checks and approve-pattern section compare."""
    result = use_case.execute(scenario.grid)
    assert_scenario_contracts(scenario, result)

    actual_body = capture_scenario_section(use_case, scenario)
    return approve_scenario_section(
        actual_body,
        expected_path,
        scenario,
        use_case,
        auto_create=True,
        force_update=approve_golden,
    )
