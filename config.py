import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///task_tracker.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8080/api")
    MCP_PORT = int(os.getenv("MCP_PORT", "5100"))
