"""BlankFinder — FR-02 blank coordinate discovery."""

from __future__ import annotations


class BlankFinder:
    """Returns blank cell coordinates in row-major order (0-index)."""

    def find(self, matrix: list[list[int]]) -> list[tuple[int, int]]:
        """Return blank coordinates in row-major order (0-index).

        Args:
            matrix: Domain grid containing zero placeholders.

        Returns:
            List of ``(row, col)`` tuples for each blank cell.
        """
        coords: list[tuple[int, int]] = []
        for row_idx, row in enumerate(matrix):
            for col_idx, cell in enumerate(row):
                if cell == 0:
                    coords.append((row_idx, col_idx))
        return coords
