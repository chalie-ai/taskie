import os

# Config reads env vars at class-definition time, so these MUST be set before
# the ``from app import create_app`` import below — otherwise the suite picks
# up the developer's on-disk DATABASE_URL from .env.
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['JWT_SECRET'] = 'test-secret'
os.environ['MASTER_EMAIL'] = 'admin@test.local'
os.environ['MASTER_PASSWORD'] = 'test-pw'

import pytest
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask_migrate import upgrade as alembic_upgrade


# pysqlite's DBAPI driver auto-commits before DDL and silently swallows BEGIN,
# which breaks SAVEPOINT-based rollback isolation. The standard SQLAlchemy
# workaround is to disable the driver's isolation_level and emit BEGIN
# explicitly. Registered at Engine-class scope so it's in place before
# create_app() opens the first connection.
# Ref: https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#serializable-isolation-savepoints-transactional-ddl
@event.listens_for(Engine, 'connect')
def _sqlite_no_autocommit(dbapi_connection, connection_record):
    try:
        dbapi_connection.isolation_level = None
    except AttributeError:
        pass


@event.listens_for(Engine, 'begin')
def _sqlite_explicit_begin(conn):
    if conn.engine.dialect.name == 'sqlite':
        try:
            conn.exec_driver_sql('BEGIN')
        except Exception:
            # Already in a transaction (e.g. nested begin) — nothing to do.
            pass


from app import create_app
from src.models import db as _db
from src.auth.jwt import create_access_token
from flask_sqlalchemy.session import Session as _FsqlaSession


class _BindRespectingSession(_FsqlaSession):
    """Honor an explicit ``bind=`` passed to the session before falling back to
    flask-sqlalchemy's engine-key routing. Without this, ``Session(bind=conn)``
    is silently ignored — the session always reaches into ``db.engines`` for a
    fresh pool connection, bypassing the SAVEPOINT-wrapped connection the
    ``db`` fixture sets up for rollback isolation.
    """

    def get_bind(self, mapper=None, clause=None, bind=None, **kwargs):
        if bind is None and self.bind is not None:
            bind = self.bind
        return super().get_bind(mapper=mapper, clause=clause, bind=bind, **kwargs)


@pytest.fixture(scope='session')
def app():
    """Flask app bound to an in-memory SQLite DB, schema applied via alembic."""
    app = create_app()
    with app.app_context():
        alembic_upgrade(revision='head')
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    """Per-test rollback wrapper around the session.

    Uses a SAVEPOINT so test code can call ``db.session.commit()`` without
    ending the outer transaction; the ``after_transaction_end`` listener
    re-opens a fresh SAVEPOINT each time, and the outer transaction is
    rolled back on teardown to keep tests isolated.
    """
    with app.app_context():
        connection = _db.engine.connect()
        transaction = connection.begin()

        _db.session.remove()
        _db.session = _db._make_scoped_session(options={
            'class_': _BindRespectingSession,
            'bind': connection,
            'binds': {},
            'join_transaction_mode': 'create_savepoint',
        })
        nested = connection.begin_nested()

        @event.listens_for(_db.session, 'after_transaction_end')
        def restart_savepoint(session, trans):
            nonlocal nested
            if not nested.is_active:
                nested = connection.begin_nested()

        try:
            yield _db
        finally:
            event.remove(_db.session, 'after_transaction_end', restart_savepoint)
            _db.session.remove()
            if transaction.is_active:
                transaction.rollback()
            connection.close()


@pytest.fixture
def master_token(app, db):
    """JWT for the bootstrap master user, suitable for Authorization: Bearer."""
    from src.models.user import User
    u = User.query.filter_by(email='admin@test.local').first()
    return create_access_token(u.id, u.role)


@pytest.fixture
def auth_headers(master_token):
    return {'Authorization': f'Bearer {master_token}'}
