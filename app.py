import time
import click
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate, upgrade as alembic_upgrade
from config import Config
from src.models import db


# Tables present in any v0.2.x install. If at least one of these exists but
# `alembic_version` is missing/empty, the DB predates Plan 1's alembic baseline
# (v0.2.x used db.create_all()) and must be stamped at 0001_baseline before
# pending migrations run — otherwise 0001_baseline tries to CREATE TABLE on
# tables that already exist and the worker dies on boot.
_LEGACY_V02X_TABLES = ('users', 'tickets', 'projects', 'cycles')


def _stamp_legacy_db_if_needed(app):
    """Auto-stamp pre-alembic (v0.2.x) databases at 0001_baseline.

    Detects the v0.2.x→v0.3.x upgrade case: legacy tables exist, but
    `alembic_version` is absent or empty. Stamps to 0001_baseline so the next
    `alembic_upgrade()` call skips re-creating tables that already exist and
    proceeds straight to 0002+. No-op for greenfield installs (no tables) and
    for already-migrated databases (alembic_version populated).
    """
    from sqlalchemy import inspect
    from flask_migrate import stamp

    insp = inspect(db.engine)
    existing = set(insp.get_table_names())

    has_legacy_tables = any(t in existing for t in _LEGACY_V02X_TABLES)
    if not has_legacy_tables:
        return  # greenfield — let alembic_upgrade() create everything from 0001

    if 'alembic_version' in existing:
        version = db.session.execute(
            db.text('SELECT version_num FROM alembic_version')
        ).scalar()
        if version:
            return  # already managed by alembic — leave alone

    app.logger.warning(
        'Detected legacy v0.2.x schema with no alembic_version. '
        'Stamping database at 0001_baseline before applying migrations.'
    )
    stamp(revision='0001_baseline')


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
        _stamp_legacy_db_if_needed(app)
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

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=8080)
