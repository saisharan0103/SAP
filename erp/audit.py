from __future__ import annotations

"""Audit logging facilities."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Tuple


@dataclass(frozen=True)
class AuditEntry:
    """Represents a single immutable audit log entry."""

    entity_id: int
    entity_type: str
    action: str
    username: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class AuditLog:
    """Immutable audit log table.

    Entries can be appended but never modified or removed.
    """

    def __init__(self) -> None:
        self._entries: List[AuditEntry] = []

    def log_action(self, entity, user, action: str) -> None:
        """Record an action performed by ``user`` on ``entity``."""
        entry = AuditEntry(
            entity_id=getattr(entity, "id", None),
            entity_type=entity.__class__.__name__,
            action=action,
            username=user.username,
        )
        self._entries.append(entry)

    def entries(self) -> Tuple[AuditEntry, ...]:
        """Return audit entries as an immutable tuple."""
        return tuple(self._entries)
