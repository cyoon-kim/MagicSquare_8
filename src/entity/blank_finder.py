"""BlankFinder — FR-02 blank coordinate discovery."""

from __future__ import annotations


class BlankFinder:
    """Returns blank cell coordinates in row-major order (0-index)."""

    def find(self, matrix: list[list[int]]) -> list[tuple[int, int]]:
        coords: list[tuple[int, int]] = []
        for row_idx, row in enumerate(matrix):
            for col_idx, cell in enumerate(row):
                if cell == 0:
                    coords.append((row_idx, col_idx))
        return coords
