# Teamwork-MCP Security Remediation Checklist

**Generated**: 2026-01-22
**Status**: URGENT - Repository is PUBLIC

## Immediate Actions (Manual)

### ✅ Step 1: Make Repository Private (DO THIS NOW)
- [ ] Navigate to https://github.com/Activ8-AI/Teamwork-MCP/settings
- [ ] Scroll to "Danger Zone"
- [ ] Click "Change repository visibility"
- [ ] Select "Make private"
- [ ] Type `Activ8-AI/Teamwork-MCP` to confirm
- [ ] Click "I understand, make this repository private"

**⏱️ Estimated time: 30 seconds**

---

### ⚠️ Step 2: Disable GitHub Actions (Recommended)
- [ ] Navigate to https://github.com/Activ8-AI/Teamwork-MCP/settings/actions
- [ ] Select "Disable actions"
- [ ] Click "Save"

**⏱️ Estimated time: 15 seconds**

---

## History Purging (Requires Automation or Manual Git Work)

### What Needs to be Purged from Git History

The following file patterns should be removed from ALL commits:

**Secrets & Credentials:**
- `.secrets.cache.json`
- `.secrets*.json`
- `.env`, `.env.*`
- `configs/notion_secrets.json`
- `*credentials*.json`
- `*token*.json`
- `*secret*.json`, `*secrets*.json`
- `*.pem`, `*.p12` (certificates)
- `*service-account*.json`

**Build Artifacts:**
- `__pycache__/` (Python bytecode)
- `*.pyc`

**Databases & Logs:**
- `*.db`, `*.sqlite`, `*.sqlite3`
- `*ledger*.db`
- `*.jsonl`
- `*transcript*`

---

### Option A: Run Automated Script (When Valid GitHub Token Available)

**Prerequisites:**
```bash
brew install gh git-filter-repo jq  # macOS
gh auth login                       # Authenticate with valid token
```

**Commands:**
```bash
# 1. DRY RUN (preview)
~/repo-audits/bin/public_repo_remediate.sh --private --purge --gitignore --disable-actions

# 2. APPLY to Teamwork-MCP
~/repo-audits/bin/public_repo_remediate.sh --apply --repo Teamwork-MCP --private --purge --gitignore --disable-actions
```

**Script location:** `/home/user/repo-audits/bin/public_repo_remediate.sh`

---

### Option B: Manual History Purge (Advanced)

**⚠️ WARNING:** This rewrites git history and requires force-push. All collaborators must re-clone.

```bash
# 1. Clone a fresh mirror
git clone --mirror https://github.com/Activ8-AI/Teamwork-MCP.git

# 2. Enter directory
cd Teamwork-MCP.git

# 3. Install git-filter-repo
pip3 install git-filter-repo

# 4. Purge each pattern (example - repeat for all patterns above)
git filter-repo --path-glob '.secrets.cache.json' --invert-paths
git filter-repo --path-glob '.secrets*.json' --invert-paths
git filter-repo --path-glob '__pycache__/*' --invert-paths
git filter-repo --path-glob '*.pyc' --invert-paths
git filter-repo --path-glob '*.db' --invert-paths
git filter-repo --path-glob '*.jsonl' --invert-paths
git filter-repo --path-glob '*transcript*' --invert-paths

# 5. Force push (DESTRUCTIVE - rewrites history)
git push --force --mirror
```

---

## Current Status

### ✅ Good News
- `.gitignore` already has Charter Standard protections
- No secret files currently tracked at HEAD
- Repository code appears clean

### ⚠️ Risks
- **Repository is PUBLIC** - anyone can clone it
- **History may contain secrets** from past commits
- **GitHub Actions are enabled** - could expose secrets

---

## Post-Remediation

### After Making Repository Private:
- [ ] Rotate any secrets that were in public history
- [ ] Update Notion Secrets Registry with new credentials
- [ ] Notify team that repository is now private
- [ ] Update any CI/CD that depends on public access

### After Purging History:
- [ ] All team members must `git clone` fresh (old clones will be out of sync)
- [ ] Any forks must be deleted and recreated
- [ ] Update any documentation referencing commit SHAs (they will change)

---

## Questions?

Contact: codex@activ8ai.app
Charter Compliance: Required for Activ8-AI organization
