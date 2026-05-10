"""Regression test for migration 0003 SQLite-safe downgrade (commit 57aa86f).

Runs the full upgrade→downgrade-to-base→upgrade cycle against a fresh isolated
SQLite file in a SUBPROCESS so the suite's in-memory app fixture is not
disturbed.

Why subprocess: env.py is hard-coupled to current_app.extensions['migrate'],
so the only way to run migrations against an arbitrary URL without polluting
the shared in-memory engine is to spawn a fresh Python process with a clean
DATABASE_URL env var.
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent


def _run_flask(args, env):
    """Invoke `flask <args...>` in a subprocess from the repo root."""
    full_env = {**os.environ, **env, 'FLASK_APP': 'app.py'}
    return subprocess.run(
        [sys.executable, '-m', 'flask', *args],
        cwd=str(REPO_ROOT),
        env=full_env,
        capture_output=True,
        text=True,
        timeout=60,
    )


def test_full_downgrade_upgrade_cycle():
    """upgrade→downgrade base→upgrade must complete without errors on SQLite."""
    fd, db_path = tempfile.mkstemp(suffix='.db', prefix='migration_cycle_')
    os.close(fd)
    env = {'DATABASE_URL': f'sqlite:///{db_path}'}

    try:
        # Step 1: upgrade fresh DB to head
        r = _run_flask(['db', 'upgrade'], env)
        assert r.returncode == 0, (
            f"Initial upgrade failed (exit {r.returncode})\n"
            f"STDOUT:\n{r.stdout}\nSTDERR:\n{r.stderr}"
        )

        # Step 2: downgrade all the way back to base — this is the
        # regression scenario (Task 8's ck_attachment_one_parent CHECK
        # constraint used to fail batch_alter_table on SQLite)
        r = _run_flask(['db', 'downgrade', 'base'], env)
        assert r.returncode == 0, (
            f"Downgrade to base failed (exit {r.returncode})\n"
            f"STDOUT:\n{r.stdout}\nSTDERR:\n{r.stderr}"
        )

        # Step 3: upgrade again — verify schema rebuilds cleanly from empty
        r = _run_flask(['db', 'upgrade'], env)
        assert r.returncode == 0, (
            f"Re-upgrade failed (exit {r.returncode})\n"
            f"STDOUT:\n{r.stdout}\nSTDERR:\n{r.stderr}"
        )

        # Sanity check: docs tables present in the rebuilt DB
        import sqlite3
        conn = sqlite3.connect(db_path)
        try:
            tables = {row[0] for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )}
        finally:
            conn.close()
        for expected in ('folders', 'documents', 'document_versions',
                         'tags', 'document_tags', 'document_ticket_links'):
            assert expected in tables, (
                f"Table '{expected}' missing after downgrade→upgrade cycle. "
                f"Tables present: {sorted(tables)}"
            )

    finally:
        try:
            os.unlink(db_path)
        except OSError:
            pass
