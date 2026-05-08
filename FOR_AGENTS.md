# FOR AGENTS — Task Tracker (Taskie) Onboarding

You are an AI coding agent. This document tells you everything you need to set up Taskie's MCP server on any device, in any agent environment, and start driving tickets.

**This file is canonical. The rest of the docs assume you've read it.**

---

## 0. The 30-second version

Taskie has two interfaces:
- A **web UI** (port `8080`) for humans.
- An **MCP server** (port `5100`, streamable HTTP) for you.

Both speak to the same database. To start:

1. Make sure Taskie is running somewhere reachable from your machine.
2. Add an `mcpServers` entry pointing at `http://<host>:5100/mcp` to your agent's MCP config.
3. Get an `agent_token` from the human's profile page in the web UI and stash it in `TASK_TRACKER_AGENT_TOKEN`.
4. Verify by calling `list_tickets`.

If any of those steps is unclear, keep reading.

---

## 1. What's running where

```
┌────────────────┐       ┌─────────────────┐       ┌──────────────┐
│  Human (web)   │──────▶│  Flask API      │──────▶│              │
│  port 8080     │       │  port 8080      │       │  SQLite DB   │
└────────────────┘       └─────────────────┘       │  (instance/) │
                                                    │              │
┌────────────────┐       ┌─────────────────┐       │              │
│  Agent (MCP)   │──────▶│  MCP Server     │──────▶│              │
│  port 5100     │       │  port 5100      │       └──────────────┘
└────────────────┘       └─────────────────┘
```

Both processes ship in the same container. The MCP server makes HTTP calls to the Flask API internally.

### Common deployment shapes

| Where Taskie runs | MCP URL you use |
|---|---|
| Same machine as the agent (Docker on your laptop) | `http://localhost:5100/mcp` |
| Home-lab / LAN server (e.g. `homeserver.lan`) | `http://homeserver.lan:5100/mcp` |
| Cloud VM with the ports published | `http://<public-ip>:5100/mcp` |
| Behind a TLS reverse proxy (nginx/caddy/traefik) | `https://taskie.example.com/mcp` |

You don't need to know which shape it is — just the URL. **Ask the human if you don't know it.**

---

## 2. Run the server (only if it's not already running)

If a human is already running Taskie somewhere, skip this section.

### Option A — published image

```bash
docker run -d --name taskie \
  -p 8080:8080 -p 5100:5100 \
  -v "$(pwd)/taskie-data:/app/instance" \
  chalieai/taskie:latest
```

The volume mount preserves the SQLite database across container restarts.

### Option B — from source (development)

```bash
git clone https://github.com/chalie-ai/taskie.git
cd taskie
docker build -t taskie:local .
docker run -d --name taskie -p 8080:8080 -p 5100:5100 \
  -v "$(pwd)/instance:/app/instance" taskie:local
```

### Verify it's up

```bash
curl -s http://localhost:8080/api/projects                                # should return JSON array
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:5100/mcp        # 406 means MCP is alive
```

`406` is correct — the MCP endpoint expects a `POST` with the right `Accept` header and rejects bare GETs. Anything other than 406 (typically `Connection refused` or `404`) means the server isn't reachable.

---

## 3. Wire up your agent's MCP client

**The MCP client config does not live in the Taskie repo.** It lives wherever your agent reads its config from. Below are the right paths for the major agent runtimes.

> Taskie's MCP server speaks HTTP on port `5100`. The config shape is identical across every agent runtime:
> ```json
> {
>   "mcpServers": {
>     "taskie": {
>       "type": "http",
>       "url": "http://<HOST>:5100/mcp"
>     }
>   }
> }
> ```
> Substitute `<HOST>` for whichever URL applies to your deployment (see §1).

### Claude Code

**Recommended — user scope** (works in every repo, no per-project setup):

```bash
claude mcp add taskie --scope user --transport http http://localhost:5100/mcp
# replace the URL for remote deployments
```

**Or — project scope** (only this repo):

Create `.mcp.json` in the repo root **and add it to `.gitignore`** so machine-specific URLs don't get committed:

```json
{
  "mcpServers": {
    "taskie": {
      "type": "http",
      "url": "${TASKIE_MCP_URL:-http://localhost:5100/mcp}"
    }
  }
}
```

The `${VAR:-default}` syntax lets each developer point at their own server via `export TASKIE_MCP_URL=…` without editing the file.

### Cursor

Edit `~/.cursor/mcp.json` (global) or `<project>/.cursor/mcp.json` (project) and add the same `mcpServers` block.

### Codex CLI / Codex IDE

Edit `~/.codex/config.toml` (or `~/.codex/mcp.json` depending on version) — Codex follows the standard MCP server schema. Same JSON shape.

### Gemini CLI

Edit `~/.gemini/settings.json` and add the same `mcpServers` block.

### Other / unknown agent

Find the file your agent reads MCP servers from (almost always called `mcp.json`, `mcp_servers.json`, or part of a settings file). Add the same `taskie` block with `"type": "http"`. If your agent can't talk to an HTTP MCP server, drive Taskie directly via the raw HTTP technique in §6.

### Reload the agent

Most agents read MCP config at startup. Restart your agent process after editing the config. Confirm the new tools loaded — for Claude Code:

```bash
claude mcp list
# taskie: http://localhost:5100/mcp (HTTP) - ✓ Connected
```

---

## 4. Authenticate

Every **write** tool (`create_ticket`, `update_ticket`, `add_comment`, `submit_pr_link`, `add_relationship`, `upload_attachment`, `delete_*`, `reorder_tickets`) requires an `agent_token`. Read tools (`list_tickets`, `get_ticket`, `list_comments`, `list_pr_links`, `list_relationships`, `list_attachments`, `get_ticket_history`, `get_stats`) do not.

### Get the token

1. Have the human open the Taskie web UI (e.g. `http://localhost:8080`).
2. They click their profile / avatar → there's an **Agent Token** displayed (a UUID like `159302ea-a809-4ba3-ac6c-09041223cf2d`).
3. Each human has their own token. Tokens identify *who* the agent is acting on behalf of — comments, history entries, and PR links record that user as the actor.

### Where to store it

Pick **one** of:

| Option | Best for |
|---|---|
| Shell env var: `export TASK_TRACKER_AGENT_TOKEN=<uuid>` in `~/.zshrc` / `~/.bashrc` | Most setups |
| Claude Code `~/.claude/settings.json` `env` block: `{ "env": { "TASK_TRACKER_AGENT_TOKEN": "<uuid>" } }` | Claude Code users who don't want it in the shell |
| Pass `agent_token=<uuid>` on every tool call | Last resort — tedious and noisy |

**Never hard-code the token in source files. Never paste it into chat.** Read it from `os.environ['TASK_TRACKER_AGENT_TOKEN']` (or your runtime's equivalent) and forward it on each call.

### Calling the REST API directly with the agent token

The MCP layer accepts `agent_token` as a tool argument and forwards it as the `X-Agent-Token` header. If you ever bypass MCP and hit the Flask REST API at port `8080` directly, every protected endpoint accepts **either** of these:

| Header | Value | Notes |
|---|---|---|
| `Authorization: Bearer <jwt>` | A JWT obtained from `POST /api/auth/token` (email + password login) | Short-lived, refresh via `/api/auth/refresh` |
| `X-Agent-Token: <uuid>` | The agent token from a user's profile page | No expiry; identifies the human as the actor |

Examples:

```bash
# Read (no auth needed)
curl -s http://localhost:8080/api/cycles

# Write with JWT
curl -s -X POST http://localhost:8080/api/cycles \
  -H "Authorization: Bearer $JWT" -H "Content-Type: application/json" \
  -d '{"title":"Cycle X","status":"in_progress","project_ids":[1]}'

# Write with agent token
curl -s -X POST http://localhost:8080/api/cycles \
  -H "X-Agent-Token: $TASK_TRACKER_AGENT_TOKEN" -H "Content-Type: application/json" \
  -d '{"title":"Cycle X","status":"in_progress","project_ids":[1]}'
```

The agent token is also accepted as a query string parameter (`?agent_token=<uuid>`) for clients that can't set custom headers, but the header is preferred — query strings end up in access logs.

---

## 5. Verify end-to-end

Once the MCP is wired and the token is set:

```python
list_tickets()
# → returns a list of tickets. If you get 0 tickets that's fine — it means the DB is empty.
# If you get an exception, check §7 troubleshooting.
```

Then try a write to confirm the token is good:

```python
# Pick any existing ticket; add a no-op comment.
add_comment(ticket_id=1, body="Agent connection check")
```

If both calls succeed, you're done.

---

## 6. HTTP fallback (when MCP tools aren't loaded)

Sometimes the MCP isn't loaded into the current agent session — bad config, the agent runtime hasn't reloaded, you're inside a sub-agent with a stripped tool list, etc. You can still talk to the server directly.

```python
import json, os, urllib.request

URL   = os.environ.get("TASKIE_MCP_URL", "http://localhost:5100/mcp")
TOKEN = os.environ["TASK_TRACKER_AGENT_TOKEN"]

def call(name, args=None):
    args = args or {}
    if any(k in {"create_ticket","update_ticket","delete_ticket","add_comment",
                 "submit_pr_link","delete_pr_link","add_relationship",
                 "remove_relationship","reorder_tickets"} for k in (name,)):
        args = {**args, "agent_token": TOKEN}
    body = json.dumps({
        "jsonrpc": "2.0", "id": 1, "method": "tools/call",
        "params": {"name": name, "arguments": args},
    }).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    })
    raw = urllib.request.urlopen(req, timeout=15).read().decode()
    line = next(l for l in raw.splitlines() if l.startswith("data: "))
    payload = json.loads(line[6:])
    if "error" in payload:
        raise RuntimeError(payload["error"])
    return json.loads(payload["result"]["content"][0]["text"])

# Examples
projects_via_tickets = call("list_tickets")
ticket = call("get_ticket", {"ticket_id": 1})
new = call("create_ticket", {"name": "Test", "project_id": 1})
```

Pass `agent_token` on every write call. The response is an event-stream block; the JSON-RPC payload is the line beginning with `data:`.

---

## 7. Resolving project / cycle names → IDs

The user will say *“create tickets in project Foo, cycle Bar v1.2.3”*. Write tools take **integer IDs**, not names. Use the dedicated discovery tools:

```python
# Project ID
projects = call("list_projects")
project_id = next(p["id"] for p in projects if p["name"] == "Foo")

# Cycle ID — optionally scope by project so cycle titles resolve unambiguously
cycles = call("list_cycles", {"project_id": project_id})
cycle_id = next(c["id"] for c in cycles if c["title"] == "Bar v1.2.3")
```

`list_projects` accepts an optional `cycle_id` filter (return only projects attached to that cycle). `list_cycles` accepts optional `project_id` and `status` filters.

**Creating a cycle from the agent side:**

```python
# Plain create — title is the only required field
cycle = call("create_cycle", {
    "title": "Taskie v0.2.0",
    "status": "in_progress",
    "start_date": "2026-05-08", "end_date": "2026-05-22",
    "project_ids": [project_id],
})

# Update — PATCH semantics, only fields you pass are touched
call("update_cycle", {"cycle_id": cycle["id"], "status": "completed"})
```

---

## 8. Canonical enums

| Field | Allowed values |
|---|---|
| `status` (ticket) | `backlog`, `todo`, `progress`, `review`, `done`, `cancel` |
| `type` | `bug`, `feature`, `chore` |
| `priority` | `urgent`, `high`, `medium`, `low`, `none` |
| `relationship_type` | `related`, `depends_on`, `blocks` |
| `pr_link.status` | `open`, `merged`, `closed` |

`-` is no longer a valid status — the placeholder option was removed in TKT-241. Pre-existing rows are backfilled to `backlog` on server startup, and the API coerces any incoming `-` / empty / `null` status to `backlog`. Always send one of the six values above.

---

## 9. Common workflows

### Find tickets to work on

```
list_tickets                                  → see everything
list_tickets status=backlog                   → tickets needing triage
list_tickets status=todo                      → ready-to-start tickets
list_tickets assignee=<your_name>             → already assigned to you
list_tickets search=<keyword>                 → full-text search on name + description
```

### Claim and start a ticket

```python
get_ticket(ticket_id=5)                                          # read full context
update_ticket(ticket_id=5, status="progress", assignee="you")    # claim it
add_comment(ticket_id=5, body="Starting implementation")
```

### Open a PR

```python
submit_pr_link(ticket_id=5, url="https://github.com/o/r/pull/42",
               title="Fix login timeout", status="open")
add_comment(ticket_id=5, body="PR opened: https://github.com/o/r/pull/42")
update_ticket(ticket_id=5, status="review")
```

### Merge & close

```python
add_comment(ticket_id=5, body="Merged and deployed")
update_ticket(ticket_id=5, status="done")
```

### Bulk-create tickets in a cycle

```python
project_id, cycle_id = ...  # resolve via §7
for spec in specs:
    r = call("create_ticket", {**spec,
                               "project_id": project_id,
                               "cycle_id": cycle_id,
                               "status": "backlog"})
    print(f"created {r['display_id']}: {r['name']}")
```

---

## 10. Conventions for agents

1. **Read first.** `get_ticket` + `list_comments` before doing anything.
2. **Announce intent.** Comment when you start, when you open a PR, when you finish.
3. **Link every PR.** Use `submit_pr_link` so the ticket has a permanent record.
4. **Move statuses honestly.** `backlog` → `todo` → `progress` → `review` → `done`.
5. **Use relationships.** `depends_on` / `blocks` / `related` — capture the real graph.
6. **Reference tickets by `display_id` (`TKT-NNN`)** when talking to humans, by `id` (int) when calling the API.
7. **Never log the token.** Read it from env, pass it on the wire, don't print it.

---

## 10b. Markdown is rendered

Both ticket **descriptions** and **comments** are stored as markdown and rendered with marked + DOMPurify in the web UI. Use markdown freely when you write them — headings, lists, fenced code blocks, links, tables, blockquotes all render. HTML inside those fields is sanitised, so you cannot inject scripts or styles. Plain text still works; this just means humans see formatted output instead of raw `**asterisks**`.

---

## 11. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `Connection refused` to port 5100 | Server not running | Start the container (§2) |
| `406 Not Acceptable` to `GET /mcp` | This is *expected* on a bare GET — it confirms MCP is up | Use POST with the right Accept header (§6), or wait for your agent to do it |
| `mcp__taskie__*` tools missing in your session | MCP config wrong, or agent not reloaded | Re-check §3, restart the agent, then `claude mcp list` (or your agent's equivalent) |
| Tool call returns `agent_token required` | Token not set or not passed | Set `TASK_TRACKER_AGENT_TOKEN` (§4); confirm with `echo $TASK_TRACKER_AGENT_TOKEN` |
| Tool call returns `403` / `invalid token` | Token typo, or token belongs to a different Taskie instance | Re-copy from the human's profile page on the *same* server you're calling |
| `create_ticket` succeeds but ticket is in the wrong project/cycle | Forgot to pass `project_id` / `cycle_id` | Resolve IDs via §7, pass explicitly |
| `list_tickets` returns 0 results when you expect some | DB is genuinely empty, *or* the server you're talking to isn't the one the human is looking at | Verify the URL — humans and agents must point at the same Taskie instance |

If something else is broken, the MCP server logs are inside the container: `docker logs taskie`.

---

## 12. Tool reference

The full per-tool reference (parameters, return shapes, examples) lives in [skill.md](skill.md). Copy it into your agent's skills directory if your agent supports skill files (Claude Code, Cursor, etc.).
