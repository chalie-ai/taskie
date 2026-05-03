import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{basedir}/instance/task_tracker.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8080/api")
    MCP_PORT = int(os.getenv("MCP_PORT", "5100"))
    JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-in-production")
    JWT_ACCESS_EXPIRY = int(os.getenv("JWT_ACCESS_EXPIRY", "3600"))
    JWT_REFRESH_EXPIRY = int(os.getenv("JWT_REFRESH_EXPIRY", "2592000"))
    MASTER_EMAIL = os.getenv("MASTER_EMAIL", "admin@tasktracker.local")
    MASTER_PASSWORD = os.getenv("MASTER_PASSWORD", "admin")
