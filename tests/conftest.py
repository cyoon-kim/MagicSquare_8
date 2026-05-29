"""Pytest configuration for local src and legacy imports."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT: Path = Path(__file__).resolve().parents[1]
SRC_PATH: Path = ROOT / "src"
LEGACY_PATH: Path = ROOT / "legacy"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

if str(LEGACY_PATH) not in sys.path:
    sys.path.insert(0, str(LEGACY_PATH))
