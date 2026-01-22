## Activ8 Unified MCP (Notion MCP server) — Build & Run Guide

This repository is **`@vizioz/teamwork-mcp`** (Teamwork MCP + a Notion Relay webhook server).  
The **Notion MCP server** you referenced lives in the `Activ8-AI/mcp` monorepo under `packages/activ8-unified-mcp`.

This doc captures the **build + configuration** workflow for bringing up the Notion MCP server via the unified MCP package.

### Get the code (monorepo)

Clone the `Activ8-AI/mcp` monorepo and navigate to the unified MCP package:

```bash
git clone git@github.com:Activ8-AI/mcp.git
cd mcp/packages/activ8-unified-mcp
```

### Install dependencies

If you have `pnpm`:

```bash
pnpm install
```

If you don’t:

```bash
npm install
```

### Build and run (Node)

Build:

```bash
pnpm build
```

Run:

```bash
node dist/server.js
```

### Build and run (Docker)

Build an image:

```bash
docker build -t activ8-unified-mcp:local .
```

Run with an env file:

```bash
docker run --rm -it --env-file .env activ8-unified-mcp:local
```

If a `docker-compose.yml` is provided in the monorepo/package, you can also use:

```bash
docker compose up --build
```

### Environment variables (minimum)

Create a local `.env` (do not commit it) with at least:

```bash
# Metadata (required)
MCP_NAME="Activ8 Unified MCP"
MCP_VERSION="1.0.0"

# Notion (required for Notion tools)
NOTION_API_TOKEN="REPLACE_ME"
```

Optional integration env vars (Slack, Google Cloud, etc.) should be configured per the `activ8-unified-mcp` package README.

### Security & compliance notes (Charter Standard)

- **Never commit secrets** (tokens, API keys, credentials) to source control.
- **Inject secrets at runtime** via environment variables (local `.env`, CI secrets, or secret manager).
- **Prefer least privilege**: scope the Notion token permissions to only what the MCP server needs.
- **Auditability**: keep logging enabled where required, and ensure logs don’t leak secrets.

