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

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=8080)
