# ACTIV8 AI — Anonymized Codex Model View (Prospect-Ready)

## Purpose
This anonymized view demonstrates the Codex model architecture and weekly check-in structure without exposing client identities.

## Charter-Compliant Naming Rules
- Use anonymized identifiers (e.g., “Client A,” “Client B”) for prospect-facing assets.
- Real client names are reserved for internal systems and weekly status reporting.
- “Prospect Visible” labels are only used on externally distributed collateral.

## Signal Flow Overview
1. **Verbatim capture** → Transcripts ingested to `/transcripts/...`.
2. **Live request detection** → Slack signals parsed to `/slack_threads/...`.
3. **Operational cadence** → Teamwork task status captured in `/tasks/...`.
4. **Deliverables** → Notion/Drive status logged to `/deliverables/...`.
5. **Assets** → GDrive/GCS uploads stored in `/assets/...`.
6. **Memory & reasoning** → Notebook LM updates stored in `/codex_memory/...`.
7. **Infra visibility** → BigQuery/GCP logs stored in `/infra_logs/...`.
8. **Reporting signals** → KPIs tracked in `/kpis/...`.

## Heartbeat Example (Anonymized)

| Client Name | Status | Last Check-In | Primary Source | Signals Count | Codex Trace |
| --- | --- | --- | --- | --- | --- |
| Client A (Anonymized) | 🟡 Yellow | 2026-01-17 | Transcript + Notion | 5 | HEARTBEAT.2026.01.21 |
| Client B (Anonymized) | 🔴 Red | 2026-01-09 | Teamwork tasks stalled | 2 | HEARTBEAT.2026.01.21 |

## Check-In Structure (Anonymized)
- **Status:** Green / Yellow / Red
- **Signals:** New signal count by source
- **Wins:** Completed deliverables
- **Risks:** Blockers and drift indicators
- **Next Actions:** Confirmed tasks with owner + due date
- **Codex Trace:** `HEARTBEAT.YYYY.MM.DD`

## Codex Trace Reference
- Current reference: `HEARTBEAT.2026.01.21`
- Usage: Aligns heartbeat tables to verifiable signal logs.
