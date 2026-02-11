# Activ8-AI GitHub Account — Day-1 Orientation Review

**Date:** 2026-02-09
**Reviewer:** ClaudeCode Agent (Senior Staff-Level)
**Scope:** Full account scan — all 70 repositories enumerated
**Mode:** Map-making pass. No changes made.

---

## High-Level Impression

This is a **single-product account with a massive fork collection**. The Activ8-AI GitHub organization contains **70 repositories**, of which **68 are forks** and only **2 are original**. The center of gravity is unambiguously **Teamwork-MCP**, a TypeScript MCP server connecting to the Teamwork.com API.

The fork collection forms a reference library across the AI/ML agent ecosystem (MCP SDKs, LangChain, CrewAI, OpenAI agents, Google ADK, Docker tooling, etc.). These forks show no evidence of significant upstream divergence — they appear to be bookmarks or staging copies rather than active development forks.

**Overall health:** The core product repo (Teamwork-MCP) is actively developed with CI, tests, and governance docs. However, it carries 15 open PRs with known blockers, and the account is heavily cluttered with untouched forks that obscure signal.

**Account type:** Product account with reference/learning library.

---

## Repository Landscape Snapshot

### Likely Production (2 repos)

| Repo | Type | Language | Last Active | Notes |
|------|------|----------|-------------|-------|
| **Teamwork-MCP** | Original | TypeScript | Feb 9, 2026 | Core product. 182 commits, 15 open PRs, CI active, MIT license |
| **mcp-1** | Fork | Go | Feb 5, 2026 | Fork of upstream Teamwork/mcp (Go implementation). May serve as reference or alternative deployment |

### Active Work / Recently Touched Forks (12 repos)

These forks were updated within the last 2 weeks (after Jan 28, 2026), suggesting active reference use:

| Repo | Upstream | Language | Last Active |
|------|----------|----------|-------------|
| elevenlabs-mcp | elevenlabs/elevenlabs-mcp | Python | Feb 9, 2026 |
| docker-Desktop-Commander-MCP | wonderwhy-er/DesktopCommanderMCP | JavaScript | Feb 9, 2026 |
| agents.md | agentsmd/agents.md | TypeScript | Feb 9, 2026 |
| modelcontextprotocol | modelcontextprotocol/modelcontextprotocol | TypeScript | Feb 9, 2026 |
| microsoft-mcp | microsoft/mcp | C# | Feb 7, 2026 |
| inspector | modelcontextprotocol/inspector | TypeScript | Feb 6, 2026 |
| atomic-agents | BrainBlend-AI/atomic-agents | Python | Feb 5, 2026 |
| airtable-oauth-example | Airtable/airtable-oauth-example | JavaScript | Feb 5, 2026 |
| fastmcp | jlowin/fastmcp | Python | Feb 5, 2026 |
| servers | modelcontextprotocol/servers | TypeScript | Feb 4, 2026 |
| notion-mcp-server | makenotion/notion-mcp-server | TypeScript | Feb 4, 2026 |
| chatgpt-codex | openai/codex | Rust | Feb 3, 2026 |

### Experiments / Spikes (6 repos)

| Repo | Type | Notes |
|------|------|-------|
| **Codex-Op** | Original | **Empty repository.** No files, no commits, no README. Placeholder only |
| **gh-repo-clone-openai-openai-agents-python** | Unknown | Near-empty. Only `.github/workflows` dir, 1 commit. Name suggests a botched `gh repo clone` |
| fathom-video-crm-status-sync | Fork | Backend design doc for video CRM sync. 6 commits, docs-only |
| codespaces-blank | Fork | GitHub's blank Codespaces template. No custom content |
| opengpts | Fork | LangChain OpenGPTs. No evident customization |
| generative-ai | Fork | Google's generative AI samples. Reference copy |

### Reference Library Forks — Inactive (50 repos)

These are forks with no evidence of modification beyond upstream, last touched before Jan 28, 2026. Grouped by domain:

**MCP Ecosystem (12)**
- python-sdk, typescript-sdk, servers, inspector, modelcontextprotocol
- github-mcp-server, postman-mcp-server, hub-mcp, aks-mcp
- google-analytics-mcp, firecrawl-mcp-server, browser-mcp

**AI Agent Frameworks (9)**
- langchain, langchainjs, langgraph, crewAI
- openai-agents-python, adk-python, adk-samples, agent-framework
- agentic-system-prompts

**Google Cloud / Research (5)**
- google-cloud-platform-agent-starter-pack, google-research
- Google-Cloud-Platform_cloud-code-intellij, local-deep-researcher, pyglove

**Developer Tooling (8)**
- n8n, gemini-cli, puppeteer, copilot-cli, uv
- typescript-eslint, -gitlens_gk-cli, skaffold

**Infrastructure / Docker (4)**
- compose-for-agents, docker-mcp-registry, gitleaks, semanticworkbench

**HubSpot (4)**
- hubspot-project-components, hubspot-cms-vscode, HubSpot-public-api-spec-collection, hubspot-api-python

**Other (5)**
- openai-cookbook, linear, slack-client, blocks, LLaVA-Med
- MongoDB-ADK-Agents, CoML, airtable.js, hbase, genai-stack

---

## Immediate Red Flags

### BLOCKER-level

1. **Teamwork-MCP has 15 open PRs with known compilation blockers (PR #42/#33)**
   - PRs #33 and #42 are mega-consolidation PRs (38 files, 3400+ lines each) with reviewer-identified syntax errors, duplicate function definitions, and broken pre-commit hooks
   - These PRs have been open since Jan 29 / Feb 2, 2026 — over a week with no resolution
   - 8 follow-up "fix" PRs (#34-#40, #43-#45) are stacked on these broken bases
   - **Risk:** PR backlog is compounding. The longer this sits, the harder the merge becomes

2. **Unauthenticated webhook endpoint enabled by default**
   - `src/servers/notion-relay-server.ts:31` — `allowUnauthenticatedWhenUnset` defaults to `true`
   - If deployed without `RELAY_SECRET` or `RELAY_TOKEN` set, all webhook endpoints accept unauthenticated requests
   - **Risk:** Production data exposure if deployed with default config

### HIGH-level

3. **Dependency vulnerability: `@modelcontextprotocol/sdk` cross-client data leak**
   - PR #46 (dependabot) bumps to 1.26.0 to fix GHSA-345p-7cg4-v4c7 (shared server/transport instance leaks cross-client response data)
   - Currently on 1.25.3, which is affected
   - **Risk:** Data leakage between MCP clients sharing a server instance

4. **`.gitignore` has extensive duplicate entries**
   - Lines 15/19: `.secrets.cache.json` duplicated
   - Lines 16/21: `configs/notion_secrets.json` duplicated
   - Lines 67-71 / 76-80: Python patterns duplicated (*.so, *.egg, *.egg-info/, dist/)
   - **Risk:** Low immediate risk, but signals sloppy housekeeping and lack of review rigor

5. **`tests/conftest.py` has code quality issues flagged but unresolved**
   - Unused `import sqlite3` (line 2)
   - `import os` buried inside function body (line 18) violating PEP 8
   - PRs #34 and #36 fix these but are stacked on blocked base PR #33

### MEDIUM-level

6. **Empty repository: `Codex-Op`**
   - Created Nov 2025, still empty. No README, no commits, no purpose stated
   - **Risk:** Organizational noise. If it has a purpose, it's invisible

7. **Botched clone: `gh-repo-clone-openai-openai-agents-python`**
   - Name suggests a `gh repo clone` command was accidentally turned into a repo name
   - Near-empty (1 commit, only `.github/workflows`), has 2 open PRs somehow
   - **Risk:** Confusing and unprofessional if account is public-facing

8. **`src/index.ts` double-calls `validateResponse()` (lines 148 + 153)**
   - Response is validated in catch block, then validated again unconditionally
   - Not a bug per se, but unnecessary work and confusing intent

9. **23 lines of commented-out prompt code in `src/index.ts` (lines 162-185)**
   - Dead code that's been sitting since initial development
   - Either implement or remove

10. **Duplicate API URL construction logic**
    - `src/utils/config.ts` and `src/services/core/apiClient.ts` both implement nearly identical `constructApiUrl` / `getApiUrlForVersion` logic
    - Maintenance risk if one is updated and the other isn't

---

## Top 5 "Start Here" Repositories

### 1. **Teamwork-MCP** (CRITICAL — the product)
- **Why:** This is the only original repo with real code and active development. Everything else orbits it
- **State:** 15 open PRs, CI active, known blockers in consolidation PRs
- **Next action:** Triage and resolve PR backlog, starting with the dependency security fix (PR #46)

### 2. **mcp-1** (HIGH — alternative implementation)
- **Why:** This is the upstream Go implementation of the same Teamwork MCP concept. Understanding whether this fork serves as reference, backup, or alternative deployment matters for architectural decisions
- **Next action:** Determine if this fork has any custom modifications or if it's purely a mirror

### 3. **notion-mcp-server** (MEDIUM — integration dependency)
- **Why:** Teamwork-MCP has a Notion relay system. The official Notion MCP server fork may indicate planned integration or was used as reference for the relay implementation
- **Next action:** Cross-reference with Teamwork-MCP's notion-relay-server to understand dependency

### 4. **docker-Desktop-Commander-MCP** (MEDIUM — operational tooling)
- **Why:** Most recently active fork (Feb 9). If it's being used for local development/agent orchestration, it matters for understanding the operational environment
- **Next action:** Determine if this is actively used or just bookmarked

### 5. **Codex-Op** (LOW priority, HIGH signal)
- **Why:** One of only 2 original repos, but completely empty. Its name suggests it was intended to be something ("Codex Operations"?). Understanding intent helps map the roadmap
- **Next action:** Ask the owner: keep, populate, or delete?

---

## Recommended Next Step

**Merge PR #46 (dependabot security fix) into Teamwork-MCP immediately.**

This is the highest-leverage move because:

1. It fixes a **known security vulnerability** (cross-client data leak in MCP SDK) with a single dependency bump from 1.25.3 to 1.26.0
2. It is a **clean, automated, single-file change** from dependabot — minimal risk
3. It is **independent of the blocked PR #33/#42 chain** — it targets `main` directly
4. It unblocks the security posture conversation before tackling the larger PR backlog

**After that:** Triage the PR backlog. Close PRs #33 as superseded by #42. Close the stacked fix PRs (#34-#40) as they target a dead branch. Address the fixes directly in #42 or as standalone PRs against `main`. Then merge the small cleanups (#43-#45) individually.

---

## Appendix: Complete Repository Inventory (70 repos)

### Original Repositories (2)

| # | Repo | Language | Status | Last Active |
|---|------|----------|--------|-------------|
| 1 | Teamwork-MCP | TypeScript | Active | Feb 9, 2026 |
| 2 | Codex-Op | — | Empty | Nov 23, 2025 |

### Forked Repositories (68)

| # | Repo | Upstream Domain | Language | Last Active |
|---|------|----------------|----------|-------------|
| 1 | elevenlabs-mcp | ElevenLabs | Python | Feb 9, 2026 |
| 2 | docker-Desktop-Commander-MCP | wonderwhy-er | JavaScript | Feb 9, 2026 |
| 3 | agents.md | agentsmd | TypeScript | Feb 9, 2026 |
| 4 | modelcontextprotocol | MCP org | TypeScript | Feb 9, 2026 |
| 5 | microsoft-mcp | Microsoft | C# | Feb 7, 2026 |
| 6 | inspector | MCP org | TypeScript | Feb 6, 2026 |
| 7 | mcp-1 | Teamwork | Go | Feb 5, 2026 |
| 8 | atomic-agents | BrainBlend-AI | Python | Feb 5, 2026 |
| 9 | airtable-oauth-example | Airtable | JavaScript | Feb 5, 2026 |
| 10 | fastmcp | jlowin | Python | Feb 5, 2026 |
| 11 | servers | MCP org | TypeScript | Feb 4, 2026 |
| 12 | notion-mcp-server | Notion | TypeScript | Feb 4, 2026 |
| 13 | chatgpt-codex | OpenAI | Rust | Feb 3, 2026 |
| 14 | opengpts | LangChain | RTF | Feb 3, 2026 |
| 15 | generative-ai | Google | Jupyter | Feb 3, 2026 |
| 16 | google-cloud-platform-agent-starter-pack | Google | Python | Jan 30, 2026 |
| 17 | openai-cookbook | OpenAI | Jupyter | Jan 30, 2026 |
| 18 | gemini-cli | Google | TypeScript | Jan 29, 2026 |
| 19 | n8n | n8n-io | TypeScript | Jan 28, 2026 |
| 20 | langchainjs | LangChain | TypeScript | Jan 28, 2026 |
| 21 | langgraph | LangChain | Python | Jan 28, 2026 |
| 22 | semanticworkbench | Microsoft | Python | Jan 28, 2026 |
| 23 | hbase | Apache | Java | Jan 28, 2026 |
| 24 | LLaVA-Med | microsoft | Python | Jan 28, 2026 |
| 25 | fathom-video-crm-status-sync | tongzhou0616 | — | Jan 28, 2026 |
| 26 | skaffold | GoogleContainerTools | Go | Jan 28, 2026 |
| 27 | google-analytics-mcp | — | Python | Jan 20, 2026 |
| 28 | uv | astral-sh | Rust | Jan 16, 2026 |
| 29 | copilot-cli | GitHub | Shell | Jan 16, 2026 |
| 30 | firecrawl-mcp-server | mendableai | JavaScript | Jan 14, 2026 |
| 31 | MongoDB-ADK-Agents | MongoDB | Python | Dec 26, 2025 |
| 32 | hub-mcp | Docker | TypeScript | Dec 26, 2025 |
| 33 | linear | Linear | TypeScript | Dec 26, 2025 |
| 34 | typescript-eslint | typescript-eslint | TypeScript | Dec 26, 2025 |
| 35 | genai-stack | docker | Python | Dec 26, 2025 |
| 36 | -gitlens_gk-cli | GitKraken | Other | Dec 26, 2025 |
| 37 | crewAI | crewAIInc | Python | Nov 27, 2025 |
| 38 | compose-for-agents | Docker | TypeScript | Nov 27, 2025 |
| 39 | docker-mcp-registry | Docker | Go | Nov 27, 2025 |
| 40 | gitleaks | gitleaks | Go | Nov 24, 2025 |
| 41 | python-sdk | MCP org | Python | Nov 24, 2025 |
| 42 | typescript-sdk | MCP org | TypeScript | Nov 24, 2025 |
| 43 | vscode-jupyter | Microsoft | TypeScript | Nov 24, 2025 |
| 44 | slack-client | — | Java | Nov 24, 2025 |
| 45 | openai-agents-python | OpenAI | Python | Nov 24, 2025 |
| 46 | langchain | LangChain | Python | Nov 24, 2025 |
| 47 | adk-python | Google | Python | Nov 24, 2025 |
| 48 | adk-samples | Google | Python | Nov 24, 2025 |
| 49 | agent-framework | — | Python | Nov 24, 2025 |
| 50 | airtable.js | Airtable | JavaScript | Nov 24, 2025 |
| 51 | postman-mcp-server | Postman | TypeScript | Nov 24, 2025 |
| 52 | codespaces-blank | GitHub | — | Nov 24, 2025 |
| 53 | github-mcp-server | GitHub | Go | Nov 24, 2025 |
| 54 | hubspot-project-components | HubSpot | TypeScript | Nov 21, 2025 |
| 55 | puppeteer | Google | TypeScript | Nov 16, 2025 |
| 56 | blocks | — | TypeScript | Nov 15, 2025 |
| 57 | hubspot-cms-vscode | HubSpot | TypeScript | Nov 15, 2025 |
| 58 | google-research | Google | Jupyter | Nov 7, 2025 |
| 59 | aks-mcp | Azure | Go | Nov 6, 2025 |
| 60 | gh-repo-clone-openai-openai-agents-python | — | — | Nov 1, 2025 |
| 61 | pyglove | Google | Python | Oct 1, 2025 |
| 62 | HubSpot-public-api-spec-collection | HubSpot | — | Sep 29, 2025 |
| 63 | hubspot-api-python | HubSpot | Python | Sep 9, 2025 |
| 64 | local-deep-researcher | LangChain | Python | Aug 8, 2025 |
| 65 | agentic-system-prompts | — | Jinja | Aug 4, 2025 |
| 66 | browser-mcp | — | TypeScript | Apr 24, 2025 |
| 67 | CoML | Microsoft | Python | Oct 8, 2024 |
| 68 | Google-Cloud-Platform_cloud-code-intellij | Google | — | Sep 16, 2024 |

**No repositories were skipped.** All 70 repos (2 original + 68 forks) are accounted for above.

---

## Appendix: Teamwork-MCP Open PR Summary (15 PRs)

| PR | Title | Author | Base | Status | Verdict |
|----|-------|--------|------|--------|---------|
| #48 | docs: conversation meta mega codex | Activ8-AI | main | Open | APPROVE WITH CHANGES — security issues in embedded code samples |
| #47 | Add canonical Claude/Notion webhook routes | Activ8-AI | main | Open | APPROVE WITH CHANGES — needs legacy alias tests |
| #46 | bump @modelcontextprotocol/sdk 1.25.3 → 1.26.0 | dependabot | main | Open | **APPROVE** — security fix, merge immediately |
| #45 | Remove duplicate publish workflow badge | Copilot | PR #42 branch | Open | APPROVE — trivial, clean |
| #44 | Remove duplicate .gitignore pattern custody/*.db | Copilot | PR #42 branch | Open | APPROVE — trivial, clean |
| #43 | Remove duplicate .gitignore entries for secrets | Copilot | PR #42 branch | Open | APPROVE — trivial, clean |
| #42 | Resolve all PRs: security, features, automation | Activ8-AI | main | Open | **BLOCK MERGE** — compilation errors, duplicate definitions, broken hooks |
| #40 | Fix npm-audit pre-commit hook | Copilot | PR #33 branch | Open | APPROVE — correct fix, but stacked on dead branch |
| #39 | Improve error diagnostics in Notion relay | Copilot | PR #33 branch | Open | APPROVE WITH CHANGES — logs sensitive data |
| #38 | Replace deprecated actions/create-release@v1 | Copilot | PR #33 branch | Open | APPROVE — correct migration |
| #37 | Add GHCR auth to release workflow | Copilot | PR #33 branch | Open | APPROVE — necessary fix |
| #36 | Move os import to top of conftest.py | Copilot | PR #33 branch | Open | APPROVE — PEP 8 compliance |
| #35 | Fix MCP SDK version mismatch | Copilot | PR #33 branch | Open | APPROVE — version alignment |
| #34 | Remove unused sqlite3 import | Copilot | PR #33 branch | Open | APPROVE WITH CHANGES — includes .pyc artifacts |
| #33 | Resolve all PRs: security, features, automation | Activ8-AI | main | Open | **BLOCK MERGE** — superseded by #42, close this |

### PR Dependency Graph

```
main
├── PR #48 (docs codex) — independent, targets main
├── PR #47 (webhook routes) — independent, targets main
├── PR #46 (dependabot security) — independent, targets main ← MERGE FIRST
├── PR #42 (mega consolidation v2) — targets main, BLOCKED
│   ├── PR #45 (fix: duplicate badge)
│   ├── PR #44 (fix: duplicate gitignore db)
│   └── PR #43 (fix: duplicate gitignore secrets)
└── PR #33 (mega consolidation v1) — targets main, SUPERSEDED
    ├── PR #40 (fix: npm-audit hook)
    ├── PR #39 (fix: error diagnostics)
    ├── PR #38 (fix: deprecated action)
    ├── PR #37 (fix: GHCR auth)
    ├── PR #36 (fix: os import)
    ├── PR #35 (fix: SDK version mismatch)
    └── PR #34 (fix: unused import)
```

### Recommended PR Resolution Order

1. **Merge** PR #46 (security fix — independent, clean)
2. **Close** PR #33 as superseded by #42
3. **Close** PRs #34-#40 (stacked on dead #33 branch)
4. **Fix** PR #42's blockers (duplicate functions, syntax errors, broken hook)
5. **Merge** PR #42 once fixed (incorporates all the fixes from #34-#40)
6. **Merge** PRs #43-#45 (small cleanups, rebase if needed after #42)
7. **Merge** PR #47 (webhook routes — independent feature)
8. **Merge** PR #48 after addressing embedded code security issues

---

*This is a Day-1 map-making pass. No changes were made to any repository.*
