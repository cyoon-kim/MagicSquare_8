"""Magic Square 4x4 screen — ECB Boundary layer."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from boundary.models import ErrorResponse
from boundary.screen.matrix_input import (
    MatrixReadError,
    create_matrix_entry_grid,
    read_matrix_from_entries,
    set_matrix_in_entries,
)
from boundary.screen.samples import G0_COMPLETE_SAMPLE, G1_TD01_SAMPLE, G2_TD02_SAMPLE
from control.solve_magic_square_use_case import SolveMagicSquareUseCase


class MagicSquareWindow:
    """4x4 grid UI; delegates solve to Control use case only."""

    def __init__(self, use_case: SolveMagicSquareUseCase) -> None:
        self._use_case = use_case
        self._root = tk.Tk()
        self._root.title("Magic Square 4x4")
        self._root.resizable(False, False)

        main = ttk.Frame(self._root, padding=12)
        main.grid(row=0, column=0, sticky="nsew")

        ttk.Label(
            main,
            text="Enter 4x4 grid (0 = blank). Then Solve.",
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        grid_frame = ttk.LabelFrame(main, text="matrix", padding=8)
        grid_frame.grid(row=1, column=0, columnspan=2, pady=(0, 8))
        self._entries = create_matrix_entry_grid(grid_frame)

        btn_frame = ttk.Frame(main)
        btn_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 8))

        ttk.Button(btn_frame, text="Solve", command=self._on_solve).pack(
            side=tk.LEFT, padx=(0, 4)
        )
        ttk.Button(btn_frame, text="Clear", command=self._on_clear).pack(
            side=tk.LEFT, padx=4
        )
        ttk.Button(btn_frame, text="Load G1 (TD-01)", command=self._load_g1).pack(
            side=tk.LEFT, padx=4
        )
        ttk.Button(btn_frame, text="Load G2 (TD-02)", command=self._load_g2).pack(
            side=tk.LEFT, padx=4
        )
        ttk.Button(
            btn_frame, text="Load G0 (complete)", command=self._load_g0
        ).pack(side=tk.LEFT, padx=4)

        result_frame = ttk.LabelFrame(main, text="result", padding=8)
        result_frame.grid(row=3, column=0, columnspan=2, sticky="ew")

        self._status_var = tk.StringVar(value="Ready.")
        ttk.Label(
            result_frame,
            textvariable=self._status_var,
            wraplength=480,
            justify="left",
        ).grid(row=0, column=0, sticky="w")

        self._load_g1()

    def run(self) -> None:
        self._root.mainloop()

    def _on_clear(self) -> None:
        for row in self._entries:
            for entry in row:
                entry.delete(0, tk.END)
        self._status_var.set("Cleared.")

    def _load_g1(self) -> None:
        set_matrix_in_entries(self._entries, G1_TD01_SAMPLE)
        self._status_var.set("Loaded PRD TD-01 (G1). Click Solve.")

    def _load_g2(self) -> None:
        set_matrix_in_entries(self._entries, G2_TD02_SAMPLE)
        self._status_var.set("Loaded PRD TD-02 (G2). Click Solve.")

    def _load_g0(self) -> None:
        set_matrix_in_entries(self._entries, G0_COMPLETE_SAMPLE)
        self._status_var.set("Loaded G0 (no blanks — expect INPUT_BLANK_COUNT_INVALID).")

    def _on_solve(self) -> None:
        try:
            matrix = read_matrix_from_entries(self._entries)
        except MatrixReadError as exc:
            self._status_var.set(f"Screen parse error: {exc}")
            return

        outcome = self._use_case.execute(matrix)
        if isinstance(outcome, ErrorResponse):
            self._status_var.set(
                f"error.code = {outcome.error.code!r}\n"
                f"error.message = {outcome.error.message!r}"
            )
            return

        self._status_var.set(
            f"Success: {outcome}\n"
            f"[r1,c1,n1,r2,c2,n2] = {outcome}"
        )
