# ACTIV8 AI — Signal Intelligence Architecture (2026-01-21)

## Charter Clarifications
- Keene Systems and Supreme Outdoor Living are no longer active clients.
- Their data is approved for anonymized model views only, not active client check-ins.
- Client Weekly Check-Ins are **only** for active Leverage Marketing Agency clients.
- “Prospect Visible” should only appear on externally used prospecting collateral.

## Signal Grid (Warehouse + Intelligence)

| Signal Type | Source | Charter Role | Output Path |
| --- | --- | --- | --- |
| 🎥 Verbatim Transcripts | Fathom / Zoom / Meet | Human-voice to Codex | `/transcripts/...` |
| 💬 Client Chat | Slack DM + Channels | Live request detection | `/slack_threads/...` |
| ✅ Tasks & Status | Teamwork | Operational cadence + logging | `/tasks/...` |
| 📁 Deliverables & Docs | Notion / Google Drive | Proposal/brief status, completion | `/deliverables/...` |
| 📦 Assets & Uploads | GDrive, GCS | Warehouse of client work | `/assets/...` |
| 📓 Notebook LM | Memory context, agent notes | 🧠 SigNIT — live reasoning trails | `/codex_memory/...` |
| 🔍 BigQuery / GCP Logs | Usage, error reports | Deployment tracking, infra drift | `/infra_logs/...` |
| 📊 LookerStudio / Sheets | KPIs, dashboards, budgets | Reporting signals | `/kpis/...` |

## Notebook LM vs Warehouse

| Feature | Notebook LM | Data Warehouses (GDrive, GCP) |
| --- | --- | --- |
| Signal Type | SigNIT (Intelligence) | Raw or enriched data assets |
| Author | Agent-generated or human input | Client-uploaded or internal upload |
| Codex Role | Memory, logic, reasoning threads | Source of truth, audit, documentation |
| Processing | Ingested via Codex trace + MCP agents | Swept via charter-sweep-agent |
| Usage | Decision support, context expansion | Evidence, reference, work product |

**Notebook LM = Dynamic Memory.**  
**Warehouses = Static Knowledge & Artifacts.**

## Registration
- Registered under Codex as: `SIGNALS.2026.01.21.ACTIV8`.
- Registered under MCP as: `mcp://activ8/signals/2026-01-21`.
- Canonical owner: Activ8 AI Signal Intelligence Model (Charter-Compliant).
