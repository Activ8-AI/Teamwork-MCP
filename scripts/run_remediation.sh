#!/usr/bin/env bash
#
# Charter-standard remediation runner
#
# Fetches secrets from Notion, authenticates gh CLI, and runs repository remediation.
#
# Usage:
#   # DRY RUN (safe preview)
#   ./scripts/run_remediation.sh
#
#   # APPLY to Teamwork-MCP only
#   ./scripts/run_remediation.sh --apply --repo Teamwork-MCP
#
#   # APPLY to all public repos
#   ./scripts/run_remediation.sh --apply
#
# Prerequisites:
#   - NOTION_TOKEN environment variable set
#   - OR: configs/notion_secrets.json with GITHUB_TOKEN cached
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

log() {
  local level="$1"; shift
  printf "[%s] %s\n" "$level" "$*" >&2
}

# Check if running from repo root
cd "$REPO_ROOT"

# ---- Step 1: Fetch secrets from Notion ----
log "INFO" "Fetching secrets from Notion Secrets Registry..."

if [[ -n "${NOTION_TOKEN:-}" ]]; then
  log "INFO" "Using NOTION_TOKEN from environment"
  python3 "$SCRIPT_DIR/fetch_notion_secrets.py" >/dev/null
elif [[ -f configs/notion_secrets.json ]]; then
  log "INFO" "Using cached secrets from configs/notion_secrets.json"
else
  log "ERROR" "No NOTION_TOKEN in environment and no cached secrets found"
  log "ERROR" ""
  log "ERROR" "To fix:"
  log "ERROR" "  1. Get Notion API token from https://www.notion.so/my-integrations"
  log "ERROR" "  2. Share Secrets Registry page with the integration"
  log "ERROR" "  3. Run: export NOTION_TOKEN='secret_xxxx'"
  log "ERROR" "  4. Run this script again"
  exit 1
fi

# ---- Step 2: Load GITHUB_TOKEN ----
GITHUB_TOKEN=""

if [[ -f configs/notion_secrets.json ]]; then
  GITHUB_TOKEN=$(python3 -c "import json; data=json.load(open('configs/notion_secrets.json')); print(data.get('GITHUB_TOKEN', ''))" 2>/dev/null || echo "")
fi

if [[ -z "$GITHUB_TOKEN" ]]; then
  log "ERROR" "No GITHUB_TOKEN found in secrets"
  log "ERROR" "Ensure Notion Secrets Registry contains a GITHUB_TOKEN entry"
  exit 1
fi

log "INFO" "✓ Found GITHUB_TOKEN"

# ---- Step 3: Authenticate gh CLI ----
log "INFO" "Authenticating GitHub CLI..."

export GITHUB_TOKEN
if echo "$GITHUB_TOKEN" | gh auth login --with-token 2>/dev/null; then
  log "INFO" "✓ GitHub CLI authenticated"
else
  log "ERROR" "Failed to authenticate gh CLI"
  log "ERROR" "Token may be invalid or expired"
  exit 1
fi

# Verify auth worked
if ! gh auth status >/dev/null 2>&1; then
  log "ERROR" "gh auth status failed after login"
  exit 1
fi

# ---- Step 4: Run remediation script ----
REMEDIATION_SCRIPT="$HOME/repo-audits/bin/public_repo_remediate.sh"

if [[ ! -f "$REMEDIATION_SCRIPT" ]]; then
  log "ERROR" "Remediation script not found: $REMEDIATION_SCRIPT"
  log "ERROR" "Expected to be installed by remediation automation setup"
  exit 1
fi

log "INFO" "Running remediation script..."
log "INFO" "Args: $*"
log "INFO" ""

# Pass all arguments to remediation script
exec "$REMEDIATION_SCRIPT" "$@"
