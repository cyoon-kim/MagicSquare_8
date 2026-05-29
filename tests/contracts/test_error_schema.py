"""R1 — shared contracts error schema and import-direction smoke."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from contracts.errors import (
    DOMAIN_NO_MAGIC_ASSIGNMENT_CODE,
    ErrorDetail,
    ErrorResponse,
    INPUT_SIZE_INVALID_CODE,
    INPUT_SIZE_INVALID_MESSAGE,
)


@pytest.mark.control
class TestContractsErrorSchema:
    """contracts.errors matches PRD §13 envelope."""

    def test_error_response_schema_round_trip(self) -> None:
        """ErrorResponse holds code and message on error detail."""
        response = ErrorResponse(
            error=ErrorDetail(
                code=INPUT_SIZE_INVALID_CODE,
                message=INPUT_SIZE_INVALID_MESSAGE,
            )
        )

        assert response.error.code == INPUT_SIZE_INVALID_CODE
        assert response.error.message == INPUT_SIZE_INVALID_MESSAGE

    def test_domain_no_magic_assignment_code_registered(self) -> None:
        """DOMAIN_NO_MAGIC_ASSIGNMENT is available from contracts SSOT."""
        assert DOMAIN_NO_MAGIC_ASSIGNMENT_CODE == "DOMAIN_NO_MAGIC_ASSIGNMENT"


@pytest.mark.control
class TestContractsImportDirectionSmoke:
    """Entity layer must not import boundary or control (ECB)."""

    def test_entity_modules_do_not_import_boundary_or_control(self) -> None:
        """R1 — grep-equivalent AST check on src/entity/*.py."""
        entity_dir = Path(__file__).resolve().parents[2] / "src" / "entity"
        forbidden_prefixes = ("boundary", "control")

        for py_file in sorted(entity_dir.glob("*.py")):
            tree = ast.parse(py_file.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if not isinstance(node, ast.ImportFrom) or node.module is None:
                    continue
                root = node.module.split(".")[0]
                assert root not in forbidden_prefixes, (
                    f"{py_file.name} imports forbidden module {node.module!r}"
                )
