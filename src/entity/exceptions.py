"""Domain exceptions (business failures use error objects at Boundary)."""


class UnsolvableDomainError(Exception):
    """FR-05a / AC-18 — no valid two-cell assignment."""
