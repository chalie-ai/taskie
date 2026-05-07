# FOR AGENTS — Task Tracker Onboarding

You are an AI coding agent. This document tells you how to work with the Task Tracker so you can find tickets, claim work, post updates, and link PRs.

## What This Project Is

Task Tracker is a human + agent task management tool. Humans use a web UI. You use MCP tools. Both share the same data — tickets, projects, cycles, comments, PR links.

## Setup

### 1. Get the MCP Server Running

The project ships as a Docker container with both the Flask API and MCP server. Your human runs:

```bash
docker run -d -p 8080:8080 -p 5100:5100 chalieai/taskie:latest
```

### 2. Connect to the MCP Server

Add this to your MCP config (`.mcp.json` or equivalent):

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

### 3. Authenticate

Every write operation requires an `agent_token`. To get yours:
- Ask your human to open `http://localhost:8080` and go to their profile page
- Their profile shows an "Agent Token" — a UUID like `159302ea-a809-4ba3-ac6c-09041223cf2d`
- Set the env variable: `export TASK_TRACKER_AGENT_TOKEN=<token>`
- Or pass it as a parameter to every MCP tool call

### 4. Install the Skill (Optional)

Copy [skill.md](skill.md) to your skills directory for a complete tool reference:

## How to Use the Tools

### Find Tickets to Work On

```
list_tickets → see all tickets
list_tickets status=backlog → tickets needing triage
list_tickets assignee=<your_name> → your tickets
list_tickets search=<keyword> → search by name
```

### Claim and Start Work

```
get_ticket(ticket_id) → read full details
update_ticket(ticket_id, status="progress", assignee=<your_name>) → claim it
add_comment(ticket_id, body="Starting work on this") → note your intent
```

### Link a PR

When you open a PR, link it:

```
submit_pr_link(ticket_id, url=<pr_url>, title=<pr_title>, status="open")
add_comment(ticket_id, body="PR opened: <url>", pr_url=<url>, pr_title=<title>)
```

When merged:

```
add_comment(ticket_id, body="Merged and deployed")
update_ticket(ticket_id, status="done")
```

### Search

```
list_tickets(search=<query>) → server-side search across ticket names and descriptions
```

## Key Rules

1. **Always read the ticket before working on it.** Use `get_ticket` and `list_comments` to understand context.
2. **Announce intent.** Add a comment when you start, when you open a PR, and when you finish.
3. **Link PRs.** Every code change should link back to a ticket via `submit_pr_link`.
4. **Update status.** Move tickets through the flow: `backlog` → `todo` → `progress` → `review` → `done`.
5. **Use the relationship tools.** If one ticket depends on another, create a relationship. If a ticket blocks another, note it.
