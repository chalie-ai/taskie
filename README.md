# Taskie

A self-hosted, local-first work board for humans and AI agents.

If you're a solopreneur or a small team vibe-coding across multiple projects, you probably don't need the full weight of Jira or Linear. You need somewhere to organise your thoughts, and somewhere your agent can read and write structured task data — without cloud accounts, without subscriptions, without your work leaving your machine.

That's what Taskie is.

## Two interfaces. One database. Stays local.

**Web UI (port `8080`)** — a clean, skimmable board for tickets, projects, cycles, and docs. Designed for humans: organise work, write descriptions, browse versioned documentation, track progress, review what your agent did.

**MCP server (port `5100`)** — 45 tools your AI agent uses to read, create, update, and link tickets and documents directly from its coding environment. Agents authenticate as the user they're working for via a per-user agent token.

Both interfaces talk to the same database. Your data stays on your machine.

## Architecture

```
Browser (SPA) ──► Flask API (:8080) ──► SQLite / MySQL
                                        │
Agent (MCP)  ──► MCP Server (:5100) ───┘
                 (calls Flask API via httpx)
```

## Quick Start

```bash
docker run -d \
  -p 8080:8080 -p 5100:5100 \
  -v "$(pwd)/taskie-data:/app/instance" \
  --name taskie \
  chalieai/taskie:latest
```

The volume mount persists your database across container restarts — don't skip it.

Open `http://localhost:8080`, log in with the master credentials (see [Environment Variables](#environment-variables) below), and create your first project.

**Build from source:**

```bash
git clone https://github.com/chalie-ai/taskie.git
cd taskie
docker build -t taskie .
docker run -d -p 8080:8080 -p 5100:5100 \
  -v "$(pwd)/instance:/app/instance" taskie
```

Releases are published to Docker Hub automatically on `v*.*.*` tags (see `.github/workflows/docker-publish.yml`).

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///<basedir>/instance/task_tracker.db` | Database connection string. Use a `mysql+pymysql://` URL for team deployments. |
| `JWT_SECRET` | `dev-secret-change-in-production` | Secret for signing JWTs. Change this before exposing Taskie on a network. |
| `MASTER_EMAIL` | `admin@tasktracker.local` | Bootstrap admin email |
| `MASTER_PASSWORD` | `admin` | Bootstrap admin password. Change immediately after first login. |
| `MCP_PORT` | `5100` | MCP server port |
| `API_BASE_URL` | `http://localhost:8080/api` | URL the MCP server uses to reach the Flask API internally |

## Human Setup

1. Open `http://localhost:8080`
2. Log in with your master credentials
3. Create projects, cycles, and tickets from the UI

## Agent Setup

For full agent onboarding, send your agent to [FOR_AGENTS.md](FOR_AGENTS.md) — it covers every deployment shape, auth setup, and tool reference.

**Quick MCP config:**

```json
{
  "mcpServers": {
    "taskie": {
      "type": "http",
      "url": "http://localhost:5100/mcp"
    }
  }
}
```

Grab your agent token from the profile page in the web UI and set it as `TASK_TRACKER_AGENT_TOKEN` in your agent's environment.

**Skill file:** copy [skill.md](skill.md) to your agent's skills directory for a full tool reference it can read on demand.

## Teams

User management is built in. Create accounts for each team member via the admin panel — each person gets their own agent token so agents authenticate as the right user. Switch to MySQL via `DATABASE_URL` if SQLite isn't enough for your workload.

## License

MIT — see [LICENSE](LICENSE).
