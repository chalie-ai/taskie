import os
import pytest
from flask_migrate import upgrade as alembic_upgrade
from app import create_app
from src.models import db as _db
from src.auth.jwt import create_access_token


@pytest.fixture(scope='session')
def app():
    """Flask app bound to an in-memory SQLite DB, schema applied via alembic."""
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
    os.environ['JWT_SECRET'] = 'test-secret'
    os.environ['MASTER_EMAIL'] = 'admin@test.local'
    os.environ['MASTER_PASSWORD'] = 'test-pw'
    app = create_app()
    with app.app_context():
        alembic_upgrade(revision='head')
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    """Per-test rollback wrapper around the session."""
    with app.app_context():
        connection = _db.engine.connect()
        transaction = connection.begin()
        _db.session.remove()
        _db.session = _db._make_scoped_session(options={'bind': connection, 'binds': {}})
        yield _db
        transaction.rollback()
        connection.close()
        _db.session.remove()


@pytest.fixture
def master_token(app, db):
    """JWT for the bootstrap master user, suitable for Authorization: Bearer."""
    from src.models.user import User
    u = User.query.filter_by(email='admin@test.local').first()
    return create_access_token(u.id, u.role)


@pytest.fixture
def auth_headers(master_token):
    return {'Authorization': f'Bearer {master_token}'}
