#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a small autonomy loop.")
    parser.add_argument(
        "--iterations",
        type=int,
        default=int(os.environ.get("AUTONOMY_LOOP_ITERATIONS", "1")),
        help="Number of iterations to run.",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=float(os.environ.get("AUTONOMY_LOOP_INTERVAL", "0")),
        help="Seconds between iterations.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    start_autonomy_loop(iterations=args.iterations, sleep_seconds=args.interval)


if __name__ == "__main__":
    main()
