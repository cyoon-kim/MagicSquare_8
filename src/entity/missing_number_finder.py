"""MissingNumberFinder — FR-03 missing number set."""

from __future__ import annotations

from entity.constants import MAX_CELL_VALUE, MIN_CELL_VALUE


class MissingNumberFinder:
    """Returns missing values from 1..16 not present in matrix (ascending)."""

    def find(self, matrix: list[list[int]]) -> list[int]:
        """Return missing values from 1..16 not present in the grid.

        Args:
            matrix: Domain grid (may contain zeros).

        Returns:
            Ascending list of missing cell values.
        """
        present = {cell for row in matrix for cell in row if cell != 0}
        return [
            value
            for value in range(MIN_CELL_VALUE, MAX_CELL_VALUE + 1)
            if value not in present
        ]
