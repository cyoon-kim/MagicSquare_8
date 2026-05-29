"""Magic Square 4x4 PyQt screen entry point.

Run from project root after ``pip install -e ".[gui]"``:

    python -m boundary.screen.app

Optional boundary check for None input (CLI):

    python -m boundary.screen.app --verify
"""

from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication

from boundary.boundary_validator import BoundaryValidator
from boundary.models import ErrorResponse
from boundary.result_formatter import ResultFormatter
from boundary.screen.main_window import MagicSquareMainWindow
from control.solve_magic_square_use_case import SolveMagicSquareUseCase
from entity.blank_finder import BlankFinder
from entity.magic_square_validator import MagicSquareValidator
from entity.missing_number_finder import MissingNumberFinder
from entity.solver import Solver


def build_use_case() -> SolveMagicSquareUseCase:
    return SolveMagicSquareUseCase(
        boundary_validator=BoundaryValidator(),
        blank_finder=BlankFinder(),
        missing_number_finder=MissingNumberFinder(),
        magic_square_validator=MagicSquareValidator(),
        solver=Solver(),
        result_formatter=ResultFormatter(),
    )


def run_verify_none_grid() -> None:
    """Print use-case outcome for None matrix (manual AC check)."""
    outcome = build_use_case().execute(None)
    if isinstance(outcome, ErrorResponse):
        print(f"code={outcome.error.code}")
        print(f"message={outcome.error.message}")
        return
    print(f"data={outcome}")


def main() -> int:
    if "--verify" in sys.argv:
        run_verify_none_grid()
        return 0

    app = QApplication(sys.argv)
    window = MagicSquareMainWindow(build_use_case())
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
