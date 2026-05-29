"""R11 — app.py uses logging instead of print for --verify CLI."""

from __future__ import annotations

import ast
import logging
from pathlib import Path

import pytest

from boundary.screen.app import run_verify_none_grid


@pytest.mark.boundary
class TestAppVerifyLogging:
    """--verify path logs outcomes; production src must not call print()."""

    def test_run_verify_none_grid_logs_error_code(self, caplog: pytest.LogCaptureFixture) -> None:
        """R11 — None matrix verify logs INPUT_SIZE_INVALID via logging."""
        caplog.set_level(logging.INFO)

        run_verify_none_grid()

        assert "code=INPUT_SIZE_INVALID" in caplog.text
        assert "message=Input matrix must be 4x4." in caplog.text

    def test_src_modules_do_not_call_print(self) -> None:
        """R11 — grep-equivalent AST check: no print() in src/."""
        src_dir = Path(__file__).resolve().parents[2] / "src"

        for py_file in sorted(src_dir.rglob("*.py")):
            tree = ast.parse(py_file.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                func = node.func
                if isinstance(func, ast.Name) and func.id == "print":
                    pytest.fail(f"{py_file.relative_to(src_dir.parent)} uses print()")
