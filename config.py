import os
from dotenv import load_dotenv

load_dotenv()


def _normalize_sqlite_url(url, basedir):
    """Resolve relative sqlite:/// paths against basedir.

    Flask-SQLAlchemy resolves relative SQLite URIs against app.instance_path,
    which can produce surprising nested paths (e.g. instance/instance/db.sqlite).
    Anchoring against the project basedir gives the path users expect.
    """
    prefix = "sqlite:///"
    if not url.startswith(prefix):
        return url
    rest = url[len(prefix):]
    if rest.startswith("/"):
        return url
    return f"sqlite:///{os.path.abspath(os.path.join(basedir, rest))}"


class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = _normalize_sqlite_url(
        os.getenv("DATABASE_URL", f"sqlite:///{basedir}/instance/task_tracker.db"),
        basedir,
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8080/api")
    MCP_PORT = int(os.getenv("MCP_PORT", "5100"))
    JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-in-production")
    JWT_ACCESS_EXPIRY = int(os.getenv("JWT_ACCESS_EXPIRY", "3600"))
    JWT_REFRESH_EXPIRY = int(os.getenv("JWT_REFRESH_EXPIRY", "2592000"))
    MASTER_EMAIL = os.getenv("MASTER_EMAIL", "admin@tasktracker.local")
    MASTER_PASSWORD = os.getenv("MASTER_PASSWORD", "admin")
    # Cap upload body size to ~25MB. Werkzeug will return 413 automatically for
    # oversize multipart payloads, before they hit our handler.
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", str(26 * 1024 * 1024)))
