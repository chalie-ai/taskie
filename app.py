from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
from src.models import db, User


def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='')
    app.config.from_object(Config)
    CORS(app)
    db.init_app(app)
    Migrate(app, db)

    from src.routes import register_all
    register_all(app)

    with app.app_context():
        # Pre-create migrations: drop NOT NULL on tickets.cycle_id for existing
        # sqlite DBs (TKT-234 backlog page needs cycle_id IS NULL tickets).
        _migrate_tickets_cycle_id_nullable(app)

        db.create_all()
        from src.services.user_service import UserService
        UserService.bootstrap_master(app)
        # Backfill legacy ticket rows that pre-date the canonical status set.
        # `-` was used as an "unset" placeholder; NULL slipped in for tickets
        # created before status had a default. Both should resolve to backlog.
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

    return app


def _migrate_tickets_cycle_id_nullable(app):
    """Drop NOT NULL on tickets.cycle_id (sqlite-only, idempotent).

    Older installs created `tickets.cycle_id` with NOT NULL. The Backlog page
    (TKT-234) requires `cycle_id IS NULL` to be valid, so existing tables are
    rebuilt in place. No-op if the column is already nullable or the table
    doesn't exist yet.
    """
    from sqlalchemy import inspect, text
    engine = db.engine
    if engine.dialect.name != 'sqlite':
        return
    insp = inspect(engine)
    if 'tickets' not in insp.get_table_names():
        return
    cols = insp.get_columns('tickets')
    cycle_col = next((c for c in cols if c['name'] == 'cycle_id'), None)
    if not cycle_col or cycle_col.get('nullable', True):
        return
    app.logger.info("migrating tickets.cycle_id to nullable")
    with engine.begin() as conn:
        conn.execute(text("PRAGMA foreign_keys=OFF"))
        conn.execute(text("ALTER TABLE tickets RENAME TO _tickets_old"))
        # Recreate via metadata (picks up new nullable=True from the model).
        from src.models.ticket import Ticket  # noqa: F401 — registers metadata
        Ticket.__table__.create(conn)
        col_names = [c['name'] for c in cols]
        conn.execute(text(
            f"INSERT INTO tickets ({', '.join(col_names)}) "
            f"SELECT {', '.join(col_names)} FROM _tickets_old"
        ))
        conn.execute(text("DROP TABLE _tickets_old"))
        conn.execute(text("PRAGMA foreign_keys=ON"))


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=8080)
