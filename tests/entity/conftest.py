"""Track B grid fixtures — G0~G3 placeholders (Report/09 SSOT).

Uncomment matrix literals when promoting skeleton to Full RED.
"""

from __future__ import annotations

# import pytest

# G0 — complete 4x4 magic square (no zeros), M=34
# G0_MATRIX: list[list[int]] = [
#     [16, 3, 2, 13],
#     [5, 10, 11, 8],
#     [9, 6, 7, 12],
#     [4, 15, 14, 1],
# ]

# G1 — blanks 1-index (2,2), (3,3); missing {7, 10}
# G1_MATRIX: list[list[int]] = [
#     [16, 3, 2, 13],
#     [5, 0, 11, 8],
#     [9, 6, 0, 12],
#     [4, 15, 14, 1],
# ]

# G2 — PRD TD-02 (Step A fail, Step B success); TBD in Report/09 finalize
# G2_MATRIX: list[list[int]] = [
#     [0, 0, 2, 13],
#     [5, 10, 11, 8],
#     [9, 6, 7, 12],
#     [4, 15, 14, 1],
# ]

# G3 — PRD TD-07 (dual assignment fail)
# G3_MATRIX: list[list[int]] = [
#     [14, 1, 5, 9],
#     [8, 7, 16, 12],
#     [6, 10, 2, 11],
#     [0, 13, 4, 0],
# ]

# @pytest.fixture
# def grid_g0() -> list[list[int]]:
#     return [row[:] for row in G0_MATRIX]

# @pytest.fixture
# def grid_g1() -> list[list[int]]:
#     return [row[:] for row in G1_MATRIX]
