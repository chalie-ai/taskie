# Task Tracker — Design Spec

**Date:** 2026-05-03
**Stack:** Python Flask + MySQL + Bootstrap 5 + jQuery UI
**Design source:** Claude Design handoff (Task Tracker.html)

## Overview

A task/issue tracker for human & agent collaboration. Humans use a web UI. AI agents interact via an MCP server that calls the REST API. The API is the single communication chokepoint — nothing else talks to the database directly.

## Architecture

```
Human:  Browser ──▶ Flask API (:5000) ──▶ MySQL
Agent:  Agent ──▶ MCP Server (:5100) ──HTTP──▶ Flask API (:5000) ──▶ MySQL
```

Two processes, single codebase:
- **Flask API** — serves REST API at `/api/*`, static SPA at `/`, talks to MySQL
- **MCP Server** — separate process, serves MCP over Streamable HTTP at `/mcp`, calls Flask API as HTTP client, zero DB access

## Database Schema

### cycles
| Column | Type | Notes |
|--------|------|-------|
| id | INT PK AUTO | |
| title | VARCHAR(255) | |
| description | TEXT | |
| status | ENUM('pending','in_progress','closed') | default 'pending' |
| start_date | DATE | |
| end_date | DATE | |
| created_at | DATETIME | |
| updated_at | DATETIME | |
| user_id | INT | nullable, for multi-user future |

### cycle_projects
| Column | Type | Notes |
|--------|------|-------|
| cycle_id | INT FK | |
| project_id | INT FK | |

### projects
| Column | Type | Notes |
|--------|------|-------|
| id | INT PK AUTO | |
| name | VARCHAR(255) | |
| location | VARCHAR(500) | path on machine |
| description | TEXT | |
| agent_instructions | TEXT | special CLAUDE.md for agents |
| color | VARCHAR(50) | e.g. oklch(0.55 0.15 265) |
| created_at | DATETIME | |
| updated_at | DATETIME | |
| user_id | INT | nullable |

### tickets
| Column | Type | Notes |
|--------|------|-------|
| id | INT PK AUTO | |
| display_id | VARCHAR(20) | e.g. "TKT-13" |
| name | VARCHAR(255) | |
| description | TEXT | |
| type | ENUM('bug','feature','chore') | |
| priority | ENUM('urgent','high','medium','low','none') | default 'none' |
| status | ENUM('backlog','todo','progress','review','done','cancel') | default 'backlog' |
| project_id | INT FK | |
| cycle_id | INT FK | nullable |
| assignee | VARCHAR(255) | nullable, display name for now |
| created_at | DATETIME | |
| updated_at | DATETIME | |
| user_id | INT | nullable |

### comments
| Column | Type | Notes |
|--------|------|-------|
| id | INT PK AUTO | |
| ticket_id | INT FK | |
| body | TEXT | |
| author_type | ENUM('human','agent') | |
| author_name | VARCHAR(255) | display name |
| created_at | DATETIME | |
| user_id | INT | nullable |

### pr_links
| Column | Type | Notes |
|--------|------|-------|
| id | INT PK AUTO | |
| ticket_id | INT FK | |
| comment_id | INT FK | nullable, if attached to a comment |
| url | VARCHAR(500) | |
| title | VARCHAR(255) | |
| status | ENUM('open','merged','closed') | default 'open' |
| created_at | DATETIME | |
| user_id | INT | nullable |

## API Endpoints

### Cycles
- `GET /api/cycles` — list all
- `POST /api/cycles` — create
- `GET /api/cycles/<id>` — detail with projects + ticket counts
- `PUT /api/cycles/<id>` — update
- `DELETE /api/cycles/<id>` —

### Projects
- `GET /api/projects` — list all (?cycle_id filter)
- `POST /api/projects` — create
- `GET /api/projects/<id>` — detail
- `PUT /api/projects/<id>` — update
- `DELETE /api/projects/<id>` —

### Tickets
- `GET /api/tickets` — list all (?cycle_id, ?project_id, ?status, ?assignee)
- `POST /api/tickets` — create
- `GET /api/tickets/<id>` — detail (includes comments + PR links)
- `PATCH /api/tickets/<id>` — partial update (status, assignee, priority, etc.)
- `DELETE /api/tickets/<id>` —

### Comments
- `GET /api/tickets/<id>/comments` — list
- `POST /api/tickets/<id>/comments` — create (body, author_type, author_name)

### PR Links
- `GET /api/tickets/<id>/pr-links` — list
- `POST /api/tickets/<id>/pr-links` — create (url, title, status)
- `DELETE /api/tickets/<id>/pr-links/<pr_id>` —

## MCP Tools

| Tool | API call | Agent can... |
|------|----------|-------------|
| `list_tickets` | `GET /api/tickets` | view all tickets |
| `get_ticket` | `GET /api/tickets/<id>` | view detail + comments |
| `add_comment` | `POST /api/tickets/<id>/comments` | add comment (author_type=agent) |
| `submit_pr_link` | `POST /api/tickets/<id>/pr-links` | submit PR link |

Agent cannot modify ticket description, name, type, severity, or status. These tools simply don't exist in the MCP server.

## UI Design (from Claude Design handoff)

### Layout
- **Persistent left sidebar** (232px): logo, search/⌘K trigger, active cycle card with progress bar, Inbox/My tickets/Triage quick filters, project list with colored dots + open counts, cycle list with "now" badge, user footer
- **Main content area**: topbar with breadcrumbs + Board/List toggle + New ticket button, filter bar (status/priority/assignee/type chips), content area

### Views
- **Board view**: 6 columns (Backlog → Cancelled), ticket cards with type badge (B/F/C), priority bars (1-3), project dot + name, comment count, assignee avatar. Per-column quick-add via + button. Done/cancelled cards are faded with strikethrough titles.
- **List view**: dense rows grouped by status, columns: priority, type, ID, title, project, comments, date, assignee
- **Projects page**: grid of project cards showing name, path, description, agent instructions block (with fade overflow), ticket stats (total/open/in progress)
- **Command palette**: ⌘K overlay, searches tickets/projects/actions, keyboard navigable

### Ticket Detail Panel
- Slide-over from the right (not a modal)
- Header: ticket ID, project, copy link/more/close buttons
- Editable title
- Props grid: Status, Priority, Assignee, Project, Cycle, Labels (as dropdown pills)
- Description section
- Activity section: threaded comments with avatar, author name, time, agent badge on agent comments
- PR attachments within comments: PR number, title, status badge (open/merged)
- Comment composer: textarea, markdown hint, "Reply as me"/"Agent" toggle, submit button (⌘↵)

### Visual Style
- **Palette**: Warm neutral — bg #FAFAF9, surface #FFFFFF, sunken #F4F3F1
- **Typography**: Inter (UI), JetBrains Mono (IDs/code)
- **Borders**: 1px #E8E6E1, subtle shadows
- **Accent**: Indigo oklch(0.55 0.15 265)
- **Status colors**: muted, used only for dots/icons — backlog #9A9A95, todo #6B6B6B, progress oklch(0.65 0.14 75) amber, review oklch(0.62 0.13 195) teal, done oklch(0.62 0.14 150) green, cancel #B8B6B0

### Keyboard Shortcuts
- `⌘K` or `/` — command palette
- `B` — board view
- `L` — list view
- `C` — new ticket
- `Esc` — close panel/palette

## Implementation Notes

- Bootstrap 5 provides grid/layout/utilities. Custom CSS overrides for the warm neutral palette and design-system tokens.
- jQuery UI Sortable for drag-drop between columns (future), Dialog for any remaining modals.
- The SPA is a single `index.html` using jQuery for AJAX calls to `/api/*`.
- MCP server uses the `mcp` Python SDK with Streamable HTTP transport.
- Config via environment variables: `DATABASE_URL`, `API_BASE_URL` (for MCP server to call API), `MCP_PORT`.
