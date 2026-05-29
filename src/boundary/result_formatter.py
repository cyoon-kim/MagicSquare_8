"""ResultFormatter — FR-05b success output contract."""

from __future__ import annotations

from boundary.models import ErrorResponse


class ResultFormatter:
    """Formats domain success payload to int[6] (1-index coordinates)."""

    def format(self, result: list[int] | ErrorResponse) -> list[int] | ErrorResponse:
        if isinstance(result, ErrorResponse):
            return result
        return result
