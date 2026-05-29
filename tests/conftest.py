"""Pytest configuration for local src and legacy imports."""

from __future__ import annotations

import sys

pytest_plugins = ["golden_master_conftest"]
import importlib.util
from pathlib import Path

import pytest

ROOT: Path = Path(__file__).resolve().parents[1]
SRC_PATH: Path = ROOT / "src"
TESTS_PATH: Path = Path(__file__).resolve().parent
LEGACY_PATH: Path = ROOT / "legacy"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

if str(TESTS_PATH) not in sys.path:
    sys.path.insert(0, str(TESTS_PATH))

if str(LEGACY_PATH) not in sys.path:
    sys.path.insert(0, str(LEGACY_PATH))

_constants_path = Path(__file__).resolve().parent / "constants.py"
_constants_spec = importlib.util.spec_from_file_location(
    "prd_test_constants",
    _constants_path,
)
_constants_mod = importlib.util.module_from_spec(_constants_spec)
assert _constants_spec.loader is not None
_constants_spec.loader.exec_module(_constants_mod)
INPUT_SIZE_INVALID_CODE = _constants_mod.INPUT_SIZE_INVALID_CODE
INPUT_SIZE_INVALID_MESSAGE = _constants_mod.INPUT_SIZE_INVALID_MESSAGE


@pytest.fixture
def input_size_invalid_code() -> str:
    """Expected error code for FR-01 AC-01."""
    return INPUT_SIZE_INVALID_CODE


@pytest.fixture
def input_size_invalid_message() -> str:
    """Expected error message for FR-01 AC-01 (PRD §13)."""
    return INPUT_SIZE_INVALID_MESSAGE


@pytest.fixture
def matrix_none() -> None:
    """BV-01: matrix not provided."""
    return None


@pytest.fixture
def matrix_empty() -> list[list[int]]:
    """BV-02: zero rows."""
    return []


@pytest.fixture
def matrix_four_empty_rows() -> list[list[int]]:
    """BV-03: four rows, zero columns each."""
    return [[], [], [], []]


@pytest.fixture
def matrix_3x4() -> list[list[int]]:
    """BV-04: three rows, four columns."""
    return [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]


@pytest.fixture
def matrix_4x3() -> list[list[int]]:
    """BV-05: four rows, three columns."""
    return [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]


@pytest.fixture
def matrix_5x5() -> list[list[int]]:
    """BV-06: five by five."""
    return [[0] * 5 for _ in range(5)]


@pytest.fixture
def matrix_td03_2x2() -> list[list[int]]:
    """TS-E-01 / TD-03: two by two."""
    return [[1, 2], [3, 4]]
