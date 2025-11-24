class Orchestrator:
    def __init__(self, ledger, relays):
        self.ledger = ledger
        self.relays = relays

    def log(self, event_type, payload=None):
        self.ledger.log_event(event_type, payload or {})

    def run_command(self, cmd: str, payload: dict = None):
        self.log("ORCH_COMMAND_RECEIVED", {"cmd": cmd})

        handler = getattr(self, f"cmd_{cmd}", None)
        if not handler:
            self.log("ORCH_COMMAND_UNKNOWN", {"cmd": cmd})
            return {"status": "unknown_command"}

        try:
            result = handler(payload or {})
            self.log("ORCH_COMMAND_SUCCESS", {"cmd": cmd})
            return {"status": "ok", "result": result}
        except Exception as e:
            self.log("ORCH_COMMAND_FAILURE", {"cmd": cmd, "error": str(e)})
            return {"status": "error", "error": str(e)}

    # Example command
    def cmd_mvp_health_check(self, payload):
        from telemetry.emit_heartbeat import generate_heartbeat

        res = {
            "mcp": "unknown",
            "heartbeat": None,
            "ledger": "unknown"
        }

        # MCP health (stub)
        res["mcp"] = "ok"

        # Heartbeat
        hb = generate_heartbeat()
        self.log("ORCH_STEP_HEARTBEAT", hb)
        res["heartbeat"] = hb

        # Ledger check
        res["ledger"] = "ok"

        return res
