"""Proves the ``db`` fixture's SAVEPOINT-based rollback actually isolates tests.

test_isolation_a writes a user and commits; test_isolation_b runs next and
must only see the bootstrapped master user. If rollback leaks, count > 1.
Names are ordered alphabetically so pytest runs them in this sequence.
"""
from src.models.user import User
from src.services.user_service import UserService


def test_isolation_a_writes_user(db):
    result = UserService.create_user({
        'name': 'Iso',
        'surname': 'Test',
        'email': 'iso-test@example.com',
        'password': 'pw-iso-test',
    })
    assert 'error' not in result, result
    db.session.commit()
    assert User.query.count() == 2


def test_isolation_b_sees_only_master(db):
    assert User.query.count() == 1
    assert User.query.filter_by(email='admin@test.local').first() is not None
    assert User.query.filter_by(email='iso-test@example.com').first() is None
