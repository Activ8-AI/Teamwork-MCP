Security Policy
===============

Supported Versions
------------------

Security updates are applied to the latest release. Older versions may not receive patches.

Reporting a Vulnerability
-------------------------

Please report vulnerabilities privately:

- Open a GitHub security advisory or
- Email a maintainer (see `CODEOWNERS` when available)

Do not file public issues for sensitive vulnerabilities.

Secrets and Credentials
-----------------------

- Do not commit secrets (tokens, API keys, passwords, certificates) to this repository.
- Store secrets in the **Notion Secrets Registry** or **GitHub Secrets**, and inject them at runtime (CI/environment).
- Local files such as `.env` and `.secrets.cache.json` must remain untracked.
