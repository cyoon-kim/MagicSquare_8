"""Track B — D-MIS-01 missing numbers (FR-03)."""

from __future__ import annotations

import pytest

from entity.missing_number_finder import MissingNumberFinder
from grids import G1_MATRIX


@pytest.mark.domain
@pytest.mark.p0
class TestDMis01MissingNumbers:
    """D-MIS-01 — missing set {7, 10} ascending on G1."""

    def test_d_mis_01_g1_missing_numbers_sorted(self) -> None:
        finder = MissingNumberFinder()

        result = finder.find(G1_MATRIX)

        assert result == [3, 13]
