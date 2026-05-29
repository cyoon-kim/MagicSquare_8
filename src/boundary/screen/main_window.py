"""PyQt main window for Magic Square 4x4 partial grid solver."""

from __future__ import annotations

from PyQt6.QtWidgets import (
    QGridLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from boundary.models import ErrorResponse
from boundary.screen.samples import G1_TD01_SAMPLE
from control.solve_magic_square_use_case import SolveMagicSquareUseCase

_GRID_SIZE = 4
_SPIN_MIN = 0
_SPIN_MAX = 16


class MagicSquareMainWindow(QMainWindow):
    """4x4 spinbox grid with solve action wired to Control use case only."""

    def __init__(self, use_case: SolveMagicSquareUseCase) -> None:
        super().__init__()
        self._use_case = use_case
        self._spinboxes: list[list[QSpinBox]] = []
        self._result_label = QLabel("")
        self._init_ui()

    def _init_ui(self) -> None:
        self.setWindowTitle("Magic Square 4x4")

        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QVBoxLayout(central)

        grid_layout = QGridLayout()
        for row in range(_GRID_SIZE):
            row_boxes: list[QSpinBox] = []
            for col in range(_GRID_SIZE):
                spinbox = QSpinBox()
                spinbox.setRange(_SPIN_MIN, _SPIN_MAX)
                spinbox.setValue(G1_TD01_SAMPLE[row][col])
                grid_layout.addWidget(spinbox, row, col)
                row_boxes.append(spinbox)
            self._spinboxes.append(row_boxes)

        solve_button = QPushButton("풀기")
        solve_button.clicked.connect(self._on_solve)

        root_layout.addLayout(grid_layout)
        root_layout.addWidget(solve_button)
        root_layout.addWidget(self._result_label)

    def _read_grid(self) -> list[list[int]]:
        return [
            [spinbox.value() for spinbox in row_boxes]
            for row_boxes in self._spinboxes
        ]

    def _on_solve(self) -> None:
        grid = self._read_grid()
        result = self._use_case.execute(grid)

        if isinstance(result, ErrorResponse):
            self._result_label.setText(f"오류: {result.error.message}")
            return

        values = ", ".join(str(value) for value in result)
        self._result_label.setText(f"결과 (r1, c1, n1, r2, c2, n2): {values}")
