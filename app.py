import time
import click
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate, upgrade as alembic_upgrade
from config import Config
from src.models import db


def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='')
    app.config.from_object(Config)
    CORS(app)
    db.init_app(app)
    Migrate(app, db)

    # Routes register lazily — query bodies fire on first request, after
    # alembic_upgrade() below has applied any pending migrations.
    from src.routes import register_all
    register_all(app)

    with app.app_context():
        # Schema is owned by alembic. Apply pending migrations on startup so
        # docker installs upgrade transparently.
        alembic_upgrade()
        from src.services.user_service import UserService
        UserService.bootstrap_master(app)
        # One-shot data backfill for status placeholders (TKT-235 cleanup).
        from src.models import Ticket
        legacy = Ticket.query.filter(
            db.or_(Ticket.status.is_(None), Ticket.status == '', Ticket.status == '-')
        )
        if legacy.count():
            legacy.update({Ticket.status: 'backlog'}, synchronize_session=False)
            db.session.commit()

    @app.route('/')
    def index():
        return send_from_directory('static', 'index.html')

    @app.cli.command('reindex-docs')
    @click.option('--space', type=click.Choice(['global', 'project']), default=None,
                  help='Restrict to a single space (global or project).')
    @click.option('--project-id', type=int, default=None,
                  help='Restrict to a single project (requires --space project).')
    def reindex_docs(space, project_id):
        """Rebuild the FTS5/MySQL full-text search index for all documents.

        On SQLite the FTS5 virtual table is truncated first so stale entries
        from deleted documents are purged before re-populating. On MySQL the
        search_body column lives on the documents table, so deleted rows are
        already gone and no truncation step is needed.
        """
        from sqlalchemy import text
        from src.models import Document
        from src.services.document_search_service import DocumentSearchService

        t0 = time.monotonic()

        # SQLite: wipe the FTS table so deleted docs do not persist across runs.
        if db.engine.dialect.name == 'sqlite':
            db.session.execute(text("DELETE FROM document_fts"))
            db.session.commit()

        q = Document.query
        if space:
            q = q.filter(Document.space_type == space)
        if project_id is not None:
            q = q.filter(Document.project_id == project_id)

        docs = q.order_by(Document.id).all()
        total = len(docs)

        for idx, doc in enumerate(docs, start=1):
            DocumentSearchService.reindex_document(doc.id)
            if idx % 50 == 0:
                click.echo(f'reindexed {idx} of {total}...')

        elapsed = time.monotonic() - t0
        click.echo(f'reindexed {total} documents in {elapsed:.1f}s')

    @app.cli.command('seed-docs')
    @click.option('--force', is_flag=True, default=False,
                  help='Wipe existing docs content and reseed from scratch.')
    def seed_docs(force):
        """Populate a fresh DB with realistic demo docs data.

        Idempotent by default — skips if any folders already exist. Pass
        --force to wipe all existing folders/documents/tags before reseeding.
        """
        from src.models import Folder, Document, DocumentVersion, Tag, DocumentTag
        from src.models import Ticket
        from src.services.document_service import DocumentService
        from src.services.folder_service import FolderService
        from src.services.tag_service import TagService
        from src.services.document_link_service import DocumentLinkService

        existing = Folder.query.count()
        if existing and not force:
            click.echo(
                f'seed-docs: {existing} folder(s) already exist — skipping. '
                'Use --force to wipe and reseed.'
            )
            return

        if force:
            # Remove all documents first (handles tags, links, attachments, FTS).
            for doc in Document.query.all():
                DocumentService.delete(doc.id)
            # Remove remaining folders (documents already gone, non-recursive OK).
            for folder in Folder.query.all():
                db.session.delete(folder)
            # Remove all tags.
            DocumentTag.query.delete(synchronize_session=False)
            Tag.query.delete(synchronize_session=False)
            db.session.commit()

        # ------------------------------------------------------------------
        # Folder tree
        # ------------------------------------------------------------------
        def _folder(name, parent_id=None):
            return FolderService.create({
                'name': name,
                'space_type': 'global',
                'parent_folder_id': parent_id,
            })

        eng = _folder('Engineering')
        ops = _folder('Operations')
        kb  = _folder('Knowledge Base')

        arch      = _folder('Architecture',  eng['id'])
        onboarding = _folder('Onboarding',   eng['id'])
        runbooks  = _folder('Runbooks',       eng['id'])
        incidents = _folder('Incidents',      ops['id'])
        policies  = _folder('Policies',       ops['id'])
        faqs      = _folder('FAQs',           kb['id'])

        folders_created = 9  # 3 root + 6 sub

        # ------------------------------------------------------------------
        # Document helper
        # ------------------------------------------------------------------
        def _doc(title, folder_id, body_md, tags=None):
            d = DocumentService.create({
                'title': title,
                'space_type': 'global',
                'folder_id': folder_id,
                'body_md': body_md,
                'tags': tags or [],
            })
            return d

        # ------------------------------------------------------------------
        # Architecture docs
        # ------------------------------------------------------------------
        body_arch_overview = """\
## Overview

Taskie is a self-hosted, Linear-style task tracker designed for small teams
that want full control over their data.

## Components

- **Backend** — Flask + SQLAlchemy, Alembic migrations, SQLite (default)
  or MySQL.
- **Frontend** — Vanilla JS single-page app served from `/static`.
- **MCP layer** — StreamableHTTP transport on `:5100/mcp` exposes all
  entities as tools for AI agents.

## Request flow

```
Browser → Flask routes → Services → SQLAlchemy ORM → SQLite / MySQL
                      ↘ MCP tools ↗
```

## Design principles

1. Local-first — no cloud dependency; runs on a Raspberry Pi.
2. Schema-as-code — Alembic owns every migration; `db.create_all()` is
   disabled.
3. Service layer — HTTP routes are thin; business logic lives in
   `src/services/`.

## Known limitations

- No real-time collaboration (no WebSockets).
- FTS5 requires SQLite ≥ 3.9 (released 2015).
"""

        body_db_design = """\
## Entity-relationship summary

```
projects ─┬─< tickets >─< comments
          ├─< folders >─< documents >─< document_versions
          └─< cycle_projects >─< cycles
```

## Key design decisions

### Polymorphic activity log

All audit events live in `activity_log(entity_type, entity_id, ...)`.
This avoids a proliferation of per-entity history tables.

### Circular FK between documents and document_versions

`documents.current_version_id → document_versions.id` and
`document_versions.document_id → documents.id` form a cycle.
SQLAlchemy's `use_alter=True` + `post_update=True` breaks the DDL
bootstrapping order and allows clean inserts.

### Attachment storage

Files land in `instance/attachments/` (tickets) or
`instance/attachments/docs/` (documents). The DB stores only a UUID
filename; the original name is preserved in the `filename` column for
display.

## Indexes

| Table | Index | Purpose |
|---|---|---|
| document_fts | FTS5 virtual | Full-text search |
| document_tags | ix_document_tags_tag_id | Tag-filter joins |
| document_ticket_links | ix_document_ticket_links_ticket_id | Reverse link lookup |
"""

        _doc('System Architecture Overview', arch['id'], body_arch_overview,
             tags=['architecture', 'engineering'])
        _doc('Database Design & ER Diagram',  arch['id'], body_db_design,
             tags=['architecture', 'engineering'])

        # ------------------------------------------------------------------
        # Onboarding docs
        # ------------------------------------------------------------------
        body_local_dev = """\
## Prerequisites

- Python 3.11+
- `pip install -r requirements.txt`
- (Optional) Docker Desktop for the containerised run

## Quick start

```bash
cp .env.example .env          # fill in JWT_SECRET, MASTER_EMAIL, MASTER_PASSWORD
flask db upgrade               # apply migrations
flask run --port 8080          # start dev server
```

Visit `http://localhost:8080`.

## Useful commands

| Command | Purpose |
|---|---|
| `flask reindex-docs` | Rebuild FTS5 search index |
| `flask seed-docs` | Populate demo data |
| `flask db upgrade` | Apply pending migrations |
| `flask db downgrade base` | Roll back all migrations |

## Environment variables

- `DATABASE_URL` — SQLAlchemy URI (default: `sqlite:///instance/app.db`)
- `JWT_SECRET` — HS256 signing key for auth tokens
- `MASTER_EMAIL` / `MASTER_PASSWORD` — bootstrap admin credentials
- `MCP_ENABLED` — set to `1` to start the MCP server on `:5100`
"""

        body_agent_guide = """\
## What is MCP?

Model Context Protocol (MCP) lets AI agents interact with Taskie via
structured tool calls over HTTP.

## Connecting

```json
{
  "mcpServers": {
    "taskie": {
      "url": "http://localhost:5100/mcp",
      "headers": { "X-Agent-Token": "<your-agent-token>" }
    }
  }
}
```

## Available tool categories

- **Tickets** — create, update, delete, list, reorder
- **Projects** — CRUD + cycle membership
- **Cycles** — sprint management
- **Documents** — folders, docs, versions, tags, links
- **Search** — FTS5 full-text across title + body + tags
- **Attachments** — upload, list, delete for tickets and documents

## Authentication

Every MCP request must carry `X-Agent-Token`. Generate a token in the UI
under **Settings → Users** or via `POST /api/auth/agent-token`.
"""

        _doc('Local Dev Setup',     onboarding['id'], body_local_dev,
             tags=['onboarding', 'engineering'])
        _doc('AI Agent Guide',      onboarding['id'], body_agent_guide,
             tags=['onboarding'])

        # ------------------------------------------------------------------
        # Runbook docs
        # ------------------------------------------------------------------
        body_db_migration = """\
## When to run this

After every deploy that ships a new Alembic revision.

## Steps

1. SSH into the host (or exec into the Docker container).

```bash
flask db upgrade
```

2. Check the output — each `Running upgrade` line is a migration applied.

3. If upgrade fails, roll back:

```bash
flask db downgrade -1
```

Then investigate `migrations/versions/` for the broken revision.

## SQLite-specific notes

- SQLite uses `batch_alter_table` for all schema changes — the table is
  rebuilt, not altered in place.
- A full `flask db downgrade base` is supported but destructive; take a
  backup first.

## Backups before migration

```bash
cp instance/app.db instance/app.db.bak-$(date +%Y%m%d)
```
"""

        body_fts_rebuild = """\
## Symptom

Search returns no results or stale results after a large import or
after restoring from backup.

## Resolution

```bash
flask reindex-docs
```

This truncates the `document_fts` FTS5 virtual table and rebuilds it
from all `documents` rows. Progress is printed every 50 documents.

## Filters

```bash
flask reindex-docs --space global
flask reindex-docs --space project --project-id 3
```

## MySQL

On MySQL `search_body` is a regular column on `documents`. After a bulk
insert bypass the ORM, re-run `flask reindex-docs` to re-emit
`search_body` for affected rows.
"""

        _doc('Database Migration Runbook', runbooks['id'], body_db_migration,
             tags=['runbook', 'engineering'])
        _doc('Search Reindex Runbook',     runbooks['id'], body_fts_rebuild,
             tags=['runbook', 'engineering'])

        # ------------------------------------------------------------------
        # Operations docs
        # ------------------------------------------------------------------
        body_incident = """\
## Severity levels

| Level | Response time | Example |
|---|---|---|
| P0 | 15 min | All users cannot log in |
| P1 | 1 hour | Specific feature broken for majority |
| P2 | Next business day | Minor UI glitch |

## Response checklist

- [ ] Identify scope (who is affected, which environment)
- [ ] Create a ticket with priority = urgent
- [ ] Post update in team channel every 30 min
- [ ] Write a post-mortem within 48 hours

## Post-mortem template

```
## Timeline
## Root cause
## Impact
## Mitigations applied
## Follow-up actions
```
"""

        body_on_call = """\
## Schedule

On-call rotates weekly. The primary on-call owns:

- Monitoring dashboard review (daily)
- Response to P0/P1 alerts within 15 minutes

## Escalation

1. Primary on-call
2. Secondary on-call (backup)
3. Engineering lead

## Tools

- Alert dashboard: `http://localhost:8080` (Taskie board, label=ops)
- Logs: `journalctl -u taskie -f` or `docker logs taskie -f`
"""

        _doc('Incident Response Playbook', incidents['id'], body_incident,
             tags=['ops', 'runbook'])
        _doc('On-Call Guide',              incidents['id'], body_on_call,
             tags=['ops'])
        _doc('Security Policy',            policies['id'],
             '## Access control\n\nAll users require JWT auth.\n\n'
             '## Secrets\n\nNever commit `.env` files.\n',
             tags=['ops'])

        # ------------------------------------------------------------------
        # Knowledge Base docs
        # ------------------------------------------------------------------
        body_faq = """\
## Why SQLite as default?

SQLite requires zero infrastructure. For teams under ~50 users and
moderate write concurrency, SQLite is fast enough and far simpler to
operate than a separate database server.

## Can I switch from SQLite to MySQL?

Yes. Set `DATABASE_URL=mysql+pymysql://...` and run `flask db upgrade`.
The migrations are dialect-aware.

## Where are uploaded files stored?

In `instance/attachments/` on the server filesystem. Back this directory
up alongside `instance/app.db`.

## How do I reset the admin password?

Delete the user row from the DB and restart — `UserService.bootstrap_master`
recreates it from `MASTER_EMAIL` / `MASTER_PASSWORD`.

## How do I export all data?

Use the MCP tools or the REST API. There is no built-in export command yet.
"""

        _doc('Frequently Asked Questions', faqs['id'], body_faq,
             tags=['ops', 'engineering'])
        _doc('Glossary',                   faqs['id'],
             '## Taskie terms\n\n'
             '- **Space** — global or project scope for a folder/doc.\n'
             '- **Cycle** — sprint / iteration.\n'
             '- **MCP** — Model Context Protocol; the agent API.\n',
             tags=['onboarding'])

        docs_created = Document.query.filter_by(space_type='global').count()

        # ------------------------------------------------------------------
        # Doc-to-ticket links (if any tickets exist)
        # ------------------------------------------------------------------
        links_created = 0
        tickets = Ticket.query.limit(2).all()
        arch_docs = Document.query.filter_by(folder_id=arch['id']).limit(2).all()
        for ticket, adoc in zip(tickets, arch_docs):
            result = DocumentLinkService.link(adoc.id, ticket.id)
            if result is not None:
                links_created += 1

        tag_count = Tag.query.count()

        click.echo(
            f'seeded {folders_created} folders, {docs_created} documents, '
            f'{tag_count} tags, {links_created} doc-ticket links'
        )

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=8080)
