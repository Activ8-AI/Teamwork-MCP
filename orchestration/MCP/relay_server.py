from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Dict

from fastapi import FastAPI
import uvicorn

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from telemetry.emit_heartbeat import emit_heartbeat


logger = logging.getLogger("relay_server")
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Codex Relay MCP", version="1.0.0")


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/heartbeat")
def heartbeat() -> Dict[str, Dict[str, str]]:
    payload = emit_heartbeat()
    logger.info("heartbeat dispatched: %s", payload)
    return {"heartbeat": payload}


def run() -> None:
    uvicorn.run(
        "orchestration.MCP.relay_server:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )


if __name__ == "__main__":
    run()
