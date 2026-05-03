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
        db.create_all()
        from src.services.user_service import UserService
        UserService.bootstrap_master(app)

    @app.route('/')
    def index():
        return send_from_directory('static', 'index.html')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=8080)
