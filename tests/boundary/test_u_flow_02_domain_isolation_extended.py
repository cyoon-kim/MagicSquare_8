"""Track A — U-FLOW-02 extended (AC-05, AC-23, FR-06)."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from boundary.boundary_validator import BoundaryValidator
from boundary.result_formatter import ResultFormatter
from control.solve_magic_square_use_case import SolveMagicSquareUseCase
from entity.blank_finder import BlankFinder
from entity.magic_square_validator import MagicSquareValidator
from entity.missing_number_finder import MissingNumberFinder
from entity.solver import Solver
from grids import G0_MATRIX


def _build_use_case_with_mocks() -> tuple[SolveMagicSquareUseCase, MagicMock]:
    solver = MagicMock(spec=Solver)
    use_case = SolveMagicSquareUseCase(
        boundary_validator=BoundaryValidator(),
        blank_finder=BlankFinder(),
        missing_number_finder=MissingNumberFinder(),
        magic_square_validator=MagicSquareValidator(),
        solver=solver,
        result_formatter=ResultFormatter(),
    )
    return use_case, solver


@pytest.mark.boundary
@pytest.mark.control
@pytest.mark.p0
class TestUFlow02DomainIsolationExtended:
    """U-FLOW-02 — Solver.solve not called on Boundary validation failure."""

    def test_u_flow_02_none_matrix_solver_never_called(self) -> None:
        use_case, solver = _build_use_case_with_mocks()

        use_case.execute(None)

        solver.solve_or_error.assert_not_called()

    def test_u_flow_02_invalid_size_solver_never_called(self) -> None:
        use_case, solver = _build_use_case_with_mocks()
        matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]

        use_case.execute(matrix)

        solver.solve_or_error.assert_not_called()

    def test_u_flow_02_wrong_blank_count_solver_never_called(self) -> None:
        use_case, solver = _build_use_case_with_mocks()

        use_case.execute(G0_MATRIX)

        solver.solve_or_error.assert_not_called()

    def test_u_flow_02_value_range_invalid_solver_never_called(self) -> None:
        use_case, solver = _build_use_case_with_mocks()
        matrix = [
            [16, 3, 2, 13],
            [5, 0, 11, 8],
            [9, 6, 0, 12],
            [4, 15, 14, -1],
        ]

        use_case.execute(matrix)

        solver.solve_or_error.assert_not_called()

    def test_u_flow_02_duplicate_non_zero_solver_never_called(self) -> None:
        use_case, solver = _build_use_case_with_mocks()
        matrix = [
            [16, 3, 2, 13],
            [5, 0, 11, 8],
            [9, 6, 0, 12],
            [4, 15, 14, 8],
        ]

        use_case.execute(matrix)

        solver.solve_or_error.assert_not_called()
