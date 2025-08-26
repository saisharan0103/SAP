"""Internal APIs exposing core facilities for extension modules."""
from typing import Any, Dict
from .events import EventBus

# Global event bus used across the application
_event_bus = EventBus()
# Registered modules by name
_modules: Dict[str, Any] = {}

def event_bus() -> EventBus:
    """Return the application's :class:`EventBus`."""
    return _event_bus

def register_module(name: str, module: Any) -> None:
    """Register a module under ``name`` and notify listeners."""
    _modules[name] = module
    _event_bus.emit("module_registered", name=name, module=module)

def register_tax_module(module: Any) -> None:
    """Convenience helper for registering a tax module."""
    register_module("tax", module)

def register_payroll_module(module: Any) -> None:
    """Convenience helper for registering a payroll module."""
    register_module("payroll", module)

def get_module(name: str) -> Any:
    """Return a previously registered module or ``None``."""
    return _modules.get(name)
