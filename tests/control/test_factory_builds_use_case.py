"""R3 — composition factory builds a working use case."""

from __future__ import annotations

import pytest

from contracts.errors import ErrorResponse
from control.factory import build_solve_magic_square_use_case
from control.solve_magic_square_use_case import SolveMagicSquareUseCase
from grids import G1_EXPECTED_STEP_A, G1_MATRIX


@pytest.mark.control
@pytest.mark.p0
class TestFactoryBuildsUseCase:
    """control.factory wires collaborators without app.py entity imports."""

    def test_factory_returns_solve_magic_square_use_case(self) -> None:
        """build_solve_magic_square_use_case returns UseCase instance."""
        use_case = build_solve_magic_square_use_case()

        assert isinstance(use_case, SolveMagicSquareUseCase)

    def test_factory_wired_use_case_solves_g1(self) -> None:
        """Factory-built use case produces G1 success int[6]."""
        use_case = build_solve_magic_square_use_case()

        result = use_case.execute(G1_MATRIX)

        assert result == G1_EXPECTED_STEP_A

    def test_factory_wired_use_case_returns_error_for_none(self) -> None:
        """Factory-built use case returns ErrorResponse for None matrix."""
        use_case = build_solve_magic_square_use_case()

        result = use_case.execute(None)

        assert isinstance(result, ErrorResponse)
        assert result.error.code == "INPUT_SIZE_INVALID"
