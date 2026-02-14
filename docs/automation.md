# Automation & Operationalization Guide

**Teamwork-MCP Repository Automation Framework**
**Version:** 1.0.0
**Last Updated:** 2026-01-21

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [GitHub Actions](#github-actions)
4. [Pre-Commit Hooks](#pre-commit-hooks)
5. [Automated Scripts](#automated-scripts)
6. [Dependabot Configuration](#dependabot-configuration)
7. [Release Process](#release-process)
8. [Troubleshooting](#troubleshooting)

---

## Overview

This repository uses a comprehensive automation framework to ensure code quality, security, and streamlined development workflows. The automation system consists of:

- **11 GitHub Actions workflows** for CI/CD, security, and maintenance
- **Pre-commit hooks** for local validation
- **Automated scripts** for common operations
- **Dependabot** for dependency management
- **Release automation** for versioning and publishing

### Benefits

- ✅ **Automated security scanning** (daily + on PR)
- ✅ **Consistent code quality** (enforced at commit time)
- ✅ **Zero-touch dependency updates** (Dependabot)
- ✅ **Automated PR management** (labeling, validation, closing)
- ✅ **Streamlined releases** (one-command deployment)
- ✅ **Branch hygiene** (automatic cleanup)

---

## Quick Start

### Initial Setup (One-Time)

```bash
# Clone the repository
git clone https://github.com/Activ8-AI/Teamwork-MCP.git
cd Teamwork-MCP

# Run automated setup
bash scripts/setup-automation.sh

# Verify setup
git commit --allow-empty -m "test: verify automation"
```

This sets up:
- Git hooks (pre-commit, commit-msg, pre-push)
- Script permissions
- Git configuration
- Secrets baseline

### Daily Workflow

```bash
# Make your changes
git add .

# Commit (hooks run automatically)
git commit -m "feat: add new feature"

# Push (security audit runs automatically)
git push
```

---

## GitHub Actions

### 1. CI/CD Pipeline (`.github/workflows/ci.yml`)

**Triggers:** PR, push to main
**Runtime:** ~2-3 minutes
**Purpose:** Build validation

**What it does:**
- Sets up Node.js 20.x
- Installs dependencies
- Runs TypeScript compilation
- Executes build process

**When it runs:**
- Every PR commit
- Every push to main branch

**Monitoring:**
```bash
# View workflow status
gh workflow view ci

# View recent runs
gh run list --workflow=ci.yml
```

---

### 2. Security Scan (`.github/workflows/security-scan.yml`)

**Triggers:** Daily (3 AM UTC), PR, push to main, manual
**Runtime:** ~1-2 minutes
**Purpose:** Vulnerability detection

**What it does:**
- Runs `npm audit` for dependencies
- Scans code for hardcoded secrets
- Validates `.gitignore` coverage
- Creates GitHub issue if vulnerabilities found
- Uploads audit report as artifact

**Schedule:** Daily at 3 AM UTC

**Manual trigger:**
```bash
gh workflow run security-scan.yml
```

**View results:**
```bash
# Latest security report
gh run download $(gh run list --workflow=security-scan.yml --limit 1 --json databaseId -q '.[0].databaseId')
```

---

### 3. Auto-Close Superseded PRs (`.github/workflows/auto-close-superseded-prs.yml`)

**Triggers:** PR opened with "supersedes" label, manual
**Purpose:** Automatically close old PRs

**Usage:**

**Option A: Via PR description**
```markdown
## Summary
This PR fixes everything.

Supersedes: #16, #17, #19
```

**Option B: Manual trigger**
```bash
gh workflow run auto-close-superseded-prs.yml \
  -f pr_number=21 \
  -f superseded_prs=16,17,19
```

**Option C: Add label**
Add the `supersedes` label to your PR, and the workflow will parse the PR description.

---

### 4. Branch Cleanup (`.github/workflows/cleanup-branches.yml`)

**Triggers:** PR closed, weekly (Sundays 2 AM UTC), manual
**Purpose:** Remove stale merged branches

**What it does:**
- Deletes branch when PR is merged
- Weekly scan for merged branches older than 30 days
- Protects branches matching patterns: dependabot, production, staging

**Protected branches:**
- `main`, `master`
- Branches containing "dependabot"
- Branches containing "production"
- Branches containing "staging"

**Manual cleanup:**
```bash
gh workflow run cleanup-branches.yml
```

---

### 5. Changelog Updates (`.github/workflows/update-changelog.yml`)

**Triggers:** PR merged to main
**Purpose:** Automatic CHANGELOG.md updates

**How it works:**
- Extracts PR title and categorizes based on prefix:
  - `feat:` → **Added**
  - `fix:` → **Fixed**
  - `security:` → **Security**
  - Others → **Changed**
- Inserts entry into appropriate section
- Commits directly to main
- Comments on PR when complete

**CHANGELOG format:** Follows [Keep a Changelog](https://keepachangelog.com/)

---

### 6. PR Validation (`.github/workflows/pr-validation.yml`)

**Triggers:** PR opened, edited, synchronized
**Purpose:** Enforce quality standards

**Validations:**
- ✅ Title follows conventional commits
- ✅ Description has minimum content
- ✅ Required sections present

**Auto-labeling:**
- File types: `typescript`, `python`, `documentation`
- Scope: `ci/cd`, `security`, `dependencies`, `tests`
- Size: `size/xs`, `size/s`, `size/m`, `size/l`, `size/xl`
- Breaking changes: `breaking-change`

**Size thresholds:**
- XS: < 10 lines
- S: < 100 lines
- M: < 500 lines
- L: < 1000 lines
- XL: ≥ 1000 lines

---

### 7. Release Automation (`.github/workflows/release.yml`)

**Triggers:** Tag push (v*), manual
**Purpose:** Automated releases

**What it does:**
- Creates GitHub Release with changelog
- Publishes to NPM (stable versions only)
- Builds and pushes Docker images
- Creates post-release checklist issue

**Usage:**
```bash
# Via script (recommended)
bash scripts/release.sh patch

# Manual tag
git tag v0.1.17-alpha
git push origin v0.1.17-alpha
```

**Prerelease detection:**
Versions containing "alpha" or "beta" are marked as prereleases and NOT published to NPM.

---

### 8. Connection Test (`.github/workflows/connection-test.yml`)

**Triggers:** Nightly (2 AM UTC), manual
**Purpose:** API connectivity validation

**What it tests:**
- Teamwork API connectivity
- Authentication
- Basic operations

**Manual run:**
```bash
gh workflow run connection-test.yml
```

---

### 9. Docker Image Publishing (`.github/workflows/publish-image.yml`)

**Triggers:** Push to main, tags (v*)
**Purpose:** Container registry updates

**What it builds:**
- Multi-platform: linux/amd64, linux/arm64
- Tags: version number + latest
- Registry: GitHub Container Registry (GHCR)

**Image location:**
```bash
ghcr.io/activ8-ai/teamwork-mcp:latest
ghcr.io/activ8-ai/teamwork-mcp:v0.1.16-alpha
```

---

## Pre-Commit Hooks

### Husky Hooks (Node.js-based)

**Location:** `.husky/`

#### pre-commit
Runs before every commit:
1. TypeScript type check (`npm run build`)
2. Secret detection (grep for patterns)
3. .gitignore validation

**Bypass (use sparingly):**
```bash
git commit --no-verify -m "emergency fix"
```

#### commit-msg
Validates commit message format:
- Must follow conventional commits
- Pattern: `type(scope): description`
- Valid types: feat, fix, docs, style, refactor, test, chore, perf, ci, build, security

**Examples:**
```bash
✅ feat(api): add user authentication
✅ fix(auth): resolve token expiration
✅ docs: update README
❌ added new feature (invalid)
❌ Fixed bug (invalid - not lowercase)
```

#### pre-push
Runs before push:
1. Tests (if pytest configured)
2. Security audit (`npm audit --audit-level=high`)

### Pre-Commit Framework (Python-based, optional)

**Location:** `.pre-commit-config.yaml`

**Install:**
```bash
pip install pre-commit
pre-commit install
```

**Additional checks:**
- Secret detection (detect-secrets)
- Trailing whitespace
- YAML/JSON validation
- Large file detection
- Private key detection
- ESLint
- Prettier
- Black (Python)
- Flake8 (Python)
- Markdownlint

**Run manually:**
```bash
# All files
pre-commit run --all-files

# Specific hook
pre-commit run detect-secrets --all-files
```

---

## Automated Scripts

### 1. Create PR (`scripts/create-pr.sh`)

**Purpose:** Streamlined PR creation

**Usage:**
```bash
bash scripts/create-pr.sh "feat: add new feature"
```

**What it does:**
- Creates draft PR with template
- Sets base and head branches
- Generates checklist
- Opens in draft mode

**Template includes:**
- Summary section
- Changes checklist
- Testing checklist
- Related issues

---

### 2. Release (`scripts/release.sh`)

**Purpose:** Automated version bumping and tagging

**Usage:**
```bash
# Patch version (0.1.16 → 0.1.17)
bash scripts/release.sh patch

# Minor version (0.1.16 → 0.2.0)
bash scripts/release.sh minor

# Major version (0.1.16 → 1.0.0)
bash scripts/release.sh major

# Specific version
bash scripts/release.sh 0.2.0-beta
```

**What it does:**
1. Validates working directory is clean
2. Pulls latest main
3. Runs security audit
4. Runs build
5. Runs tests
6. Bumps version in package.json
7. Updates CHANGELOG.md
8. Commits with message: `chore(release): X.Y.Z`
9. Creates git tag: `vX.Y.Z`
10. Pushes to origin

**Safety features:**
- Confirms before proceeding
- Validates all checks pass
- Automatically switches to main branch

---

### 3. Setup Hooks (`scripts/setup-hooks.sh`)

**Purpose:** Install Git hooks

**Usage:**
```bash
bash scripts/setup-hooks.sh
```

**What it does:**
- Installs Husky
- Creates hook files
- Makes hooks executable
- Updates package.json

---

### 4. Master Setup (`scripts/setup-automation.sh`)

**Purpose:** Complete automation setup

**Usage:**
```bash
bash scripts/setup-automation.sh
```

**What it does:**
- Checks prerequisites
- Runs hook setup
- Configures Git settings
- Verifies GitHub CLI
- Creates secrets baseline
- Makes scripts executable
- Displays summary

---

## Dependabot Configuration

**Location:** `.github/dependabot.yml`

### NPM Dependencies

**Schedule:** Weekly (Mondays, 3 AM UTC)
**Limit:** 5 open PRs
**Grouping:**
- Development dependencies (minor + patch)
- Production dependencies (patch only)

**Labels:** `dependencies`, `automated`

### GitHub Actions

**Schedule:** Weekly (Mondays, 3 AM UTC)
**Limit:** 3 open PRs
**Labels:** `ci/cd`, `dependencies`, `automated`

### Docker

**Schedule:** Weekly (Mondays, 3 AM UTC)
**Limit:** 2 open PRs
**Labels:** `docker`, `dependencies`, `automated`

### Security Updates

Always enabled and created immediately (not part of schedule).

### Management

```bash
# View Dependabot PRs
gh pr list --label dependencies

# Auto-merge safe updates (patch only)
gh pr merge <PR-NUMBER> --auto --squash
```

---

## Release Process

### Semantic Versioning

This project follows [SemVer](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backwards compatible)
- **PATCH**: Bug fixes (backwards compatible)

**Alpha/Beta versions:** `0.1.17-alpha`, `1.0.0-beta`

### Release Workflow

```bash
# 1. Ensure main is up to date
git checkout main
git pull origin main

# 2. Run release script
bash scripts/release.sh patch

# 3. Confirm when prompted

# 4. Monitor GitHub Actions
# Workflow automatically:
#  - Builds Docker image
#  - Creates GitHub Release
#  - Publishes to NPM (if stable)
```

### Manual Release (Alternative)

```bash
# 1. Update version
npm version patch

# 2. Update CHANGELOG manually
vim CHANGELOG.md

# 3. Commit
git add .
git commit -m "chore(release): 0.1.17"

# 4. Tag
git tag v0.1.17

# 5. Push
git push origin main --tags
```

---

## Troubleshooting

### Common Issues

#### 1. Hook Failures

**Problem:** Pre-commit hook fails

**Solution:**
```bash
# Check what failed
git commit -m "test"

# Bypass (emergency only)
git commit --no-verify -m "emergency fix"

# Fix and recommit
npm run build
git add .
git commit -m "fix: resolve build errors"
```

#### 2. Workflow Not Running

**Problem:** GitHub Action doesn't trigger

**Causes & Solutions:**
- **Not authenticated:** `gh auth login`
- **Workflow disabled:** Check Settings → Actions
- **Branch protection:** Check Settings → Branches

#### 3. Dependabot PRs Not Merging

**Problem:** Dependabot PR has conflicts

**Solution:**
```bash
# Rebase Dependabot PR
gh pr comment <PR-NUMBER> --body "@dependabot rebase"

# Or close and recreate
gh pr close <PR-NUMBER>
gh pr comment <PR-NUMBER> --body "@dependabot recreate"
```

#### 4. Release Fails

**Problem:** Release workflow errors

**Check:**
1. Are secrets configured? (NPM_TOKEN for NPM publish)
2. Are permissions correct? (packages: write)
3. Is version valid? (SemVer format)

**Manual fix:**
```bash
# Delete bad tag
git tag -d v0.1.17
git push origin :refs/tags/v0.1.17

# Recreate
bash scripts/release.sh 0.1.17
```

#### 5. Can't Push to Main

**Problem:** Branch protection blocks push

**Cause:** Direct pushes to main are typically blocked

**Solution:** Always use pull requests
```bash
# Create feature branch
git checkout -b fix/issue-123

# Make changes and commit
git add .
git commit -m "fix: resolve issue"

# Push and create PR
git push origin fix/issue-123
bash scripts/create-pr.sh "fix: resolve issue #123"
```

---

## Best Practices

### Commit Messages

**Format:** `type(scope): description`

**Good examples:**
```bash
feat(api): add user authentication endpoint
fix(auth): resolve token expiration bug
docs(readme): add installation instructions
test(auth): add unit tests for login flow
chore(deps): update dependencies
```

**Bad examples:**
```bash
fixed bug          # Missing type format
Added feature      # Capitalized, wrong format
Update             # Too vague
```

### PR Management

1. **Always use draft PRs** for work-in-progress
2. **Link related issues:** "Closes #123"
3. **Request reviews** before merging
4. **Keep PRs small:** < 500 lines when possible
5. **Squash merge** for cleaner history

### Security

1. **Never commit secrets** - use environment variables
2. **Review Dependabot PRs** within 7 days
3. **Run security audits** before releases
4. **Monitor workflow failures** for security issues

### Branch Hygiene

1. **Delete branches** after merge (automated)
2. **Keep main clean** - no direct commits
3. **Rebase feature branches** regularly
4. **Use descriptive names:** `feat/add-auth`, `fix/issue-123`

---

## Configuration Reference

### Repository Settings

**Required settings for full automation:**

1. **Actions:**
   - Settings → Actions → General
   - Workflow permissions: Read and write
   - Allow GitHub Actions to create PRs: ✅

2. **Branch Protection (main):**
   - Require PR reviews: ✅ (recommended)
   - Require status checks: ✅
   - Required checks: CI
   - Require branches up to date: ✅

3. **Security:**
   - Enable Dependabot alerts: ✅
   - Enable Dependabot security updates: ✅
   - Enable secret scanning: ✅ (public repos only)
   - Enable push protection: ✅

4. **Secrets (if using NPM publish):**
   - Settings → Secrets → Actions
   - Add: `NPM_TOKEN` (for npm publish)

### Environment Variables

**For development:**
```bash
# .env (never commit!)
TEAMWORK_DOMAIN=your-company
TEAMWORK_USERNAME=your-email@example.com
TEAMWORK_PASSWORD=your-password

# For Notion relay
NOTION_TOKEN=secret_xxx
```

**For CI/CD:**
Add to GitHub Secrets (Settings → Secrets → Actions)

---

## Monitoring

### Dashboard

View all workflows:
```bash
gh workflow list
```

View recent runs:
```bash
gh run list --limit 20
```

View specific workflow:
```bash
gh run view <RUN-ID>
```

### Notifications

**GitHub:** Settings → Notifications
**Slack/Email:** Configure in workflow files using:
```yaml
- name: Notify on failure
  if: failure()
  # Add notification step
```

---

## Support

**Issues:** https://github.com/Activ8-AI/Teamwork-MCP/issues
**Documentation:** https://github.com/Activ8-AI/Teamwork-MCP/tree/main/docs
**Contributing:** See CONTRIBUTING.md

---

**Version:** 1.0.0
**Last Updated:** 2026-01-21
**Maintainer:** Activ8-AI Team
