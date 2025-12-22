import time
from custody.custodian_ledger import log_event
from telemetry.emit_heartbeat import generate_heartbeat


def run_single_cycle() -> None:
    heartbeat = generate_heartbeat({"cycle": "single"})
    log_event("AUTONOMY_LOOP", heartbeat)


def start_autonomy_loop(iterations: int = 1, sleep_seconds: float = 0.0) -> None:
    for _ in range(iterations):
        run_single_cycle()
        if sleep_seconds:
            time.sleep(sleep_seconds)


if __name__ == "__main__":
    start_autonomy_loop()
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import sys
import time
import uuid
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from agent_hub.activate import activate_agent
from custody.custodian_ledger import CustodianLedger


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a simple autonomy loop.")
    parser.add_argument(
        "--interval",
        type=float,
        default=float(os.environ.get("AUTONOMY_LOOP_INTERVAL", "5")),
        help="Seconds between loop iterations.",
    )
    return parser.parse_args()


def run_autonomy_loop(interval: float) -> None:
    ledger = CustodianLedger()
    agent_info = activate_agent()
    print(f"[autonomy] activated agent: {agent_info}", flush=True)

    iteration = 0
    try:
        while True:
            iteration += 1
            cycle_id = str(uuid.uuid4())
            ledger.record_autonomy_loop(
                cycle_id=cycle_id,
                meta={"iteration": iteration, "agent": agent_info["agent_name"]},
            )
            print(f"[autonomy] recorded cycle {iteration} ({cycle_id})", flush=True)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Autonomy loop halted by user.", flush=True)


def main() -> None:
    args = parse_args()
    run_autonomy_loop(interval=args.interval)


if __name__ == "__main__":
    main()
