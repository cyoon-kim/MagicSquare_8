"""Track B — D-LOC-01 blank coordinate discovery (FR-02)."""

from __future__ import annotations

import pytest

from entity.blank_finder import BlankFinder
from grids import G1_MATRIX


@pytest.mark.domain
@pytest.mark.p0
class TestDLoc01BlankCoords:
    """D-LOC-01 — row-major blank positions on G1 (0-index)."""

    def test_d_loc_01_g1_row_major_blank_coords(self) -> None:
        finder = BlankFinder()

        result = finder.find(G1_MATRIX)

        assert result == [(0, 1), (0, 3)]
