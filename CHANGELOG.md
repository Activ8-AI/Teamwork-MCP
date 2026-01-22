## Changelog

All notable changes to this repository are documented here.

This project follows pragmatic release notes (not strict SemVer guarantees during alpha).

## Unreleased

### Security
- Updated `@modelcontextprotocol/sdk` to remediate high-severity advisories (DNS rebinding default + ReDoS).
- Ensured `qs` resolves to `>= 6.14.1` to remediate high-severity DoS advisory.
- CI now fails closed on `npm audit --audit-level=high`.

### Testing
- Added Node built-in test runner coverage for the Notion Relay server health endpoint and webhook signature contract.

### CI/CD
- CI now runs `npm test` (build + targeted tests) on PRs and `main`.
