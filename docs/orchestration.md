# Multi-Agent Orchestration

This project provides a simple handoff queue for orchestrating collaboration across agents (e.g., Notion Relay, Prime, Claude). It aligns with the Charter Standard (hypothesis-driven, MECE, auditability).

## Handoff Flow

- Produce a `HandoffEvent` with title, optional hypothesis, targets, and context
- Enqueue via the `enqueueHandoff` tool
- Downstream relays consume `handoff/queue.jsonl` and dispatch to the appropriate agent(s)

## Example Tool Call

```json
{
  "name": "enqueueHandoff",
  "arguments": {
    "title": "Prime Charter Agent: Execute 72-hour monitoring",
    "hypothesis": "Automated setup accelerates compliance",
    "targets": [
      { "name": "NotionRelay", "channel": "status-page" },
      { "name": "PrimeAgent" },
      { "name": "ClaudeAgent" }
    ],
    "context": { "projectId": 123456 }
  }
}
```

## Notes

- Persistence is JSONL under `handoff/queue.jsonl` for simplicity; replace with a message bus as needed
- Extend adapters to push to Notion, task queues, or other systems

## Reflex → Competitor Intelligence Pipeline

- Web-analysis agents emit structured signals which are normalized by the Competitor Intelligence Engine.
- The MCP tool `ingestCompetitorDelta` calls `enqueueHandoff` with targets `NotionRelay`, `PrimeAgent`, and `ClaudeAgent`.
- A mirror of every delta is stored under `reflex/pipelines/competitor-deltas.jsonl` for downstream DAGs.
- Teamwork task routing uses the per-client `teamworkTasklistId` defined in the Competitor Definition Map; FALLBACK is `TEAMWORK_COMP_INTEL_TASKLIST_ID`.
- Client Portal widgets subscribe to the same JSONL/brief artifacts to ensure Reflex, Teamwork, and Portal stay in lockstep.
