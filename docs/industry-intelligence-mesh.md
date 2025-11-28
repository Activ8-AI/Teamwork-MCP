# Industry Intelligence Mesh (v1)

Give MAOS a wide-field sensing fabric that keeps every agent aware of macro-level change. The mesh does not replace the Competitive Intelligence Engine (CIE); it sits beside it so we can see both player-level moves (CIE) and atmospheric pressure (Mesh).

---

## 1. Purpose

- Continuously ingest the macro signals (industry, regulatory, platform, cultural) that precede competitive motion.
- Normalize those signals into shared structures so downstream DAGs, Teamwork tasks, and the Client Intelligence Portal consume them without bespoke parsing.
- Publish anticipatory intelligence (volatility, opportunity, threats) into the Reflex system so MAOS plans ahead instead of reacting after damage.

---

## 2. Why It Follows the Competitive Intelligence Engine

| Layer | Scope | Latency | Primary Question | Dependency |
| --- | --- | --- | --- | --- |
| Competitive Intelligence Engine | Direct competitors, tactical moves | Hours | “What are they doing?” | Requires macro cues to interpret intent |
| Industry Intelligence Mesh | Ecosystem-wide forces | Minutes → Days | “Why are they doing it, and what shifts next?” | Uses CIE outputs to weight alerts |

Competitor movement is rarely spontaneous; it is usually responding to market, regulatory, or platform heat. Without the mesh, we can detect footsteps but miss the weather system that caused them.

---

## 3. Inputs (Signal Surface)

| Feed Cluster | Example Sources | Harvest Method | Refresh Rhythm | Notes |
| --- | --- | --- | --- | --- |
| MarTech / Growth | MKTG Brew, MarTech.org, Growth TLDR | RSS → Harvester or API | 2–4x daily | Tag to demand-gen, retention |
| Strategy & Economics | McKinsey, Bain, BCG, IMF, Fed minutes | Email scrape + PDF parser | Weekly / event driven | Key for macro threat alerts |
| Tech & AI News | Business Insider, Bloomberg Tech, The Information | Paid API + newsletter parsing | Hourly | Flag LLM ecosystem items |
| SEO / Search | SEJ, SEMrush Sensor, Moz weather, Google status, Bing ranking posts | API + webhooks | ≤15 min when API, hourly scrapes otherwise | Drives channel drift |
| LLM Releases | OpenAI, Anthropic, Google, xAI, Perplexity changelogs | RSS / GitHub releases | Event driven | Write to LLM surface map |
| Social / Community | Reddit trending (programmatic), YouTube tech/news, X spaces | API + monitored lists | 15 min poll | Sentiment / narrative deltas |
| Sector Feeds | Real estate, medical, manufacturing, retail trade pubs | Configurable connectors per client matrix | Daily | Determine per client taxonomy |

Treat each feed like weather telemetry—no single article summary, just tagged events with coordinates (source, domain, geography, impacted channels).

---

## 4. Mesh Outputs (System Behaviors)

- **Industry Volatility Index (IVI):** Rolling 7/30-day heat score per vertical, channel, and geo. Weight = volume × recency × sentiment.
- **Opportunity Surges:** Auto-generated hypotheses when IVI positive deviation > configurable sigma and TAM > threshold.
- **Threat Alerts:** Economic shocks, regulatory motions, algorithm updates exceeding risk threshold.
- **Channel Drift Maps:** Visual + data representation of audience migration (search → social, paid → organic).
- **Revenue Impact Projections:** Basic scenario modeling tying IVI + channel drift to pipeline deltas by vertical.
- **Client-Specific Readouts:** Personalized slices triggered by client tags (sector, revenue band, strategic horizon).
- **Charter-Standard Intelligence Briefs:** Every alert logs governance metadata (source, UID, reviewer) for SRR.

These outputs are events, not long-form PDFs; each one triggers reflex DAG nodes and optional Teamwork tasks.

---

## 5. Wiring Across MAOS

```
Signal Harvester → Mesh Normalizer → Industry Event Bus → Reflex DAG → Teamwork / Client Portal → Custodian Hub
```

### 5.1 Signal Harvester
- Connector drivers fetch content, dedupe, attach provenance.
- Store raw packets in `/data/harvester/YYYY-MM-DD/<source>.jsonl`.
- Each packet gets UID + SHA for Custodian audit.

### 5.2 Mesh Normalizer
- Transforms raw packets into `IndustrySignal` objects (schema below).
- Classifies: domain (e.g., Search, Regulatory), sector, geography, impact vector (demand, supply, platform).
- Applies sentiment + velocity scoring.
- Enriches with client matrix tags (from `teamwork.json` or upcoming CRM adapter).

### 5.3 Industry Event Bus
- Publishes normalized signals to `industry-events.jsonl` and in-memory dispatcher.
- Hooks into existing orchestration by emitting `HandoffEvent` records via `enqueueHandoff`, which already persists to `handoff/queue.jsonl` for downstream relays.

```11:24:src/services/orchestration/enqueueHandoff.ts
export async function enqueueHandoff(event: HandoffEvent): Promise<{ success: boolean; id: string }> {
  ...
  fs.appendFileSync(queueFile, JSON.stringify(record) + '\n', { encoding: 'utf8' });
}
```

### 5.4 Reflex DAG & Teamwork Integration
- Reflex DAG consumes bus topics, decides whether to:
  - Open Teamwork tasks (e.g., “SEO team: validate rumored Google core update”).
  - Notify Notion Relay / Prime Agents via existing adapters.
- Conversation ingestion already lands JSONL (`conversations/events.jsonl`), so reflex narratives can append there for full-thread synthesis.

```10:18:src/services/conversations/ingestEvent.ts
fs.appendFileSync(file, JSON.stringify(record) + '\n', { encoding: 'utf8' });
```

### 5.5 Client Portal + Custodian Hub
- Portal widgets subscribe to IVI, Channel Drift, and Opportunity events filtered per client.
- Every published event writes to Custodian Hub (immutable log + signer). Include SRR fields: UID, source, evidence locator, reviewer, decision.

---

## 6. Data Contracts

### `IndustrySignal` (Normalized Payload)

```json
{
  "uid": "sig_2024-11-24T12:34:56Z_google-core-update",
  "capturedAt": "2024-11-24T12:34:56Z",
  "source": {
    "name": "Google Search Status",
    "type": "platform-update",
    "url": "https://status.search.google.com"
  },
  "classification": {
    "domain": ["Search", "SEO"],
    "sectors": ["Retail", "B2B SaaS"],
    "geos": ["Global"],
    "impactVector": ["Demand", "Channel"]
  },
  "metrics": {
    "volatilityScore": 0.82,
    "confidence": 0.71,
    "sentiment": -0.32
  },
  "llm_surface": {
    "modelVendors": ["OpenAI", "Anthropic"],
    "capabilityTags": ["search-augmentation"]
  },
  "clientMatrix": [
    {
      "clientId": "TW-ACME-RE",
      "relevance": 0.91,
      "notes": "Core traffic mix 70% organic"
    }
  ],
  "attachments": [
    {
      "type": "evidence",
      "uri": "s3://custodian/industry/google-core-update-2024-11-24.pdf",
      "checksum": "sha256:..."
    }
  ]
}
```

### `IndustryAlert` (Derived Output)

Contains alert type (`IVI`, `Opportunity`, `Threat`), delta metrics, recommended reflex action, SLA, and Teamwork mapping (project/tasklist default).

---

## 7. Implementation Plan (v1)

| Phase | Goal | Key Tasks | Owner Signals |
| --- | --- | --- | --- |
| **P0 – Scaffolding (Day 0–1)** | Repo-ready foundations | - Create `/data/harvester` + `/data/mesh` scaffolds<br>- Define `IndustrySignal` TypeScript model<br>- Add placeholder service `src/services/industry/emitIndustrySignal.ts` for bus writes | AUX |
| **P1 – Harvest & Normalize (Day 2–5)** | First 5 connectors live | - Implement RSS/HTTP harvester runner<br>- Add source adapters (MarTech, Google Search, Reddit Trending, LLM Releases, Sector feed template)<br>- Store raw JSONL + normalized output with classification heuristics | AUX + Prime QA |
| **P2 – Event Bus + Reflex Wiring (Day 6–8)** | Alerts flow into Reflex | - Build `src/services/industry/publishAlert.ts` to emit `HandoffEvent` payloads<br>- Extend `enqueueHandoff` consumer config to tag `industry` origin<br>- Add Reflex DAG node spec (Opportunity, Threat) | AUX + Prime |
| **P3 – Client Portal Surfaces (Day 9–11)** | IVI + Drift visible | - Create API stub (GraphQL/REST) for portal widget<br>- Write `Charter-Standard Intelligence Brief` template<br>- Connect Custodian logging (UID, SHA) | Portal Squad |
| **P4 – Governance Hardening (Day 12–14)** | Audit-ready | - Add SRR metadata enforcement<br>- Integrate Custodian Hub signer<br>- Run failover drill + Conversation Review | Custodian |

Backlog after v1: advanced ML scoring, automated revenue projections, sector-specific NLP prompts, streaming connectors (webhooks, Pub/Sub).

---

## 8. Activation Checklist

1. **Install** – Merge scaffolding PR + deploy harvester runners.
2. **Wire** – Point harvester outputs to normalizer; enable event bus + reflex DAG nodes.
3. **Activate** – Start cron/scheduler, monitor first IVI run, verify Teamwork tasks auto-open.
4. **Fold Into Reflex** – Update orchestrator DAG manifest so Opportunity/Threat nodes subscribe to `industry.*` topics.
5. **Document via Custodian Hub** – Log deployment, attach evidence, capture SRR IDs.

---

## 9. Governance & Observability

- **Evidence binder:** Raw packet storage + SHA ensures each alert references immutable source evidence.
- **Conversation Review:** Reflex explanations appended to conversation log so syntheses include why tasks fired.
- **Telemetry:** Track connector latency, normalization throughput, alert precision/recall, false positives.
- **Fail-safes:** Rate-limit connectors, fallback to cached IVI when feed outage occurs, alert on stale data.

---

## 10. Immediate Next Actions

1. Approve scaffolding PR for `IndustrySignal` models + services.
2. Stand up 3 highest-signal harvesters (Google Search, LLM releases, Reddit trending) to seed IVI baseline.
3. Define Reflex rules of engagement (thresholds, assignment defaults) so tasks created through Teamwork align with Charter SLAs.
4. Register deployment in Custodian Hub and update the Client Portal spec to include IVI + Channel Drift widgets.

Charter on. Wire the mesh, and MAOS breathes the atmosphere around every client move.
