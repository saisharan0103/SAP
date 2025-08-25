import pytest
from dataclasses import FrozenInstanceError
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from erp.audit import AuditLog
from erp.entities import Entity
from erp.security import Permission, Role, User


def test_post_requires_permission():
    poster_role = Role("poster", [Permission.POST])
    poster = User("poster", [poster_role])
    non_poster = User("nopost", [])

    log = AuditLog()
    doc = Entity(id=1, created_by="author")

    doc.post(poster, log)
    assert doc.posted_by == "poster"

    with pytest.raises(PermissionError):
        doc.post(non_poster, log)


def test_approve_requires_permission():
    approver_role = Role("approver", [Permission.APPROVE])
    approver = User("approver", [approver_role])
    non_approver = User("noapprove", [])

    log = AuditLog()
    doc = Entity(id=2, created_by="author")

    doc.approve(approver, log)
    assert doc.approved_by == "approver"

    with pytest.raises(PermissionError):
        doc.approve(non_approver, log)


def test_audit_log_immutable():
    role = Role("poster", [Permission.POST])
    user = User("user", [role])
    log = AuditLog()
    doc = Entity(id=3, created_by="user")
    doc.post(user, log)

    entries = log.entries()
    assert len(entries) == 1
    entry = entries[0]

    with pytest.raises(FrozenInstanceError):
        entry.username = "hacker"

    with pytest.raises(AttributeError):
        entries.append(entry)
