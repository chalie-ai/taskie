# Task Tracker

A task tracker built for human + AI agent collaboration. Humans get a clean web UI for managing tickets, projects, and cycles. Agents get an MCP server with 16 tools to read, create, update, and link tickets directly from their coding environment.

## Architecture

```
Browser (SPA) ──► Flask API (:8080) ──► SQLite / MySQL
                                        │
Agent (MCP)  ──► MCP Server (:5100) ───┘
                 (calls Flask API via httpx)
```

## Quick Start (Docker)

Pull the published image:

```bash
docker run -d -p 8080:8080 -p 5100:5100 --name taskie chalieai/taskie:latest
```

Or build from source:

```bash
docker build -t taskie .
docker run -d -p 8080:8080 -p 5100:5100 --name taskie taskie
```

Releases are published to Docker Hub automatically when a `v*.*.*` tag is pushed (see `.github/workflows/docker-publish.yml`).

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///instance/task_tracker.db` | Database connection string |
| `JWT_SECRET` | `dev-secret-change-in-production` | Secret for signing JWTs |
| `MASTER_EMAIL` | `admin@tasktracker.local` | Bootstrap admin email |
| `MASTER_PASSWORD` | `admin` | Bootstrap admin password |
| `MCP_PORT` | `5100` | MCP server port |
| `API_BASE_URL` | `http://localhost:8080/api` | API URL the MCP server calls |

On first run, a master admin user is created from `MASTER_EMAIL` / `MASTER_PASSWORD`. Change the password immediately.

## Human Setup

1. Open `http://localhost:8080` in your browser
2. Log in with the master account (or your credentials if an admin created your account)
3. Create projects, cycles, and tickets from the UI

## Agent Setup

See [FOR_AGENTS.md](FOR_AGENTS.md) for full agent onboarding instructions.

### Quick MCP Config

```json
{
  "mcpServers": {
    "task-tracker": {
      "type": "streamable-http",
      "url": "http://localhost:5100/mcp"
    }
  }
}
```

Set the `TASK_TRACKER_AGENT_TOKEN` env var to your agent token (found in your profile page) or pass `agent_token` as a parameter to each MCP tool call.

### Skill Installation

Copy [skill.md](skill.md) to your coding agent's skills directory for a complete tool reference.
