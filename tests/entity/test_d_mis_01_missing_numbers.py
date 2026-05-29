"""Track B — D-MIS-01 missing numbers RED skeleton (FR-03).

Domain Mock forbidden.
"""

from __future__ import annotations

import pytest

# from entity.missing_number_finder import MissingNumberFinder
# from entity.services.missing_number_finder import find_not_exist_nums


@pytest.mark.domain
@pytest.mark.p0
class TestDMis01MissingNumbers:
    """D-MIS-01 — missing set {7, 10} ascending on G1."""

    def test_d_mis_01_g1_missing_numbers_sorted(self) -> None:
        """D-MIS-01 — G1 missing numbers [7, 10]."""
        # Given: G1_MATRIX
        # finder = MissingNumberFinder()
        # When: finder.find(g1_matrix)
        # Then (Full RED): [7, 10] or {7, 10}
        pytest.fail("RED: D-MIS-01 — G1 missing numbers {7, 10} ascending")
