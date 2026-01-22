# Public Repository Remediation (Charter Standard)

This repo includes `scripts/public_repo_remediate.sh`, a **deterministic**, **audit-logged**, **default safe (DRY RUN)** remediation automation designed to run from macOS (or Linux) with:

- `gh` (GitHub CLI)
- `git-filter-repo`
- `jq`
- `git`

## Goals

- Make **RED** repos private (optional)
- Purge risky artifacts from **git history** (optional; force-push rewrite)
- Inject and enforce `.gitignore` (optional)
- Remove tracked risky artifacts at **HEAD** (optional; commit + push)
- Optionally disable GitHub Actions for **YELLOW/RED** repos

## Install (macOS)

```bash
brew install gh git-filter-repo jq
gh auth status
```

Optionally keep the script in your audit bin:

```bash
mkdir -p ~/repo-audits/bin
cp scripts/public_repo_remediate.sh ~/repo-audits/bin/public_repo_remediate.sh
chmod +x ~/repo-audits/bin/public_repo_remediate.sh
```

## Usage

### DRY RUN first (default safe)

```bash
~/repo-audits/bin/public_repo_remediate.sh --private --purge --gitignore --disable-actions
```

### APPLY to one repo first (recommended)

```bash
~/repo-audits/bin/public_repo_remediate.sh --apply --repo Teamwork-MCP --private --purge --gitignore --disable-actions
```

### APPLY across all public repos (after validation)

```bash
~/repo-audits/bin/public_repo_remediate.sh --apply --private --purge --gitignore --disable-actions
```

### Optional flags

- `--org <org>`: defaults to `Activ8-AI`
- `--out <dir>`: override the output directory (default `~/repo-audits/remediate-<timestamp>`)

## Evidence Outputs (Audit Ready)

Each run produces a timestamped folder containing:

- `summary.txt`: per-repo disposition + URL
- `public_repos.txt`: deterministic list of public repos evaluated
- `logs/run.log`: full run log (tee’d)
- `events.jsonl`: machine-ingestible JSONL event stream

## Critical Note: History Rewrite

Using `--purge` **rewrites history** and **force-pushes** rewritten commits (SHAs will change). Anyone with old clones will need to re-clone.

