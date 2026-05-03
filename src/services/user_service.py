import bcrypt
from src.models import db, User


class UserService:

    @staticmethod
    def _serialize(u):
        return {
            'id': u.id, 'name': u.name, 'surname': u.surname,
            'email': u.email, 'role': u.role,
            'agent_token': u.agent_token,
            'avatar_color': u.avatar_color,
            'created_at': str(u.created_at), 'updated_at': str(u.updated_at),
        }

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def verify_password(password, password_hash):
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

    @staticmethod
    def list_users():
        return [UserService._serialize(u) for u in User.query.order_by(User.name).all()]

    @staticmethod
    def get_user(user_id):
        u = db.session.get(User, user_id)
        if not u:
            return None
        return UserService._serialize(u)

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_user_by_agent_token(token):
        return User.query.filter_by(agent_token=token).first()

    @staticmethod
    def create_user(data):
        if not data.get('email') or not data.get('password'):
            return {'error': 'email and password are required'}
        if User.query.filter_by(email=data['email']).first():
            return {'error': 'A user with that email already exists'}
        u = User(
            name=data['name'],
            surname=data.get('surname', ''),
            email=data['email'],
            password_hash=UserService.hash_password(data['password']),
            role=data.get('role', 'member'),
            avatar_color=data.get('avatar_color', 'oklch(0.55 0.15 265)'),
        )
        db.session.add(u)
        db.session.commit()
        return UserService._serialize(u)

    @staticmethod
    def update_user(user_id, data):
        u = db.session.get(User, user_id)
        if not u:
            return None
        for field in ['name', 'surname', 'email', 'role', 'avatar_color']:
            if field in data:
                setattr(u, field, data[field])
        db.session.commit()
        return UserService._serialize(u)

    @staticmethod
    def change_password(user_id, new_password):
        u = db.session.get(User, user_id)
        if not u:
            return False
        u.password_hash = UserService.hash_password(new_password)
        db.session.commit()
        return True

    @staticmethod
    def delete_user(user_id):
        u = db.session.get(User, user_id)
        if not u:
            return False
        db.session.delete(u)
        db.session.commit()
        return True

    @staticmethod
    def bootstrap_master(app):
        if User.query.first() is not None:
            return
        u = User(
            name=app.config.get('MASTER_EMAIL', 'admin@tasktracker.local').split('@')[0],
            surname='Admin',
            email=app.config.get('MASTER_EMAIL', 'admin@tasktracker.local'),
            password_hash=UserService.hash_password(
                app.config.get('MASTER_PASSWORD', 'admin')),
            role='admin',
            avatar_color='oklch(0.55 0.15 265)',
        )
        db.session.add(u)
        db.session.commit()
