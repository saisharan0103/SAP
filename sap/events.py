from collections import defaultdict
from typing import Callable, Dict, List

class EventBus:
    """Simple publish/subscribe event system."""

    def __init__(self) -> None:
        self._listeners: Dict[str, List[Callable]] = defaultdict(list)

    def subscribe(self, event: str, listener: Callable) -> None:
        """Register ``listener`` to be called when ``event`` is emitted."""
        self._listeners[event].append(listener)

    def emit(self, event: str, **payload) -> None:
        """Emit ``event`` and invoke all registered listeners with ``payload``."""
        for listener in self._listeners.get(event, []):
            listener(**payload)
