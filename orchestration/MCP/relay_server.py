from typing import Callable, Dict, Any, Optional


class RelayServer:
    """Minimal relay server stub to satisfy MAOS requirements."""

    def __init__(self, handlers: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]]):
        self.handlers = handlers

    def handle(self, command: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if command not in self.handlers:
            return {"status": "unknown_command", "command": command}
        return self.handlers[command](payload or {})
