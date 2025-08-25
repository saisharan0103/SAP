"""Core package providing extension points for SAPro."""
from .api import (
    event_bus,
    get_module,
    register_module,
    register_payroll_module,
    register_tax_module,
)
from .hooks import apply_hooks

__all__ = [
    "event_bus",
    "get_module",
    "register_module",
    "register_payroll_module",
    "register_tax_module",
    "apply_hooks",
]
