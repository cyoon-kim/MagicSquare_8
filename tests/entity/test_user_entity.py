"""Tests for the User entity."""

from __future__ import annotations

import pytest

from entity.user import User


def test_create_user_with_valid_data() -> None:
    """Creates a user when input satisfies invariants."""
    # Arrange
    user_id = 1
    name = "Alice"
    email = "alice@example.com"

    # Act
    user = User(user_id=user_id, name=name, email=email)

    # Assert
    assert user.user_id == user_id
    assert user.name == name
    assert user.email == email
    assert user.is_active is True


def test_create_user_with_invalid_name_raises_error() -> None:
    """Raises ValueError for empty names."""
    # Arrange
    user_id = 1
    name = "   "
    email = "alice@example.com"

    # Act / Assert
    with pytest.raises(ValueError, match="name must not be empty."):
        User(user_id=user_id, name=name, email=email)


def test_create_user_with_invalid_email_raises_error() -> None:
    """Raises ValueError for invalid email format."""
    # Arrange
    user_id = 1
    name = "Alice"
    email = "alice.example.com"

    # Act / Assert
    with pytest.raises(ValueError, match="email format is invalid."):
        User(user_id=user_id, name=name, email=email)


def test_deactivate_returns_new_inactive_user() -> None:
    """Creates a new inactive user without mutating original."""
    # Arrange
    original_user = User(user_id=1, name="Alice", email="alice@example.com")

    # Act
    updated_user = original_user.deactivate()

    # Assert
    assert original_user.is_active is True
    assert updated_user.is_active is False
    assert updated_user.user_id == original_user.user_id


def test_change_email_returns_new_user_with_updated_email() -> None:
    """Changes email while preserving other fields."""
    # Arrange
    original_user = User(user_id=1, name="Alice", email="alice@example.com")
    new_email = "alice.new@example.com"

    # Act
    updated_user = original_user.change_email(new_email=new_email)

    # Assert
    assert original_user.email == "alice@example.com"
    assert updated_user.email == new_email
    assert updated_user.name == original_user.name
    assert updated_user.user_id == original_user.user_id
