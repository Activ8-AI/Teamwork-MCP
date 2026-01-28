#!/usr/bin/env bash
set -euo pipefail

# Charter-standard public repo remediation automation
# - Deterministic ordering
# - Audit-logged outputs
# - Default safe (DRY RUN)
# - Uses: gh, git-filter-repo, jq, git

ORG_DEFAULT="Activ8-AI"

# ---- Modes ----
DRY_RUN=1
DO_PRIVATE=0
DO_PURGE=0
DO_GITIGNORE=0
DO_DISABLE_ACTIONS=0
LIMIT_REPO=""
OUT_DIR=""
ORG="$ORG_DEFAULT"

# ---- Risk patterns (file names) ----
# Anything that should NOT be tracked in public repos.
PURGE_GLOBS=(
  ".secrets.cache.json"
  ".secrets*.json"
  ".env"
  ".env.*"
  "configs/notion_secrets.json"
  "**/__pycache__/*"
  "**/*.pyc"
  "**/*.p12"
  "**/*.pem"
  "**/*service-account*.json"
  "**/*credentials*.json"
  "**/*token*.json"
  "**/*secret*.json"
  "**/*secrets*.json"
  "**/*ledger*.db"
  "**/*.db"
  "**/*.sqlite"
  "**/*.sqlite3"
  "**/*.jsonl"
  "**/*transcript*"
)

# Filenames that should mark repo as RED immediately.
RED_REGEX='\.secrets|secrets|secret|token|apikey|api_key|private|\.pem$|\.p12$|credentials|service-account|sa\.json|\.secrets?\.cache|ledger|jsonl|transcript|webhook|hmac|__pycache__|\.pyc$'

usage() {
  cat <<USAGE
Usage: $(basename "$0") [options]

Options:
  --apply                 Actually perform actions (default is DRY RUN)
  --private               Make RED repos private
  --purge                 Purge risky files from git history (git-filter-repo)
  --gitignore             Inject .gitignore + remove tracked risky artifacts at HEAD
  --disable-actions       Disable GitHub Actions on RED/YELLOW repos
  --repo <name>           Limit to one repo name (e.g., Teamwork-MCP)
  --org <org>             GitHub org/user (default: $ORG_DEFAULT)
  --out <dir>             Output directory (default: ~/repo-audits/remediate-<ts>)

Examples:
  # DRY RUN (safe; prints plan + writes audit files)
  $(basename "$0") --private --purge --gitignore --disable-actions

  # APPLY to Teamwork-MCP only
  $(basename "$0") --apply --repo Teamwork-MCP --private --purge --gitignore --disable-actions
USAGE
}

ts_utc() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

log() {
  local level="$1"; shift
  printf "[%s] %s\n" "$level" "$*" 1>&2
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || { echo "Missing required command: $1" 1>&2; exit 1; }
}

emit_event() {
  # JSONL for audit ingestion
  # Args: repo action detail
  local repo="$1"; shift
  local action="$1"; shift
  local detail="$*"
  printf '{"ts":"%s","org":"%s","repo":"%s","action":"%s","detail":%s}\n' \
    "$(ts_utc)" \
    "$ORG" \
    "$repo" \
    "$action" \
    "$(jq -Rs . <<<"$detail")" >> "$EVENTS_JSONL"
}

run_cmd() {
  # Use a subshell string to preserve compatibility with redirects/pipes.
  local repo="$1"; shift
  local cmd="$*"
  if [[ "$DRY_RUN" == "1" ]]; then
    log "DRYRUN" "$cmd"
    emit_event "$repo" "dryrun_cmd" "$cmd"
  else
    log "RUN" "$cmd"
    emit_event "$repo" "run_cmd" "$cmd"
    bash -c "$cmd"
  fi
}

# Determine risk disposition from working tree (fast heuristic)
classify_repo() {
  local repo_dir="$1"
  local risk="GREEN"

  if [[ -d "$repo_dir/.github/workflows" ]]; then
    risk="YELLOW"
  fi

  if (cd "$repo_dir" && git ls-files | grep -E -i -q "$RED_REGEX"); then
    risk="RED"
  fi

  echo "$risk"
}

disable_actions() {
  local repo="$1"
  # GitHub REST: PUT /repos/{owner}/{repo}/actions/permissions { "enabled": false }
  run_cmd "$repo" "gh api -X PUT repos/$ORG/$repo/actions/permissions -F enabled=false >/dev/null"
}

make_private() {
  local repo="$1"
  run_cmd "$repo" "gh repo edit $ORG/$repo --visibility private >/dev/null"
}

purge_history() {
  local repo_url="$1"
  local repo="$2"
  local workroot="$3"

  local mirror_dir="$workroot/$repo.mirror"

  run_cmd "$repo" "rm -rf \"$mirror_dir\""
  run_cmd "$repo" "git clone --mirror \"$repo_url\" \"$mirror_dir\" >/dev/null"

  if [[ "$DRY_RUN" == "1" ]]; then
    emit_event "$repo" "purge_plan" "Would run git-filter-repo with ${#PURGE_GLOBS[@]} glob(s) on mirror: $mirror_dir"
    return 0
  fi

  cd "$mirror_dir"

  # Single-pass deterministic rewrite (repeated flags are supported).
  local args=(git filter-repo --force)
  for g in "${PURGE_GLOBS[@]}"; do
    args+=(--path-glob "$g")
  done
  args+=(--invert-paths)

  log "RUN" "${args[*]}"
  emit_event "$repo" "purge_filter_repo" "${args[*]}"
  "${args[@]}" >/dev/null

  log "RUN" "Force push rewritten history (mirror)"
  emit_event "$repo" "purge_force_push" "git push --force --mirror"
  git push --force --mirror >/dev/null
}

ensure_gitignore_and_head_cleanup() {
  local repo_dir="$1"
  local repo="$2"

  # Append-safe ignore block
  local ignore_block
  ignore_block=$(cat <<'IGN'
# ---- Charter Standard: Never commit secrets/caches/artifacts ----
.secrets.cache.json
.secrets*.json
.env
.env.*
configs/notion_secrets.json

# Python bytecode
__pycache__/
*.pyc

# Local DBs / ledgers
*.db
*.sqlite
*.sqlite3

# Logs / ledgers / transcripts
*.jsonl
*transcript*
IGN
)

  if [[ "$DRY_RUN" == "1" ]]; then
    emit_event "$repo" "head_hygiene_plan" "Would enforce .gitignore marker + remove tracked artifacts at HEAD"
    return 0
  fi

  cd "$repo_dir"

  # Ensure git user is configured (avoid commit failure)
  git config user.name >/dev/null 2>&1 || git config user.name "activ8ai-bot"
  git config user.email >/dev/null 2>&1 || git config user.email "codex@activ8ai.app"

  # Append ignore block only if missing marker line
  if ! grep -F -q "Charter Standard: Never commit secrets/caches/artifacts" .gitignore 2>/dev/null; then
    printf "\n%s\n" "$ignore_block" >> .gitignore
  fi

  # Remove tracked risky artifacts at HEAD (cached remove)
  shopt -s globstar nullglob
  set +e
  git rm -f --cached .secrets.cache.json 2>/dev/null
  git rm -f --cached .secrets*.json 2>/dev/null
  git rm -f --cached configs/notion_secrets.json 2>/dev/null
  for p in **/__pycache__ **/*.pyc; do
    git rm -r -f --cached "$p" 2>/dev/null
  done
  set -e

  git add .gitignore || true

  # Only commit if there are changes
  if ! git diff --cached --quiet; then
    git commit -m "chore(charter): enforce ignore rules; remove tracked artifacts" >/dev/null
    git push origin HEAD >/dev/null
    emit_event "$repo" "head_hygiene_committed" "Committed/pushed .gitignore + cached removals"
  else
    emit_event "$repo" "head_hygiene_noop" "No HEAD cleanup changes to commit"
  fi
}

main() {
  require_cmd gh
  require_cmd jq
  require_cmd git
  require_cmd git-filter-repo

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --apply) DRY_RUN=0; shift ;;
      --private) DO_PRIVATE=1; shift ;;
      --purge) DO_PURGE=1; shift ;;
      --gitignore) DO_GITIGNORE=1; shift ;;
      --disable-actions) DO_DISABLE_ACTIONS=1; shift ;;
      --repo) LIMIT_REPO="${2:-}"; shift 2 ;;
      --org) ORG="${2:-}"; shift 2 ;;
      --out) OUT_DIR="${2:-}"; shift 2 ;;
      -h|--help) usage; exit 0 ;;
      *) echo "Unknown arg: $1" 1>&2; usage; exit 1 ;;
    esac
  done

  local TS
  TS="$(date -u +"%Y%m%dT%H%M%SZ")"
  local ROOT="${HOME}/repo-audits"
  local OUT="${OUT_DIR:-$ROOT/remediate-$TS}"
  mkdir -p "$OUT/logs"

  EVENTS_JSONL="$OUT/events.jsonl"
  : > "$EVENTS_JSONL"

  # Tee all stderr/stdout into an audit log file (still prints to terminal).
  local RUN_LOG="$OUT/logs/run.log"
  exec > >(tee -a "$RUN_LOG") 2>&1

  log "INFO" "Org=$ORG Timestamp(UTC)=$TS Out=$OUT DryRun=$DRY_RUN"
  log "INFO" "Flags: private=$DO_PRIVATE purge=$DO_PURGE gitignore=$DO_GITIGNORE disable_actions=$DO_DISABLE_ACTIONS limit_repo=${LIMIT_REPO:-<none>}"
  emit_event "-" "start" "Org=$ORG Out=$OUT DryRun=$DRY_RUN"

  # Enumerate public repos deterministically.
  local repos_file="$OUT/public_repos.txt"
  gh repo list "$ORG" --limit 500 --json name,visibility,url \
    | jq -r 'sort_by(.name) | .[] | select(.visibility=="PUBLIC") | "\(.name) \(.url)"' \
    > "$repos_file"

  if [[ ! -s "$repos_file" ]]; then
    log "WARN" "No public repos found (or gh auth missing)."
    emit_event "-" "no_public_repos" "repos_file empty"
    exit 0
  fi

  local summary="$OUT/summary.txt"
  : > "$summary"

  while read -r NAME URL; do
    [[ -z "${NAME:-}" ]] && continue
    if [[ -n "$LIMIT_REPO" && "$NAME" != "$LIMIT_REPO" ]]; then
      continue
    fi

    log "INFO" "----- REPO $NAME -----"
    emit_event "$NAME" "repo_begin" "$URL"

    local repo_dir="$OUT/$NAME"
    run_cmd "$NAME" "rm -rf \"$repo_dir\""
    run_cmd "$NAME" "git clone --depth 1 \"$URL\" \"$repo_dir\" >/dev/null"

    local risk="(dryrun)"
    if [[ "$DRY_RUN" == "0" ]]; then
      risk="$(classify_repo "$repo_dir")"
      log "INFO" "Disposition=$risk"
      emit_event "$NAME" "classified" "$risk"

      if [[ "$DO_DISABLE_ACTIONS" == "1" && ( "$risk" == "YELLOW" || "$risk" == "RED" ) ]]; then
        disable_actions "$NAME"
      fi

      if [[ "$risk" == "RED" ]]; then
        if [[ "$DO_PRIVATE" == "1" ]]; then
          make_private "$NAME"
        fi
        if [[ "$DO_PURGE" == "1" ]]; then
          purge_history "$URL" "$NAME" "$OUT"
        fi
      fi

      if [[ "$DO_GITIGNORE" == "1" ]]; then
        ensure_gitignore_and_head_cleanup "$repo_dir" "$NAME"
      fi
    else
      log "INFO" "Disposition=SKIPPED (dry run does not classify)"
      emit_event "$NAME" "dryrun_repo" "Would remediate per flags"
    fi

    printf "%s %s %s\n" "$NAME" "$URL" "$risk" >> "$summary"
    emit_event "$NAME" "repo_end" "$risk"
  done < "$repos_file"

  log "INFO" "Done. Summary: $summary"
  log "INFO" "Audit log: $RUN_LOG"
  log "INFO" "Events: $EVENTS_JSONL"
  log "INFO" "Public repo list: $repos_file"
  emit_event "-" "done" "Summary=$summary"
}

EVENTS_JSONL=""
main "$@"

