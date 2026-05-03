from functools import wraps
from flask import request, jsonify, g
from src.services.user_service import UserService


def require_agent_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('X-Agent-Token', '')
        if not token:
            token = request.args.get('agent_token', '')
        if not token:
            return jsonify({'error': 'Missing agent token. Provide X-Agent-Token header or agent_token param.'}), 401
        user = UserService.get_user_by_agent_token(token)
        if not user:
            return jsonify({'error': 'Invalid agent token'}), 401
        g.user_id = user.id
        g.user_role = user.role
        g.agent_user = user
        return f(*args, **kwargs)
    return decorated
