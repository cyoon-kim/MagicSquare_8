"""Shared test grids G0~G3 (PRD TD SSOT)."""

from __future__ import annotations

G0_MATRIX: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

# PRD TD-01 — small-first Step A (blanks 0-index (0,1), (0,3); missing [3, 13])
G1_MATRIX: list[list[int]] = [
    [16, 0, 2, 0],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

G2_MATRIX: list[list[int]] = [
    [0, 0, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

G3_MATRIX: list[list[int]] = [
    [14, 1, 5, 9],
    [8, 7, 16, 12],
    [6, 10, 2, 11],
    [0, 13, 4, 0],
]

G1_EXPECTED_STEP_A: list[int] = [1, 2, 3, 1, 4, 13]
G1_EXPECTED_DOMAIN_STEP_A: list[int] = [0, 1, 3, 0, 3, 13]
G2_EXPECTED_DOMAIN_STEP_B: list[int] = [0, 0, 16, 0, 1, 3]
