"""Magic Square 4x4 PyQt screen entry point.

Run from project root after ``pip install -e ".[gui]"``:

    python -m boundary.screen.app

Optional boundary check for None input (CLI):

    python -m boundary.screen.app --verify
"""

from __future__ import annotations

import logging
import sys

from PyQt6.QtWidgets import QApplication

from boundary.screen.main_window import MagicSquareMainWindow
from contracts.errors import ErrorResponse
from control.factory import build_solve_magic_square_use_case

logger = logging.getLogger(__name__)


def run_verify_none_grid() -> None:
    """Log use-case outcome for None matrix (manual AC check)."""
    outcome = build_solve_magic_square_use_case().execute(None)
    if isinstance(outcome, ErrorResponse):
        logger.info("code=%s", outcome.error.code)
        logger.info("message=%s", outcome.error.message)
        return
    logger.info("data=%s", outcome)


def main() -> int:
    """Launch PyQt GUI or run ``--verify`` CLI boundary check."""
    if "--verify" in sys.argv:
        logging.basicConfig(level=logging.INFO, format="%(message)s")
        run_verify_none_grid()
        return 0

    app = QApplication(sys.argv)
    window = MagicSquareMainWindow(build_solve_magic_square_use_case())
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
