# Charter-Standard Repository Remediation

**Automated security remediation for Activ8-AI repositories**

## Overview

This tooling provides Charter-standard automation to:
- Make RED repositories private
- Purge secrets from git history
- Enforce .gitignore rules
- Remove tracked risky artifacts
- Disable GitHub Actions (optional)

## Quick Start

### Prerequisites

1. **Notion Integration Token**
   - Go to: https://www.notion.so/my-integrations
   - Create integration or use existing
   - Copy Internal Integration Token
   - Share Secrets Registry page with integration

2. **Notion Secrets Registry**
   - Must contain `GITHUB_TOKEN` entry
   - Token needs scopes: `repo`, `admin:org`, `workflow`
   - Generate token at: https://github.com/settings/tokens/new

### Usage

```bash
# Set Notion token (required first time)
export NOTION_TOKEN="secret_xxxxxxxxxxxx"

# DRY RUN (safe preview - shows what would happen)
./scripts/run_remediation.sh --private --purge --gitignore --disable-actions

# APPLY to Teamwork-MCP only
./scripts/run_remediation.sh --apply --repo Teamwork-MCP --private --purge --gitignore --disable-actions

# APPLY to all public repos
./scripts/run_remediation.sh --apply --private --purge --gitignore --disable-actions
```

## How It Works

### 1. Fetch Secrets from Notion (`fetch_notion_secrets.py`)
- Connects to Notion Secrets Registry using NOTION_TOKEN
- Downloads GITHUB_TOKEN and other secrets
- Caches to `configs/notion_secrets.json` (gitignored)
- Can use cached secrets on subsequent runs

### 2. Authenticate GitHub CLI (`run_remediation.sh`)
- Loads GITHUB_TOKEN from cache
- Authenticates `gh` CLI
- Validates authentication

### 3. Run Remediation (`public_repo_remediate.sh`)
- Enumerates public repositories
- Classifies risk (GREEN/YELLOW/RED)
- Applies remediation based on flags:
  - `--private`: Make RED repos private
  - `--purge`: Purge secrets from git history
  - `--gitignore`: Enforce .gitignore rules
  - `--disable-actions`: Disable GitHub Actions
- Generates audit logs and summary

## Files Purged from History

When `--purge` is used, these patterns are removed from ALL commits:

**Secrets:**
- `.secrets.cache.json`, `.secrets*.json`
- `.env`, `.env.*`
- `configs/notion_secrets.json`
- `*credentials*.json`, `*token*.json`
- `*secret*.json`, `*secrets*.json`
- `*.pem`, `*.p12` (certificates)
- `*service-account*.json`

**Artifacts:**
- `__pycache__/`, `*.pyc` (Python bytecode)
- `*.db`, `*.sqlite`, `*.sqlite3` (databases)
- `*ledger*.db`
- `*.jsonl`, `*transcript*` (logs)

## Risk Classification

- **GREEN**: No workflows, no sensitive files
- **YELLOW**: Has workflows (`.github/workflows/`)
- **RED**: Contains files matching sensitive patterns

## Output

After each run:
```
~/repo-audits/remediate-<timestamp>/
├── summary.txt           # Risk classification per repo
├── public_repos.txt      # List of public repos
├── logs/                 # Detailed operation logs
└── <repo-name>/          # Cloned repos (when --apply)
```

## Caching

Once secrets are fetched from Notion:
```bash
# Use cached secrets (skip Notion API call)
./scripts/fetch_notion_secrets.py --use-cache

# Get specific token for export
export GITHUB_TOKEN=$(./scripts/fetch_notion_secrets.py --use-cache --output-token GITHUB_TOKEN)
```

## Security Notes

- `configs/notion_secrets.json` is gitignored (never committed)
- NOTION_TOKEN required only for first fetch
- Subsequent runs use cached secrets
- History rewrite requires force-push (changes commit SHAs)
- All team members must re-clone after history purge

## Troubleshooting

### "NOTION_TOKEN required"
```bash
export NOTION_TOKEN="secret_xxxxx"
```

### "GITHUB_TOKEN not found in secrets"
Ensure Notion Secrets Registry has:
- Entry named: `GITHUB_TOKEN`
- Value: Valid GitHub PAT with required scopes

### "Failed to authenticate gh CLI"
Token may be expired. Generate new token at:
https://github.com/settings/tokens/new

### "No public repos found"
Either:
- All repos are already private (good!)
- GitHub auth failed
- No access to Activ8-AI organization

## Support

- Charter compliance: codex@activ8ai.app
- Security incidents: See SECURITY.md
- Bug reports: https://github.com/Activ8-AI/Teamwork-MCP/issues
