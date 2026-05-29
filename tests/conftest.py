"""Pytest configuration for local src and legacy imports."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT: Path = Path(__file__).resolve().parents[1]
SRC_PATH: Path = ROOT / "src"
LEGACY_PATH: Path = ROOT / "legacy"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

if str(LEGACY_PATH) not in sys.path:
    sys.path.insert(0, str(LEGACY_PATH))

# AC-FR-01-01 expected contract (PRD §8.1) — test-side constants until boundary exists
INVALID_SIZE_CODE: str = "INVALID_SIZE"
INVALID_SIZE_MESSAGE: str = "Grid must be 4x4."


@pytest.fixture
def invalid_size_code() -> str:
    """Expected error code for AC-FR-01-01 size violations."""
    return INVALID_SIZE_CODE


@pytest.fixture
def invalid_size_message() -> str:
    """Expected error message for AC-FR-01-01 (PRD §8.1)."""
    return INVALID_SIZE_MESSAGE


@pytest.fixture
def grid_3x4() -> list[list[int]]:
    """3 rows × 4 columns — invalid for 4×4 contract."""
    return [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
