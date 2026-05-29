"""Track B grid fixtures — G0~G3 (PRD TD / Report/09 SSOT)."""

from __future__ import annotations

import pytest

from grids import G0_MATRIX, G1_MATRIX, G2_MATRIX, G3_MATRIX

__all__ = ["G0_MATRIX", "G1_MATRIX", "G2_MATRIX", "G3_MATRIX"]


@pytest.fixture
def grid_g0() -> list[list[int]]:
    return [row[:] for row in G0_MATRIX]


@pytest.fixture
def grid_g1() -> list[list[int]]:
    return [row[:] for row in G1_MATRIX]


@pytest.fixture
def grid_g2() -> list[list[int]]:
    return [row[:] for row in G2_MATRIX]


@pytest.fixture
def grid_g3() -> list[list[int]]:
    return [row[:] for row in G3_MATRIX]
