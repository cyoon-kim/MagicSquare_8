"""Control-layer ports (Protocols) — dependency inversion for boundary adapters."""

from __future__ import annotations

from typing import Protocol

from contracts.errors import ErrorResponse


class MatrixValidatorPort(Protocol):
    """FR-01 input validation at the boundary."""

    def validate(self, matrix: list[list[int]] | None) -> ErrorResponse | None:
        """Return ErrorResponse when input invalid; None when valid."""
        ...


class ResultFormatterPort(Protocol):
    """FR-05b success output formatting at the boundary."""

    def format(self, result: list[int] | ErrorResponse) -> list[int] | ErrorResponse:
        """Format domain success payload or pass through errors."""
        ...
