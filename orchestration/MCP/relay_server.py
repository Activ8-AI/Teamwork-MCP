from __future__ import annotations

from typing import Any, Callable, Dict, Optional


class RelayServer:
    """Minimal relay server stub to satisfy MAOS requirements.

    This module intentionally avoids external web dependencies (FastAPI/Uvicorn).
    """

    def __init__(self, handlers: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]]):
        self.handlers = handlers

    def handle(self, command: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if command not in self.handlers:
            return {"status": "unknown_command", "command": command}
        try:
            return self.handlers[command](payload or {})
        except Exception as e:
            return {"status": "error", "command": command, "error": "An internal error occurred."}


__all__ = ["RelayServer"]
