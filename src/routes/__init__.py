def register_all(app):
    from src.routes.cycles import cycles_bp
    from src.routes.projects import projects_bp
    from src.routes.tickets import tickets_bp
    from src.routes.comments import comments_bp
    from src.routes.pr_links import pr_links_bp
    from src.routes.users import users_bp
    from src.routes.stats import stats_bp
    from src.routes.auth import auth_bp
    from src.routes.attachments import attachments_bp
    from src.routes.folders import folders_bp
    from src.routes.documents import documents_bp
    from src.routes.document_versions import document_versions_bp
    from src.routes.tags import tags_bp

    app.register_blueprint(cycles_bp, url_prefix='/api')
    app.register_blueprint(projects_bp, url_prefix='/api')
    app.register_blueprint(tickets_bp, url_prefix='/api')
    app.register_blueprint(comments_bp, url_prefix='/api')
    app.register_blueprint(pr_links_bp, url_prefix='/api')
    app.register_blueprint(users_bp, url_prefix='/api')
    app.register_blueprint(stats_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(attachments_bp, url_prefix='/api')
    app.register_blueprint(folders_bp, url_prefix='/api')
    app.register_blueprint(documents_bp, url_prefix='/api')
    app.register_blueprint(document_versions_bp, url_prefix='/api')
    app.register_blueprint(tags_bp, url_prefix='/api')
