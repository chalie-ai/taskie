import jwt
from datetime import datetime, timezone, timedelta
from functools import wraps
from flask import request, jsonify, current_app, g


def create_access_token(user_id, role):
    now = datetime.now(timezone.utc)
    expiry = now + timedelta(seconds=current_app.config['JWT_ACCESS_EXPIRY'])
    payload = {'sub': str(user_id), 'role': role, 'type': 'access',
               'iat': now, 'exp': expiry}
    return jwt.encode(payload, current_app.config['JWT_SECRET'], algorithm='HS256')


def create_refresh_token(user_id):
    now = datetime.now(timezone.utc)
    expiry = now + timedelta(seconds=current_app.config['JWT_REFRESH_EXPIRY'])
    payload = {'sub': str(user_id), 'type': 'refresh', 'iat': now, 'exp': expiry}
    return jwt.encode(payload, current_app.config['JWT_SECRET'], algorithm='HS256')


def decode_token(token):
    try:
        return jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return {'error': 'token_expired'}
    except jwt.InvalidTokenError:
        return {'error': 'invalid_token'}


def _attach_user_name(user_id):
    if not user_id:
        return None
    from src.models.user import User
    from src.models import db
    u = db.session.get(User, int(user_id))
    return u.name if u else None


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Try JWT Bearer token first
        auth = request.headers.get('Authorization', '')
        if auth.startswith('Bearer '):
            payload = decode_token(auth[7:])
            if not isinstance(payload, dict) or 'error' not in payload:
                if payload.get('type') == 'access':
                    g.user_id = int(payload['sub'])
                    g.user_role = payload['role']
                    g.user_name = _attach_user_name(g.user_id)
                    return f(*args, **kwargs)

        # Try agent token
        agent_token = request.headers.get('X-Agent-Token', '')
        if not agent_token:
            agent_token = request.args.get('agent_token', '')
        if agent_token:
            from src.services.user_service import UserService
            user = UserService.get_user_by_agent_token(agent_token)
            if user:
                g.user_id = user.id
                g.user_role = user.role
                g.user_name = user.name
                return f(*args, **kwargs)

        return jsonify({'error': 'Missing or invalid Authorization header or agent token'}), 401
    return decorated


def optional_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        g.user_id = None
        g.user_role = None
        g.user_name = None
        auth = request.headers.get('Authorization', '')
        if auth.startswith('Bearer '):
            payload = decode_token(auth[7:])
            if not isinstance(payload, dict) or 'error' not in payload:
                g.user_id = payload.get('sub')
                g.user_role = payload.get('role')
                g.user_name = _attach_user_name(g.user_id)
        return f(*args, **kwargs)
    return decorated
