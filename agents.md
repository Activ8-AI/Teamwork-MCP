# Agent Hub — Web Analysis Stack

This file is the canonical routing table for the Competitive Intelligence Engine v1. It links MAOS Reflex triggers to the six web-analysis agents and documents their contracts, confidence scoring, and governance hooks.

## Assignment Rules

| Agent | When Assigned | Primary Objective | Escalation |
| --- | --- | --- | --- |
| `surveillance_agent` | Every UI-facing delta (homepage, nav, CTA, modals) | Capture before/after state, tag sentiment | Escalate to `signal_harvester_agent` when severity >= medium |
| `research_agent` | Funding, org, macro sentiment, regulatory changes | Provide context pack + sources for briefs | Escalate to Prime for Charter memo gaps |
| `competitor_watch_agent` | SEO/PPC/ad-library overlaps & keyword aggression | Quantify overlap %, budget deltas, channel mix | Escalate to Teamwork if overlap > 40% on branded terms |
| `web_crawler_agent` | Structural diffs (pricing, docs, changelog, sitemap) | Produce DOM snapshots + diff artifacts | Escalate to `content_diff_agent` if feature parity detected |
| `signal_harvester_agent` | All merged signals with severity >= medium | Score, normalize, and send Reflex packet | Escalate to Reflex DAG + Teamwork tasks |
| `content_diff_agent` | Release notes, blog posts, docs, pricing copy | Generate semantic diffs vs. client features | Escalate to Strategy Sprint backlog if parity gaps found |

## Trigger Logic

- **Delta severity**: computed by `signal_harvester_agent` from normalized inputs; severity >= `medium` auto-pushes Reflex + Teamwork.
- **Channel monitors**:
  - Pricing endpoints poll every 15 minutes (Orbit) / hourly (Atlas).
  - Blogs, press releases, and documentation trigger on RSS/Atom updates.
  - Social/ad library watchers trigger on engagement spikes (>20% WoW) or new campaign IDs.
- **Custodian hash**: `sha256(clientId|competitorId|timestamp|summary)` stored in every brief for auditability.

## Output Contracts

Each agent produces a typed payload that rolls into the Competitor Intelligence Engine:

| Agent | Output ID | Schema fragment |
| --- | --- | --- |
| `surveillance_agent` | `diffSummary` | `{ "before": "...", "after": "...", "area": "hero|nav|cta", "sentiment": "push|defend|unknown" }` |
| `research_agent` | `contextPack` | `{ "funding": {...}, "hires": [...], "macroSignals": [...] }` |
| `competitor_watch_agent` | `campaignAlert` | `{ "channel": "seo|ppc|social", "overlapPct": 0-1, "budgetEstimate": "$", "keywords": [] }` |
| `web_crawler_agent` | `contentDiff` | `{ "path": "/pricing", "changeType": "copy|structure|asset", "diff": "..." }` |
| `content_diff_agent` | `featureGapAnalysis` | `{ "feature": "...", "clientParity": "lead|lag|equal", "impactScore": 1-5 }` |
| `signal_harvester_agent` | `reflexPacket` | `{ "severity": "info|low|medium|high|critical", "confidence": 0-1, "recommendedActions": [] }` |

## Confidence Scoring

```
confidence = baseWeight(signal) + recencyBoost + corroborationBonus - noisePenalty
```

- `baseWeight` per signal type (pricing=0.3, product=0.25, campaign=0.2, sentiment=0.15, other=0.1).
- `recencyBoost` adds up to 0.2 when corroborated within 24h.
- `corroborationBonus` adds 0.15 when at least two agents observe the same competitor.
- `noisePenalty` subtracts up to 0.25 when evidence lacks source or repeats stale data.

Scores below `0.45` remain in Trend Watch with yellow alert; `>=0.72` qualifies for Reflex tasking; `>=0.85` triggers Prime review.

## Governance Hooks

- Every delta writes a brief to `competitor-intel/briefs/*.md` with Summary → Market Impact → Strategic Implication → Recommended Actions → Governance Notes → Confidence → Custodian hash.
- Reflex queue entry targets `NotionRelay`, `PrimeAgent`, and `ClaudeAgent`. Unknown targets are rejected.
- Teamwork routing uses per-client task list IDs defined in `codex-portal/client-intelligence/competitor-definition-map.json`. Fallback env var: `TEAMWORK_COMP_INTEL_TASKLIST_ID`.
- STOP–RESET–REALIGN: if three consecutive red alerts occur without closure, pause ingestion, notify Prime, and require TAO memo before reactivation.
