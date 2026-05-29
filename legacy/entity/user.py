"""User entity for MagicSquare domain."""

from __future__ import annotations

from dataclasses import dataclass
from re import match


_EMAIL_PATTERN: str = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


@dataclass(frozen=True, slots=True)
class User:
    """Represents a domain user entity.

    This entity stays independent from boundary/control concerns and only
    encapsulates user-related domain rules.

    Attributes:
        user_id: Unique positive identifier.
        name: User display name.
        email: User email address.
        is_active: Activation status.
    """

    user_id: int
    name: str
    email: str
    is_active: bool = True

    def __post_init__(self) -> None:
        """Validates domain invariants after initialization.

        Raises:
            ValueError: If any invariant is violated.
        """
        if self.user_id <= 0:
            raise ValueError("user_id must be a positive integer.")
        if not self.name.strip():
            raise ValueError("name must not be empty.")
        if match(_EMAIL_PATTERN, self.email) is None:
            raise ValueError("email format is invalid.")

    def activate(self) -> User:
        """Returns a new active user.

        Returns:
            User: A copied user with active status.
        """
        return User(
            user_id=self.user_id,
            name=self.name,
            email=self.email,
            is_active=True,
        )

    def deactivate(self) -> User:
        """Returns a new inactive user.

        Returns:
            User: A copied user with inactive status.
        """
        return User(
            user_id=self.user_id,
            name=self.name,
            email=self.email,
            is_active=False,
        )

    def change_name(self, new_name: str) -> User:
        """Returns a new user with updated name.

        Args:
            new_name: New display name.

        Returns:
            User: A copied user with changed name.

        Raises:
            ValueError: If new_name is empty.
        """
        if not new_name.strip():
            raise ValueError("new_name must not be empty.")
        return User(
            user_id=self.user_id,
            name=new_name,
            email=self.email,
            is_active=self.is_active,
        )

    def change_email(self, new_email: str) -> User:
        """Returns a new user with updated email.

        Args:
            new_email: New email address.

        Returns:
            User: A copied user with changed email.

        Raises:
            ValueError: If new_email format is invalid.
        """
        if match(_EMAIL_PATTERN, new_email) is None:
            raise ValueError("new_email format is invalid.")
        return User(
            user_id=self.user_id,
            name=self.name,
            email=new_email,
            is_active=self.is_active,
        )
