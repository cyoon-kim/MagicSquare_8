"""R3 — app.py composition root must not wire entity directly."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest


@pytest.mark.boundary
class TestAppCompositionRoot:
    """boundary.screen.app uses factory, not entity imports."""

    def test_app_module_does_not_import_entity(self) -> None:
        """R3 — app.py has zero entity imports."""
        app_path = (
            Path(__file__).resolve().parents[2]
            / "src"
            / "boundary"
            / "screen"
            / "app.py"
        )
        tree = ast.parse(app_path.read_text(encoding="utf-8"))

        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom) or node.module is None:
                continue
            root = node.module.split(".")[0]
            assert root != "entity", f"app.py imports forbidden module {node.module!r}"
