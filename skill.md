# Task Tracker MCP Tools

Reference for the 45 MCP tools available from the Task Tracker server.

Tools are grouped into two areas:
- **Tickets & Projects** (tools 1–23): tickets, comments, PR links, relationships, attachments, cycles, projects, stats
- **Docs** (tools 24–45): folders, documents, versions, tags, doc↔ticket links, document attachments, search

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

### list_attachments
List attachments on a ticket. Read-only. Returns id, filename, size_bytes, content_type, uploader_name, created_at, and a `download_url` you can GET to fetch the file.

| Parameter | Type | Description |
|-----------|------|-------------|
| `ticket_id` | int | **Required.** Ticket ID |

### upload_attachment
Upload a file to a ticket. Requires `agent_token`. The file must be base64-encoded and passed in `file_base64`. Max 25MB. Logs an `attachment_added` activity entry.

| Parameter | Type | Description |
|-----------|------|-------------|
| `ticket_id` | int | **Required.** Ticket ID |
| `agent_token` | str | **Required.** Your agent token |
| `filename` | str | **Required.** Original filename (used for display + download) |
| `file_base64` | str | **Required.** Base64-encoded file contents |
| `content_type` | str | MIME type (defaults to `application/octet-stream`) |

### delete_attachment
Remove an attachment. Requires `agent_token`. Logs an `attachment_removed` activity entry. The on-disk file is removed too.

| Parameter | Type | Description |
|-----------|------|-------------|
| `ticket_id` | int | **Required.** Ticket ID |
| `attachment_id` | int | **Required.** Attachment ID |
| `agent_token` | str | **Required.** Your agent token |

---

## Docs Tools

The docs system provides Confluence-style documentation management organised into spaces ("global" or per-project), folders, documents, and versions. All content is stored as Markdown.

### Space types

| `space_type` | When to use |
|---|---|
| `global` | Documentation not tied to a specific project (architecture docs, runbooks, ADRs) |
| `project` | Documentation scoped to a project; requires `project_id` |

---

### list_folders
List folders in a space. Read-only.

| Parameter | Type | Description |
|-----------|------|-------------|
| `space` | str | **Required.** `global` or `project` |
| `project_id` | int | Required when `space=project` |

### create_folder
Create a folder. Requires `agent_token`.

| Parameter | Type | Description |
|-----------|------|-------------|
| `agent_token` | str | **Required.** Your agent token |
| `name` | str | **Required.** Folder name |
| `space_type` | str | **Required.** `global` or `project` |
| `project_id` | int | Required when `space_type=project` |
| `parent_folder_id` | int | Parent folder for nesting |
| `sort_order` | int | Display order hint |

### update_folder
Rename or move a folder. PATCH semantics. Requires `agent_token`.

| Parameter | Type | Description |
|-----------|------|-------------|
| `folder_id` | int | **Required.** Folder ID |
| `agent_token` | str | **Required.** Your agent token |
| `name` | str | New name |
| `parent_folder_id` | int | New parent (`null` moves to root) |
| `sort_order` | int | New sort order |

### delete_folder
Delete a folder and everything inside it (subfolders, documents, versions, tags, links, attachment files). Requires `agent_token`. Cannot be undone.

| Parameter | Type | Description |
|-----------|------|-------------|
| `folder_id` | int | **Required.** Folder ID |
| `agent_token` | str | **Required.** Your agent token |

---

### list_documents
List documents in a space, with optional filters. Read-only.

| Parameter | Type | Description |
|-----------|------|-------------|
| `space` | str | **Required.** `global` or `project` |
| `project_id` | int | Required when `space=project` |
| `folder_id` | int | Filter by folder |
| `tag` | str | Filter by tag name |
| `limit` | int | Max results (default 50) |
| `offset` | int | Pagination offset |

### get_document
Get full document details: metadata, current version body, tags, linked ticket IDs, and attachments. Read-only.

| Parameter | Type | Description |
|-----------|------|-------------|
| `document_id` | int | **Required.** Document ID |

### create_document
Create a document and optionally its first version. Requires `agent_token`.

| Parameter | Type | Description |
|-----------|------|-------------|
| `agent_token` | str | **Required.** Your agent token |
| `title` | str | **Required.** Document title |
| `space_type` | str | **Required.** `global` or `project` |
| `project_id` | int | Required when `space_type=project` |
| `folder_id` | int | Folder to place the document in |
| `body_md` | str | Initial body (Markdown) |
| `change_note` | str | Note for the first version |
| `tags` | list[str] | Tag names to attach (created if they don't exist) |
| `sort_order` | int | Display order hint |

### update_document_metadata
Update document metadata (title, folder, sort order, tags). Does NOT create a new version — use `save_document` for content edits. Requires `agent_token`.

| Parameter | Type | Description |
|-----------|------|-------------|
| `document_id` | int | **Required.** Document ID |
| `agent_token` | str | **Required.** Your agent token |
| `title` | str | New title |
| `folder_id` | int | New folder (`null` moves to root) |
| `sort_order` | int | New sort order |
| `tags` | list[str] | Replace full tag set (pass `[]` to clear all tags) |

### delete_document
Delete a document, all its versions, tags, links, and attachment files. Requires `agent_token`. Cannot be undone.

| Parameter | Type | Description |
|-----------|------|-------------|
| `document_id` | int | **Required.** Document ID |
| `agent_token` | str | **Required.** Your agent token |

---

### list_document_versions
List all versions of a document. Read-only. Returns id, version_number, title, change_note, created_at, and created_by.

| Parameter | Type | Description |
|-----------|------|-------------|
| `document_id` | int | **Required.** Document ID |

### get_document_version
Get a specific version including its full `body_md`. Read-only.

| Parameter | Type | Description |
|-----------|------|-------------|
| `document_id` | int | **Required.** Document ID |
| `version_id` | int | **Required.** Version ID |

### save_document
Save a new version of a document and make it current. Requires `agent_token`.

| Parameter | Type | Description |
|-----------|------|-------------|
| `document_id` | int | **Required.** Document ID |
| `agent_token` | str | **Required.** Your agent token |
| `body_md` | str | **Required.** New body (Markdown) |
| `title` | str | New title (defaults to current) |
| `change_note` | str | Description of what changed |

### rollback_document
Roll back to a previous version. The old version becomes current; no new version is created. Requires `agent_token`.

| Parameter | Type | Description |
|-----------|------|-------------|
| `document_id` | int | **Required.** Document ID |
| `version_id` | int | **Required.** Version ID to restore |
| `agent_token` | str | **Required.** Your agent token |

---

### list_tags
List tags, optionally filtered by name prefix. Read-only.

| Parameter | Type | Description |
|-----------|------|-------------|
| `prefix` | str | Only return tags whose name starts with this string |

### create_tag
Create a tag (or return the existing one if the name already exists). Requires `agent_token`.

| Parameter | Type | Description |
|-----------|------|-------------|
| `agent_token` | str | **Required.** Your agent token |
| `name` | str | **Required.** Tag name |

### delete_tag
Delete a tag globally. All document_tag associations are removed. Requires `agent_token`.

| Parameter | Type | Description |
|-----------|------|-------------|
| `tag_id` | int | **Required.** Tag ID |
| `agent_token` | str | **Required.** Your agent token |

---

### link_document_to_ticket
Link a document to a ticket (bidirectional). Idempotent — safe to call again if already linked. Requires `agent_token`.

| Parameter | Type | Description |
|-----------|------|-------------|
| `document_id` | int | **Required.** Document ID |
| `ticket_id` | int | **Required.** Ticket ID |
| `agent_token` | str | **Required.** Your agent token |

### unlink_document_from_ticket
Remove a document↔ticket link. Requires `agent_token`.

| Parameter | Type | Description |
|-----------|------|-------------|
| `document_id` | int | **Required.** Document ID |
| `ticket_id` | int | **Required.** Ticket ID |
| `agent_token` | str | **Required.** Your agent token |

### list_linked_tickets
List ticket IDs linked to a document. Read-only.

| Parameter | Type | Description |
|-----------|------|-------------|
| `document_id` | int | **Required.** Document ID |

---

### list_document_attachments
List attachments on a document. Read-only.

| Parameter | Type | Description |
|-----------|------|-------------|
| `document_id` | int | **Required.** Document ID |

### upload_document_attachment
Upload a file to a document. Requires `agent_token`. Max 25MB. File must be base64-encoded.

| Parameter | Type | Description |
|-----------|------|-------------|
| `document_id` | int | **Required.** Document ID |
| `agent_token` | str | **Required.** Your agent token |
| `filename` | str | **Required.** Original filename |
| `file_base64` | str | **Required.** Base64-encoded file contents |
| `content_type` | str | MIME type (defaults to `application/octet-stream`) |

### delete_attachment
Remove an attachment from a ticket OR document. Polymorphic — same tool handles both attachment kinds. Requires `agent_token`. On-disk file is removed too.

| Parameter | Type | Description |
|-----------|------|-------------|
| `attachment_id` | int | **Required.** Attachment ID |
| `agent_token` | str | **Required.** Your agent token |

---

### search_documents
Full-text search across document titles and bodies. Uses FTS5 on SQLite, FULLTEXT index on MySQL. Read-only.

| Parameter | Type | Description |
|-----------|------|-------------|
| `q` | str | **Required.** Search query (multi-word = AND match) |
| `space` | str | Filter by space (`global` or `project`) |
| `project_id` | int | Filter by project |
| `tag` | str | Filter by tag name |
| `limit` | int | Max results (1–100, default 20) |

Returns a list of `{id, title, snippet, rank, space_type, project_id, folder_id}`.

---

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

### "Write a design doc for ticket PROJ-5"
```python
# Create the document in the project's docs space
doc = create_document(
    title="Auth Refactor — Design",
    space_type="project",
    project_id=1,
    body_md="## Overview\n\nThis document describes ...",
    change_note="Initial draft",
    tags=["design", "auth"],
)

# Link it to the ticket so the panel shows it
link_document_to_ticket(document_id=doc["id"], ticket_id=5)
add_comment(ticket_id=5, body=f"Design doc written: doc #{doc['id']}")
```

### "Find all docs about authentication"
```python
results = search_documents(q="authentication", limit=10)
for r in results:
    print(r["title"], "—", r["snippet"])
```

### "Update a doc after implementation"
```python
# Get the current version
doc = get_document(document_id=42)
current = doc["current_version"]["body_md"]

# Save a new version with changes
save_document(
    document_id=42,
    body_md=current + "\n\n## Implementation notes\n\n...",
    change_note="Added implementation notes post-merge",
)
```
