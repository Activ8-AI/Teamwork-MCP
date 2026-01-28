# Competitive Intelligence Engine (v1)

Status: **Required** • Classification: MAOS → Intelligence Plane → Web Analysis Agents → Client Portal

The Competitive Intelligence Engine gives MAOS external situational awareness by pairing automated web-analysis agents with Reflex tasking and Client Portal outputs. It complements the internal Action Matrix by streaming competitor deltas into Teamwork, Codex, and client-facing surfaces.

## Components

1. **Competitor Definition Map** (`codex-portal/client-intelligence/competitor-definition-map.json`)
   - Mirrors the Notion + Codex sources of truth.
   - Stores task list IDs, Reflex channels, alerts, and watchlists per client/competitor.
   - Referenced by the MCP server to resolve routing.

2. **Web Analysis Agents**
   - `surveillance_agent`, `research_agent`, `competitor_watch_agent`, `web_crawler_agent`, `signal_harvester_agent`, `content_diff_agent`.
   - Assignment rules, triggers, and output contracts documented in `agents.md`.

3. **Intelligence Service**
   - `src/services/intelligence/competitorIntelligenceEngine.ts`
   - Persists deltas to `competitor-intel/deltas.jsonl`, writes briefs, and enqueues Reflex handoffs.
   - Generates Teamwork tasks using per-client task list IDs or `TEAMWORK_COMP_INTEL_TASKLIST_ID`.

4. **MCP Tool**
   - `ingestCompetitorDelta`
   - Input schema enforces Charter-standard metadata (summary, evidence, market impact, actions).
   - Returns the enriched delta record, including brief path and custodian hash.

5. **Client Portal Outputs**
   - Portal tabs and widgets defined in the map (Competitor Intelligence, Industry Radar, Trend Watch, Risk Levels, Action Recommendations).
   - Downstream portal services read `competitor-intel/briefs` + `deltas.jsonl` to hydrate cards, risk meters, and heartbeat streams.

## Reflex + Teamwork Pipeline

1. Agents detect an external signal and emit a structured payload.
2. The MCP tool `ingestCompetitorDelta` is invoked (manually or via automation).
3. The service:
   - Writes JSONL + Markdown artifacts.
   - Calculates confidence score + custodian hash.
   - Creates a Teamwork task with embedded summary/actions.
   - Enqueues a `handoff` event targeting Notion Relay, Prime Agent, and Claude Agent.
   - Mirrors the record to `reflex/pipelines/competitor-deltas.jsonl`.
4. Client Portal pulls the latest briefs + deltas, raising red/yellow alerts and updating KPIs/Risk meters.

## Configuration

| Requirement | Location |
| --- | --- |
| Per-client task list routing | `teamworkTasklistId` in Competitor Definition Map (fallback env: `TEAMWORK_COMP_INTEL_TASKLIST_ID`). |
| Reflex channel name | `reflexChannel` per client. |
| Portal tab layouts | `portalViews` per client. |
| Alert thresholds | `alerts` array per client. |

## Operational Notes

- Every brief follows: Summary → Market Impact → Strategic Implication → Recommended Actions → Governance Notes → Confidence → Custodian Hash.
- STOP–RESET–REALIGN policy: three unresolved red alerts pause ingestion until a TAO memo is filed (see `agents.md`).
- Evidence is stored as URLs/snippets today; connect to Evidence Binder in Vault for binary artifacts when available.
- Extend the tool or service when new intel categories (e.g., app store, developer docs, partner ecosystems) need polling—ensure the Competitor Definition Map is updated for those sources.
