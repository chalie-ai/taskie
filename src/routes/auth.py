from flask import Blueprint, request, jsonify, g
from src.services.user_service import UserService
from src.auth.jwt import create_access_token, create_refresh_token, decode_token, require_auth

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/auth/token', methods=['POST'])
def issue_token():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'email and password are required'}), 400
    user = UserService.get_user_by_email(data['email'])
    if not user or not UserService.verify_password(data['password'], user.password_hash):
        return jsonify({'error': 'Invalid email or password'}), 401
    access = create_access_token(user.id, user.role)
    refresh = create_refresh_token(user.id)
    return jsonify({
        'access_token': access,
        'refresh_token': refresh,
        'token_type': 'bearer',
        'user': {'id': user.id, 'name': user.name, 'email': user.email, 'role': user.role},
    })


@auth_bp.route('/auth/refresh', methods=['POST'])
def refresh_token():
    data = request.get_json()
    if not data or not data.get('refresh_token'):
        return jsonify({'error': 'refresh_token is required'}), 400
    payload = decode_token(data['refresh_token'])
    if isinstance(payload, dict) and 'error' in payload:
        return jsonify({'error': payload['error']}), 401
    if payload.get('type') != 'refresh':
        return jsonify({'error': 'Not a refresh token'}), 401
    from src.models import db, User
    user = db.session.get(User, payload['sub'])
    if not user:
        return jsonify({'error': 'User not found'}), 401
    access = create_access_token(user.id, user.role)
    return jsonify({'access_token': access, 'token_type': 'bearer'})


@auth_bp.route('/auth/change-password', methods=['POST'])
@require_auth
def change_password():
    data = request.get_json()
    if not data or not data.get('old_password') or not data.get('new_password'):
        return jsonify({'error': 'old_password and new_password are required'}), 400
    from src.models import db, User
    user = db.session.get(User, g.user_id)
    if not user or not UserService.verify_password(data['old_password'], user.password_hash):
        return jsonify({'error': 'Invalid current password'}), 401
    UserService.change_password(user.id, data['new_password'])
    return jsonify({'status': 'Password changed'})
