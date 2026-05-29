"""FR-01 AC-05 / FR-06 AC-23 — Domain chain isolation RED tests.

AC-05, AC-23: FR-01 failure must not invoke Domain or ResultFormatter.
PRD §13 INPUT_SIZE_INVALID on size-invalid matrix.
"""

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


@pytest.mark.control
@pytest.mark.p0
class TestFr01Ac05Ac23UseCaseIsolation:
    """FR-06 orchestration — no Domain/Formatter on FR-01 fail."""

    @staticmethod
    def _build_use_case_with_mocks() -> tuple[SolveMagicSquareUseCase, dict[str, MagicMock]]:
        """Arrange collaborators as MagicMock for call-count verification."""
        mocks = {
            "blank_finder": MagicMock(spec=BlankFinder),
            "missing_number_finder": MagicMock(spec=MissingNumberFinder),
            "magic_square_validator": MagicMock(spec=MagicSquareValidator),
            "solver": MagicMock(spec=Solver),
            "result_formatter": MagicMock(spec=ResultFormatter),
        }
        use_case = SolveMagicSquareUseCase(
            boundary_validator=BoundaryValidator(),
            blank_finder=mocks["blank_finder"],
            missing_number_finder=mocks["missing_number_finder"],
            magic_square_validator=mocks["magic_square_validator"],
            solver=mocks["solver"],
            result_formatter=mocks["result_formatter"],
        )
        return use_case, mocks

    def test_matrix_none_domain_chain_called_zero_times(
        self,
        input_size_invalid_code: str,
    ) -> None:
        """AC-05, AC-23 — BlankFinder/MissingNumberFinder/Validator/Solver not called."""
        # Given: matrix is None and Domain collaborators are mocked
        use_case, mocks = self._build_use_case_with_mocks()
        matrix = None

        # When: UseCase executes with size-invalid matrix
        result = use_case.execute(matrix)

        # Then: AC-05, AC-23
        mocks["blank_finder"].find.assert_not_called()
        mocks["missing_number_finder"].find.assert_not_called()
        mocks["magic_square_validator"].is_valid.assert_not_called()
        mocks["solver"].solve_or_error.assert_not_called()
        assert result is not None
        assert result.error.code == input_size_invalid_code
        assert result.error.code == "INPUT_SIZE_INVALID"

    def test_matrix_none_result_formatter_called_zero_times(
        self,
    ) -> None:
        """AC-23 — ResultFormatter must not run when FR-01 fails."""
        # Given: matrix is None
        use_case, mocks = self._build_use_case_with_mocks()
        matrix = None

        # When: UseCase executes
        use_case.execute(matrix)

        # Then: AC-23
        mocks["result_formatter"].format.assert_not_called()

    @pytest.mark.parametrize(
        "matrix",
        [
            pytest.param(None, id="BV-01-none"),
            pytest.param([], id="BV-02-empty"),
            pytest.param([[], [], [], []], id="BV-03-four-empty-rows"),
        ],
    )
    def test_invalid_size_matrix_domain_chain_never_invoked(
        self,
        matrix: list[list[int]] | None,
    ) -> None:
        """AC-05, AC-23 — isolation holds for all AC-01 boundary inputs."""
        # Given: size-invalid matrix
        use_case, mocks = self._build_use_case_with_mocks()

        # When: UseCase executes
        use_case.execute(matrix)

        # Then: AC-05, AC-23
        mocks["blank_finder"].find.assert_not_called()
        mocks["missing_number_finder"].find.assert_not_called()
        mocks["magic_square_validator"].is_valid.assert_not_called()
        mocks["solver"].solve_or_error.assert_not_called()
        mocks["result_formatter"].format.assert_not_called()
