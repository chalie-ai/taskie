from flask import Blueprint, request, jsonify
from services import Services

users_bp = Blueprint('users', __name__)


@users_bp.route('/users', methods=['GET'])
def list_users():
    return jsonify(Services.list_users())


@users_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    u = Services.get_user(user_id)
    if not u:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(u)


@users_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'name is required'}), 400
    result = Services.create_user(data)
    if isinstance(result, dict) and 'error' in result:
        return jsonify(result), 400
    return jsonify(result), 201


@users_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400
    u = Services.update_user(user_id, data)
    if not u:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(u)


@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    ok = Services.delete_user(user_id)
    if not ok:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'deleted': True})
