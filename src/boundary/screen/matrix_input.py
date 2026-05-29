"""Read 4x4 matrix from screen cell entries."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class MatrixReadError(Exception):
    """Cell value cannot be parsed as 0 or 1..16."""


def read_matrix_from_entries(
    entries: list[list[tk.Entry]],
) -> list[list[int]]:
    """Parse grid entries: empty or '0' -> 0; otherwise int in 0..16."""
    matrix: list[list[int]] = []
    for row_entries in entries:
        row: list[int] = []
        for entry in row_entries:
            text = entry.get().strip()
            if text == "" or text == "0":
                row.append(0)
                continue
            try:
                value = int(text)
            except ValueError as exc:
                raise MatrixReadError(f"Invalid cell value: {text!r}") from exc
            row.append(value)
        matrix.append(row)
    return matrix


def set_matrix_in_entries(
    entries: list[list[tk.Entry]],
    matrix: list[list[int]],
) -> None:
    for row_idx, row_entries in enumerate(entries):
        for col_idx, entry in enumerate(row_entries):
            value = matrix[row_idx][col_idx]
            entry.delete(0, tk.END)
            if value == 0:
                entry.insert(0, "0")
            else:
                entry.insert(0, str(value))


def create_matrix_entry_grid(parent: ttk.Frame) -> list[list[tk.Entry]]:
    entries: list[list[tk.Entry]] = []
    for _row in range(4):
        row_entries: list[tk.Entry] = []
        for _col in range(4):
            entry = ttk.Entry(parent, width=4, justify="center")
            entry.grid(row=_row, column=_col, padx=2, pady=2)
            row_entries.append(entry)
        entries.append(row_entries)
    return entries
