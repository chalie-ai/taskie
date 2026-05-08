# Task Tracker MCP Tools

Reference for the 20 MCP tools available from the Task Tracker server.

## Markdown

Ticket **descriptions** and **comments** render as markdown in the web UI (marked + DOMPurify). Use headings, lists, fenced code blocks, links, tables, blockquotes — they render cleanly. HTML is sanitised. Always write descriptions/comments as markdown rather than plain text concatenated with `\n` so the human reader sees structure.

## Authentication

Every **write** tool takes an `agent_token` argument (UUID, copied from the user's profile page in the web UI). Read-only tools accept it but don't require it. Read it from the `TASK_TRACKER_AGENT_TOKEN` environment variable rather than hard-coding or pasting it. When calling the underlying REST API directly (port `8080`), pass the same UUID via the `X-Agent-Token` HTTP header (or `Authorization: Bearer <jwt>` for password-derived JWTs).

## Tool List

### list_tickets
Search and list tickets. Read-only.

| Parameter | Type | Description |
|-----------|------|-------------|
| `cycle_id` | int | Filter by cycle |
| `project_id` | int | Filter by project |
| `status` | str | Filter by status (backlog/todo/progress/review/done/cancel) |
| `assignee` | str | Filter by assignee name |
| `assignee_id` | int | Filter by assignee user ID |
| `search` | str | Server-side full-text search on name + description |

### get_ticket
Get full ticket details including comments, PR links, relationships, and history.

| Parameter | Type | Description |
|-----------|------|-------------|
| `ticket_id` | int | **Required.** Ticket ID |

### create_ticket
Create a new ticket. Requires `agent_token`.

| Parameter | Type | Description |
|-----------|------|-------------|
| `agent_token` | str | **Required.** Your agent token |
| `name` | str | **Required.** Ticket title |
| `description` | str | Markdown description |
| `type` | str | bug / feature / chore (default: feature) |
| `priority` | str | urgent / high / medium / low / none (default: medium) |
| `status` | str | Initial status (default: backlog) |
| `project_id` | int | Project to assign to |
| `cycle_id` | int | Cycle to assign to |
| `assignee` | str | Who this is assigned to |
| `assignee_id` | int | Assignee user ID |
| `due_date` | str | Due date (YYYY-MM-DD) |

### update_ticket
Update ticket fields. Requires `agent_token`.

| Parameter | Type | Description |
|-----------|------|-------------|
| `ticket_id` | int | **Required.** Ticket ID |
| `agent_token` | str | **Required.** Your agent token |
| `name` | str | New title |
| `description` | str | New description |
| `type` | str | New type |
| `priority` | str | New priority |
| `status` | str | New status |
| `assignee` | str | New assignee |
| `assignee_id` | int | New assignee user ID |
| `due_date` | str | New due date |

### delete_ticket
Hard-delete a ticket. Requires `agent_token`. Comments, PR links, history, and relationships are removed in the same transaction. The deletion is logged at WARNING level to the server log (grep `ticket_deleted` in `docker logs taskie`) — there is no undo.

| Parameter | Type | Description |
|-----------|------|-------------|
| `ticket_id` | int | **Required.** Ticket ID |
| `agent_token` | str | **Required.** Your agent token |

### reorder_tickets
Reorder tickets within or across status columns. Requires `agent_token`.

| Parameter | Type | Description |
|-----------|------|-------------|
| `agent_token` | str | **Required.** Your agent token |
| `items` | list | Array of `{id, status, sort_order}` objects |

### add_comment
Add a comment to a ticket. Requires `agent_token`. Comments are posted as the agent user.

| Parameter | Type | Description |
|-----------|------|-------------|
| `ticket_id` | int | **Required.** Ticket ID |
| `body` | str | **Required.** Comment text (markdown) |
| `agent_token` | str | **Required.** Your agent token |
| `pr_url` | str | PR URL to attach |
| `pr_title` | str | PR title for the link |

### list_comments
List comments on a ticket. Read-only.

| Parameter | Type | Description |
|-----------|------|-------------|
| `ticket_id` | int | **Required.** Ticket ID |

### submit_pr_link
Link a PR to a ticket. Requires `agent_token`.

| Parameter | Type | Description |
|-----------|------|-------------|
| `ticket_id` | int | **Required.** Ticket ID |
| `url` | str | **Required.** PR URL |
| `agent_token` | str | **Required.** Your agent token |
| `title` | str | PR title |
| `status` | str | open / merged / closed (default: open) |

### list_pr_links
List PR links for a ticket. Read-only.

| Parameter | Type | Description |
|-----------|------|-------------|
| `ticket_id` | int | **Required.** Ticket ID |

### delete_pr_link
Remove a PR link. Requires `agent_token`.

| Parameter | Type | Description |
|-----------|------|-------------|
| `ticket_id` | int | **Required.** Ticket ID |
| `pr_id` | int | **Required.** PR link ID to delete |
| `agent_token` | str | **Required.** Your agent token |

### list_relationships
List ticket relationships (dependencies/blocks/related). Read-only.

| Parameter | Type | Description |
|-----------|------|-------------|
| `ticket_id` | int | **Required.** Ticket ID |

### add_relationship
Create a relationship between tickets. Requires `agent_token`.

| Parameter | Type | Description |
|-----------|------|-------------|
| `ticket_id` | int | **Required.** Source ticket ID |
| `agent_token` | str | **Required.** Your agent token |
| `related_ticket_id` | int | **Required.** Target ticket ID |
| `relationship_type` | str | related / depends_on / blocks (default: related) |

### remove_relationship
Remove a ticket relationship. Requires `agent_token`.

| Parameter | Type | Description |
|-----------|------|-------------|
| `ticket_id` | int | **Required.** Ticket ID |
| `relationship_id` | int | **Required.** Relationship ID to remove |
| `agent_token` | str | **Required.** Your agent token |

### get_ticket_history
Get the change history for a ticket. Read-only. Returns every audit entry — field changes (status, priority, assignee, etc. — `sort_order` is excluded as drag-reorder noise), `ticket_created`, `comment_added`, `pr_linked`, `pr_removed`, `relationship_added`, `relationship_removed`. Each entry records the actor (`author_name`, `user_id`) resolved from the request's JWT or agent token, plus `old_value`/`new_value` for field changes or a label for events.

| Parameter | Type | Description |
|-----------|------|-------------|
| `ticket_id` | int | **Required.** Ticket ID |

### get_stats
Get aggregate stats (inbox count, triage count, my tickets). Read-only.

| Parameter | Type | Description |
|-----------|------|-------------|
| `cycle_id` | int | Filter stats by cycle |

### list_projects
List projects. Read-only.

| Parameter | Type | Description |
|-----------|------|-------------|
| `cycle_id` | int | Only return projects attached to this cycle |

Returns each project's `id`, `name`, `description`, `color`, `git_repo_url`, `agent_instructions`, and ticket counts (`ticket_count`, `open_count`, `progress_count`).

### list_cycles
List cycles. Read-only.

| Parameter | Type | Description |
|-----------|------|-------------|
| `project_id` | int | Only return cycles attached to this project |
| `status` | str | Filter by cycle status (`pending`, `in_progress`, `completed`, `cancelled`) |

Returns each cycle's `id`, `title`, `description`, `status`, `start_date`, `end_date`, `project_ids`, `projects` (id/name/color), `ticket_count`, and `done` (count of tickets in `done`/`cancel`).

### create_cycle
Create a new cycle. Requires `agent_token`.

| Parameter | Type | Description |
|-----------|------|-------------|
| `agent_token` | str | **Required.** Your agent token |
| `title` | str | **Required.** Cycle title |
| `description` | str | Markdown description |
| `status` | str | `pending` / `in_progress` / `completed` / `cancelled` (default: `pending`) |
| `start_date` | str | YYYY-MM-DD |
| `end_date` | str | YYYY-MM-DD |
| `project_ids` | list[int] | Projects to attach to this cycle |

### update_cycle
Update a cycle. PATCH semantics — only fields you pass are changed. Requires `agent_token`.

| Parameter | Type | Description |
|-----------|------|-------------|
| `cycle_id` | int | **Required.** Cycle ID |
| `agent_token` | str | **Required.** Your agent token |
| `title` | str | New title |
| `description` | str | New description |
| `status` | str | New status |
| `start_date` | str | New start date |
| `end_date` | str | New end date |
| `project_ids` | list[int] | Replace the attached project list (pass `[]` to clear) |

## Common Workflows

### "What should I work on?"
```
list_tickets → see everything
list_tickets status=todo → ready-to-start tickets
list_tickets assignee=<your_name> → tickets already assigned to you
```

### "I'm starting work on ticket PROJ-5"
```
get_ticket 5 → read context
update_ticket 5 status=progress
add_comment 5 "Starting implementation"
```

### "PR is ready for review"
```
submit_pr_link 5 url=https://github.com/org/repo/pull/42 title="Fix login timeout"
add_comment 5 "PR open for review: https://github.com/org/repo/pull/42"
update_ticket 5 status=review
```
