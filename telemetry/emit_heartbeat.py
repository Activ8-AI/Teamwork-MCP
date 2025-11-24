import socket
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional


def generate_heartbeat(additional_payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Generate a standard heartbeat payload."""
    payload = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "host": socket.gethostname(),
        "status": "ok",
    }

    if additional_payload:
        payload.update(additional_payload)

    return payload
