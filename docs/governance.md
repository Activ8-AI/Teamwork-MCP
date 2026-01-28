# Governance

This repository follows a pragmatic governance model:

## Roles and Ownership

- CODEOWNERS define review responsibility for critical paths
- Maintainers approve releases and enforce policies

## Decision Records

- Significant changes should include a short Decision Record in PR description covering: context, options, decision, rationale, and impact

## CI/CD

- On PR: install, `npm audit --audit-level=high`, typecheck/build, targeted Node tests
- Releases: the same gates run before publish workflows

**Fail-closed principle**: if any required check fails (build, tests, audit), merges are blocked until remediated.

## Security

- Vulnerability reports via SECURITY policy
- No secrets in code; use Notion Secrets Registry or GitHub Secrets (never commit local caches)

## Documentation

- README is entry point; docs folder for standards
- Keep examples updated when APIs change
 - See `operational-execution-charter.md` for the CIS operating mode and accountabilities
