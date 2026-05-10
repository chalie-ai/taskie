"""Regression test for migration 0003 SQLite-safe downgrade (commit 57aa86f).

Runs upgrade→downgrade-to-base→upgrade again against a fresh isolated SQLite
file so the in-memory test DB is not disturbed. Uses Flask-Migrate's Python API
(flask_migrate.upgrade / flask_migrate.downgrade) because env.py is coupled to
current_app — a raw Alembic Config outside the app context would not work.

This test is intentionally session-scoped on the app fixture but does NOT use
the shared in-memory DB. It opens its own temporary file-backed SQLite, runs
both directions, and tears it down.
"""
import os
import tempfile

import pytest


def test_full_downgrade_upgrade_cycle(app):
    """upgrade→downgrade base→upgrade must complete without errors on SQLite."""
    from flask_migrate import upgrade as alembic_upgrade
    from flask_migrate import downgrade as alembic_downgrade

    # Use a temp file so we never touch the suite's in-memory schema.
    fd, db_path = tempfile.mkstemp(suffix='.db', prefix='migration_cycle_')
    os.close(fd)
    try:
        # Reconfigure the app to point at the temp file for this test only.
        original_url = app.config['SQLALCHEMY_DATABASE_URI']
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

        # Dispose the current engine pool so SQLAlchemy opens a fresh
        # connection against the new URL.
        from src.models import db as _db
        with app.app_context():
            _db.engine.dispose()

        try:
            with app.app_context():
                # Fresh DB: migrate up to head
                alembic_upgrade(revision='head')

                # Migrate all the way back to base (no tables should remain)
                alembic_downgrade(revision='base')

                # Migrate up again — this is the regression scenario
                alembic_upgrade(revision='head')

                # If we got here without raising, the cycle works.
                # Assert the docs tables are present after re-upgrade.
                from sqlalchemy import inspect
                inspector = inspect(_db.engine)
                tables = set(inspector.get_table_names())
                for expected in ('folders', 'documents', 'document_versions',
                                 'tags', 'document_tags', 'document_ticket_links'):
                    assert expected in tables, \
                        f"Table '{expected}' missing after downgrade→upgrade cycle"

        finally:
            # Restore the original in-memory URL so remaining tests are unaffected.
            app.config['SQLALCHEMY_DATABASE_URI'] = original_url
            with app.app_context():
                _db.engine.dispose()

    finally:
        try:
            os.unlink(db_path)
        except OSError:
            pass
