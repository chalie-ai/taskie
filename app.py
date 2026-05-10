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

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=8080)
