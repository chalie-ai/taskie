from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
from models import db


def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='')
    app.config.from_object(Config)
    CORS(app)
    db.init_app(app)
    Migrate(app, db)

    from routes.api.cycles import cycles_bp
    from routes.api.projects import projects_bp
    from routes.api.tickets import tickets_bp
    from routes.api.comments import comments_bp
    from routes.api.pr_links import pr_links_bp
    from routes.api.users import users_bp

    app.register_blueprint(cycles_bp, url_prefix='/api')
    app.register_blueprint(projects_bp, url_prefix='/api')
    app.register_blueprint(tickets_bp, url_prefix='/api')
    app.register_blueprint(comments_bp, url_prefix='/api')
    app.register_blueprint(pr_links_bp, url_prefix='/api')
    app.register_blueprint(users_bp, url_prefix='/api')

    @app.route('/')
    def index():
        return send_from_directory('static', 'index.html')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=8080)
