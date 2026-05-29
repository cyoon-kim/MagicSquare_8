"""Entity layer — domain logic (FR-02~05a)."""

from entity.blank_finder import BlankFinder
from entity.exceptions import UnsolvableDomainError
from entity.magic_square_validator import MagicSquareValidator
from entity.missing_number_finder import MissingNumberFinder
from entity.solver import Solver

__all__ = [
    "BlankFinder",
    "MagicSquareValidator",
    "MissingNumberFinder",
    "Solver",
    "UnsolvableDomainError",
]
