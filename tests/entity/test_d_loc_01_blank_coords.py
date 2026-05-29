"""Track B — D-LOC-01 blank coordinate discovery RED skeleton (FR-02).

Domain Mock forbidden.
"""

from __future__ import annotations

import pytest

# from entity.blank_finder import BlankFinder
# from entity.services.blank_locator import find_blank_coords


@pytest.mark.domain
@pytest.mark.p0
class TestDLoc01BlankCoords:
    """D-LOC-01 — row-major blank positions on G1 (0-index)."""

    def test_d_loc_01_g1_row_major_blank_coords(self) -> None:
        """D-LOC-01 — G1 blanks at (1,1) and (2,2) 0-index."""
        # Given: G1_MATRIX from tests/entity/conftest.py
        # finder = BlankFinder()
        # When: finder.find(g1_matrix)  # or find_blank_coords(g1_matrix)
        # Then (Full RED): [(1, 1), (2, 2)]
        pytest.fail("RED: D-LOC-01 — G1 row-major blanks [(1,1), (2,2)] 0-index")
