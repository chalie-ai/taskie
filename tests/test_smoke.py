def test_app_boots(client):
    resp = client.get('/')
    assert resp.status_code == 200


def test_master_user_exists(db):
    from src.models.user import User
    assert User.query.filter_by(email='admin@test.local').first() is not None
