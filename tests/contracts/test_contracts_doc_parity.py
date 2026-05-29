"""R12 — contracts.md error codes match contracts.errors SSOT."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from contracts import errors as contracts_errors


@pytest.mark.control
class TestContractsDocParity:
    """docs/contracts.md §2.1 codes exist in contracts.errors."""

    def test_all_contracts_error_codes_registered_in_python(self) -> None:
        """R12 — every documented §13 code has a *_CODE constant."""
        contracts_md = (
            Path(__file__).resolve().parents[2] / "docs" / "contracts.md"
        )
        content = contracts_md.read_text(encoding="utf-8")
        documented_codes = set(re.findall(r"`([A-Z_]+)`", content))
        documented_codes = {
            code
            for code in documented_codes
            if code.startswith(("INPUT_", "OUTPUT_", "DOMAIN_"))
        }

        python_codes = {
            name.removesuffix("_CODE")
            for name in dir(contracts_errors)
            if name.endswith("_CODE")
        }

        missing = documented_codes - python_codes
        assert not missing, f"contracts.md codes missing in contracts.errors: {missing}"
