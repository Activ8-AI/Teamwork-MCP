Notion Portal & Relay
=====================

Databases
---------

Agents Dashboard (properties)
- Agent (Select): Prime, Clawed, Ancillary
- Task (Title)
- Charter Stage (Select): Intake, In-Flight, Review, Complete
- Status (Select): G, Y, R
- Due (Date & Time, America/New_York)
- Log (Relation → Agent Logs)

Agent Logs (properties)
- Timestamp (Date & Time)
- Agent (Relation → Agents Dashboard)
- Action Description (Text)
- Version (Text, e.g., v1.0)

Charter Checkpoint (template)
- Pilot Principle checklist
- Integrity Override flag

Relay Webhooks
--------------

- Prime → POST /webhook/prime
- Claude → POST /webhook/claude (legacy alias: /webhook/clawed)
- Notion → POST /webhook/notion (legacy alias: /webhook/ancillary)

Payload (example)
```json
{
  "task_id": "<notion_row_id>",
  "agent": "Prime",
  "action": "Intake",
  "timestamp": "2025-09-30T15:33:00Z",
  "version": "v1.0"
}
```

Server
------

- Start local webhook server: `npm run relay:serve`
- The server enqueues handoffs consumed by the dispatcher.

Client Portal Intelligence Views
--------------------------------

The Client Portal now renders competitor intelligence tabs defined in `codex-portal/client-intelligence/competitor-definition-map.json`.

- **Competitor Intelligence Tab**: live delta feed with Reflex status badges, linked briefs, and Teamwork task sync.
- **Industry Radar Tab**: macro heatmap (pricing bands, sentiment trends, share-of-voice gauges).
- **Trend Watch Tab**: ranked signal stack highlighting confidence scores and pending analysis.
- **Risk Levels Tab**: red/yellow/green grid tying external threats to revenue segments.
- **Action Recommendations Tab**: mirrors Teamwork tasks created by the Competitor Intelligence Engine, grouped by charter priority.

Each tab can be bound to a Notion database view; use the `portalViews` array inside the Competitor Definition Map to align widget names to their Notion database IDs.
