"""Control layer — use case orchestration."""

from control.factory import build_solve_magic_square_use_case
from control.solve_magic_square_use_case import SolveMagicSquareUseCase

__all__ = ["SolveMagicSquareUseCase", "build_solve_magic_square_use_case"]
