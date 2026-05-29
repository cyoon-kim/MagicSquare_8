"""R2 — use case depends on ports, not concrete boundary modules."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest


@pytest.mark.control
class TestControlUseCasePortDependency:
    """solve_magic_square_use_case must not import boundary concretes."""

    def test_use_case_module_does_not_import_boundary(self) -> None:
        """R2 — control use case file has zero boundary imports."""
        use_case_path = (
            Path(__file__).resolve().parents[2]
            / "src"
            / "control"
            / "solve_magic_square_use_case.py"
        )
        tree = ast.parse(use_case_path.read_text(encoding="utf-8"))

        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom) or node.module is None:
                continue
            root = node.module.split(".")[0]
            assert root != "boundary", (
                f"use case imports forbidden module {node.module!r}"
            )
