from flask import Blueprint, request, jsonify, g
from src.services.user_service import UserService
from src.auth.jwt import require_auth

users_bp = Blueprint('users', __name__)


@users_bp.route('/users', methods=['GET'])
@require_auth
def list_users():
    return jsonify(UserService.list_users())


@users_bp.route('/users/<int:user_id>', methods=['GET'])
@require_auth
def get_user(user_id):
    u = UserService.get_user(user_id)
    if not u:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(u)


@users_bp.route('/users', methods=['POST'])
@require_auth
def create_user():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'name is required'}), 400
    result = UserService.create_user(data)
    if isinstance(result, dict) and 'error' in result:
        return jsonify(result), 400
    return jsonify(result), 201


@users_bp.route('/users/<int:user_id>', methods=['PUT'])
@require_auth
def update_user(user_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400
    u = UserService.update_user(user_id, data)
    if not u:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(u)


@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
@require_auth
def delete_user(user_id):
    if not UserService.delete_user(user_id):
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'deleted': True})


@users_bp.route('/users/<int:user_id>/password', methods=['PUT'])
@require_auth
def admin_change_password(user_id):
    if g.user_role != 'admin':
        return jsonify({'error': 'Admin only'}), 403
    data = request.get_json()
    if not data or not data.get('new_password'):
        return jsonify({'error': 'new_password is required'}), 400
    if not UserService.change_password(user_id, data['new_password']):
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'status': 'Password changed'})
