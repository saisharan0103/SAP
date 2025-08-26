"""Configuration-driven hooks for custom fields and validation rules."""
from __future__ import annotations

from typing import Any, Dict
from .events import EventBus


def apply_hooks(config: Dict[str, Any], bus: EventBus) -> None:
    """Apply hooks defined in ``config`` using ``bus``.

    The configuration may include:
    ``custom_fields``: mapping of field name to default value
    ``validation_rules``: mapping of rule name to callable accepting data
    """
    for field, default in config.get("custom_fields", {}).items():
        bus.emit("register_custom_field", name=field, default=default)

    for name, rule in config.get("validation_rules", {}).items():
        bus.emit("register_validation_rule", name=name, rule=rule)
