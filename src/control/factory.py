"""Composition factory — wires concrete boundary and entity collaborators."""

from __future__ import annotations

from boundary.boundary_validator import BoundaryValidator
from boundary.result_formatter import ResultFormatter
from control.solve_magic_square_use_case import SolveMagicSquareUseCase
from entity.blank_finder import BlankFinder
from entity.magic_square_validator import MagicSquareValidator
from entity.missing_number_finder import MissingNumberFinder
from entity.solver import Solver


def build_solve_magic_square_use_case() -> SolveMagicSquareUseCase:
    """Build a fully wired SolveMagicSquareUseCase (composition root helper).

    Returns:
        Use case with default boundary and entity implementations.
    """
    return SolveMagicSquareUseCase(
        boundary_validator=BoundaryValidator(),
        blank_finder=BlankFinder(),
        missing_number_finder=MissingNumberFinder(),
        magic_square_validator=MagicSquareValidator(),
        solver=Solver(),
        result_formatter=ResultFormatter(),
    )
