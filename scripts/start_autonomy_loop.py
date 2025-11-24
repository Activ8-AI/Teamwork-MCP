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
