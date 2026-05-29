"""Launch Magic Square screen (Boundary → Control → Entity)."""

from __future__ import annotations

from boundary.boundary_validator import BoundaryValidator
from boundary.result_formatter import ResultFormatter
from boundary.screen.magic_square_window import MagicSquareWindow
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


def main() -> None:
    window = MagicSquareWindow(build_use_case())
    window.run()


if __name__ == "__main__":
    main()
