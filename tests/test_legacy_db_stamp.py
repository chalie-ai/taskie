"""Regression test for the v0.2.x → v0.3.x auto-stamp guard in ``app.create_app()``.

v0.2.x used ``db.create_all()`` and never wrote an ``alembic_version`` row, so
booting v0.3.x against a v0.2.x volume tried to run ``0001_baseline`` and died
with ``table cycles already exists``. ``_stamp_legacy_db_if_needed()`` is the
fix: it detects "legacy tables present, no alembic_version" and stamps the DB
at ``0001_baseline`` before alembic runs.

Tested in a SUBPROCESS (same pattern as ``test_migration_downgrade_cycle.py``)
so the suite's in-memory app fixture is not disturbed and we can boot the real
``create_app()`` against a synthetic legacy SQLite file.
"""
import os
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


# Minimal v0.2.x-shaped schema: just enough tables for the guard to recognise
# this as a legacy install. We only need ONE of the legacy tables present to
# trigger the stamp; we add a few realistic ones to mirror the production case.
LEGACY_V02X_SCHEMA = """
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20),
    agent_token VARCHAR(64) NOT NULL UNIQUE,
    avatar_color VARCHAR(50),
    created_at DATETIME,
    updated_at DATETIME
);
CREATE TABLE projects (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(500),
    description TEXT,
    agent_instructions TEXT,
    color VARCHAR(50),
    git_repo_url VARCHAR(500),
    created_at DATETIME,
    updated_at DATETIME,
    user_id INTEGER
);
CREATE TABLE tickets (
    id INTEGER PRIMARY KEY,
    display_id VARCHAR(20),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    type VARCHAR(20),
    priority VARCHAR(20),
    status VARCHAR(20),
    project_id INTEGER,
    cycle_id INTEGER,
    assignee VARCHAR(255),
    assignee_id INTEGER,
    due_date DATE,
    sort_order INTEGER,
    created_at DATETIME,
    updated_at DATETIME,
    user_id INTEGER
);
CREATE TABLE cycles (
    id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(20),
    start_date DATE,
    end_date DATE,
    created_at DATETIME,
    updated_at DATETIME,
    user_id INTEGER
);
CREATE TABLE ticket_history (
    id INTEGER PRIMARY KEY,
    ticket_id INTEGER NOT NULL,
    author_name VARCHAR(255),
    field_name VARCHAR(50) NOT NULL,
    old_value TEXT,
    new_value TEXT,
    created_at DATETIME,
    user_id INTEGER,
    FOREIGN KEY(ticket_id) REFERENCES tickets(id)
);
CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    ticket_id INTEGER NOT NULL,
    body TEXT NOT NULL,
    author_type VARCHAR(20),
    author_name VARCHAR(255),
    created_at DATETIME,
    user_id INTEGER,
    FOREIGN KEY(ticket_id) REFERENCES tickets(id)
);
CREATE TABLE attachments (
    id INTEGER PRIMARY KEY,
    ticket_id INTEGER NOT NULL,
    filename VARCHAR(255) NOT NULL,
    content_type VARCHAR(120),
    size_bytes INTEGER NOT NULL,
    storage_path VARCHAR(500) NOT NULL UNIQUE,
    uploader_name VARCHAR(255),
    user_id INTEGER,
    created_at DATETIME,
    FOREIGN KEY(ticket_id) REFERENCES tickets(id)
);
CREATE TABLE ticket_relationships (
    id INTEGER PRIMARY KEY,
    ticket_id INTEGER NOT NULL,
    related_ticket_id INTEGER NOT NULL,
    relationship_type VARCHAR(20) NOT NULL,
    created_at DATETIME,
    user_id INTEGER,
    FOREIGN KEY(ticket_id) REFERENCES tickets(id),
    FOREIGN KEY(related_ticket_id) REFERENCES tickets(id)
);
CREATE TABLE pr_links (
    id INTEGER PRIMARY KEY,
    ticket_id INTEGER NOT NULL,
    comment_id INTEGER,
    url VARCHAR(500) NOT NULL,
    title VARCHAR(255),
    status VARCHAR(20),
    created_at DATETIME,
    user_id INTEGER,
    FOREIGN KEY(ticket_id) REFERENCES tickets(id),
    FOREIGN KEY(comment_id) REFERENCES comments(id)
);
CREATE TABLE cycle_projects (
    cycle_id INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    PRIMARY KEY(cycle_id, project_id),
    FOREIGN KEY(cycle_id) REFERENCES cycles(id),
    FOREIGN KEY(project_id) REFERENCES projects(id)
);
"""


def _build_legacy_db():
    fd, path = tempfile.mkstemp(suffix='.db', prefix='legacy_v02x_')
    os.close(fd)
    conn = sqlite3.connect(path)
    try:
        conn.executescript(LEGACY_V02X_SCHEMA)
        conn.execute(
            "INSERT INTO tickets (id, name, status) VALUES (1, 'pre-existing', 'backlog')"
        )
        conn.commit()
    finally:
        conn.close()
    return path


_BOOT_SCRIPT = """
import app as a
flask_app = a.create_app()
from sqlalchemy import text
from src.models import db
with flask_app.app_context():
    v = db.session.execute(text('SELECT version_num FROM alembic_version')).scalar()
    n = db.session.execute(text('SELECT COUNT(*) FROM tickets')).scalar()
    print(f'VERSION={v}')
    print(f'TICKETS={n}')
"""


def _boot_create_app(db_path):
    """Spawn a child process that calls ``create_app()`` against ``db_path``."""
    env = {
        **os.environ,
        'DATABASE_URL': f'sqlite:///{db_path}',
        'JWT_SECRET': 'test-secret',
        'PYTHONPATH': f"{REPO_ROOT}{os.pathsep}{os.environ.get('PYTHONPATH', '')}",
    }
    fd, script_path = tempfile.mkstemp(suffix='.py', prefix='boot_create_app_')
    os.close(fd)
    try:
        with open(script_path, 'w') as f:
            f.write(_BOOT_SCRIPT)
        return subprocess.run(
            [sys.executable, script_path],
            cwd=str(REPO_ROOT),
            env=env,
            capture_output=True,
            text=True,
            timeout=60,
        )
    finally:
        try:
            os.unlink(script_path)
        except OSError:
            pass


def test_legacy_v02x_db_is_auto_stamped_and_upgraded():
    """A v0.2.x DB (legacy tables, no alembic_version) boots cleanly under v0.3+."""
    db_path = _build_legacy_db()
    try:
        result = _boot_create_app(db_path)
        assert result.returncode == 0, (
            f"create_app() failed against legacy DB (exit {result.returncode})\n"
            f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
        # Pre-existing data must survive
        assert 'TICKETS=1' in result.stdout, (
            f"Pre-existing ticket row was lost or duplicated.\nstdout:\n{result.stdout}"
        )
        # alembic_version must now be at head (0003_docs_init), proving the
        # stamp ran AND the subsequent upgrade caught up to head.
        assert 'VERSION=0003_docs_init' in result.stdout, (
            f"alembic_version is not at head after auto-stamp.\nstdout:\n{result.stdout}"
        )
        # Docs tables must exist now
        conn = sqlite3.connect(db_path)
        try:
            tables = {row[0] for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )}
        finally:
            conn.close()
        for expected in ('folders', 'documents', 'document_versions',
                         'activity_log', 'alembic_version'):
            assert expected in tables, (
                f"Expected table '{expected}' missing after legacy upgrade. "
                f"Tables: {sorted(tables)}"
            )
    finally:
        try:
            os.unlink(db_path)
        except OSError:
            pass


def test_greenfield_db_boots_without_stamp():
    """A brand-new install (no tables at all) should still upgrade from base normally."""
    fd, db_path = tempfile.mkstemp(suffix='.db', prefix='greenfield_')
    os.close(fd)
    try:
        result = _boot_create_app(db_path)
        assert result.returncode == 0, (
            f"create_app() failed on greenfield DB (exit {result.returncode})\n"
            f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
        assert 'VERSION=0003_docs_init' in result.stdout, (
            f"Greenfield DB did not reach head.\nstdout:\n{result.stdout}"
        )
        assert 'TICKETS=0' in result.stdout, (
            f"Greenfield DB had unexpected pre-existing tickets.\nstdout:\n{result.stdout}"
        )
    finally:
        try:
            os.unlink(db_path)
        except OSError:
            pass
