from __future__ import annotations

"""Domain entities for the ERP system."""

from dataclasses import dataclass
from typing import Optional

from .audit import AuditLog
from .security import Permission, User, has_permission


@dataclass
class Entity:
    """Base entity storing audit metadata."""

    id: int
    created_by: str
    posted_by: Optional[str] = None
    approved_by: Optional[str] = None

    def post(self, user: User, log: AuditLog) -> None:
        """Post the entity if the user has the ``POST`` permission."""
        if not has_permission(user, Permission.POST):
            raise PermissionError("User lacks permission to post")
        self.posted_by = user.username
        log.log_action(self, user, "post")

    def approve(self, user: User, log: AuditLog) -> None:
        """Approve the entity if the user has the ``APPROVE`` permission."""
        if not has_permission(user, Permission.APPROVE):
            raise PermissionError("User lacks permission to approve")
        self.approved_by = user.username
        log.log_action(self, user, "approve")
