from __future__ import annotations

"""Simple user, role and permission models for the ERP system."""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List


class Permission(Enum):
    """Supported permissions within the ERP system."""

    POST = auto()
    APPROVE = auto()


@dataclass
class Role:
    """A role aggregates a set of permissions."""

    name: str
    permissions: List[Permission] = field(default_factory=list)


@dataclass
class User:
    """Represents an authenticated user in the system."""

    username: str
    roles: List[Role] = field(default_factory=list)

    def has_permission(self, permission: Permission) -> bool:
        """Return ``True`` if the user is granted ``permission``."""
        return any(permission in role.permissions for role in self.roles)


def has_permission(user: User, permission: Permission) -> bool:
    """Convenience helper to check for a permission on a user."""

    return user.has_permission(permission)
