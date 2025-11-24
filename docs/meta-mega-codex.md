# Meta Mega Codex — Multi-Agent Charter Standard Execution

This codex unifies every governance and execution layer—doctrine, policies, governors, resilience, logging, workflows, routing, and operations—into a single artifact that can be referenced during audits or activation sequences.

---

## Layer 1: Charter Doctrine
- Sovereign boundaries enforced at runtime
- Determinism via pinned versions and caching
- Audit immutability with append-only logs, UTC timestamps, artifact uploads
- Resilience expectations: failover states, backoff retries, watchdog escalation
- Evidence coherence through aggregated JSON binders and dashboards
- Zero drift via version-locked workflows

## Layer 2: Policies
**Domain policies**
- `activ8_domain_policy.json`
- `lma_domain_policy.json`
- `personal_domain_policy.json`

**Copilot policies**
- `activ8-ai-copilot.json`
- `lma-copilot.json`
- `personal-copilot.json`

## Layer 3: Governors
- `activ8_governor.py` — policy-enforced sweep for Activ8 AI
- `lma_governor.py` — policy-enforced sweep for LMAOS
- `personal_governor.py` — policy-enforced sweep for PERSONAL

## Layer 4: Resilience
- `resilient_governor_runner.py` — structured failover orchestration with retries/backoff
- `watchdog.py` — stale detection, escalation hooks, paging
- `governor_evidence_aggregator.py` — aggregated evidence and dashboard updates

## Layer 5: Logging Spine
- `custodian_log_binder.py` — append-only custodian log
- `genesis_trace.py` — append-only trace log

## Layer 6: Router
- `mcp_governor_router.py` — routes Activ8, LMA, and Personal governors

## Layer 7: Workflows
- `.github/workflows/activ8-governor-sweep.yml`
- `.github/workflows/lma-governor-sweep.yml`
- `.github/workflows/personal-governor-sweep.yml`
- `.github/workflows/governor-watchdog.yml`
- `.github/workflows/governor-evidence-aggregation.yml`
- `.github/workflows/governor-failover.yml`

_All GH Actions workflows pinned to `ubuntu-22.04`, `actions/checkout@v4.1.0`, `actions/setup-python@v4.7.0`, with pip caching and conflict-safe commits._

## Layer 8: Operations
**Local run commands**
- `PAT_ACTIV8_AI=<token> python activ8_governor.py`
- `PAT_LMA=<token> python lma_governor.py`
- `PAT_PERSONAL=<token> python personal_governor.py`
- `PAT_ACTIV8_AI=<token> PAT_LMA=<token> PAT_PERSONAL=<token> python resilient_governor_runner.py`
- `python watchdog.py`
- `python governor_evidence_aggregator.py`

**Invocation phrase**
- “Charter On — Execute Meta Mega Codex.”
- “Run Governors — Activ8 AI, LMAOS, PERSONAL — Charter Standard Execution.”

---

Reference this codex whenever activating, auditing, or extending the multi-agent governors so every layer stays aligned with Charter Standard execution.
