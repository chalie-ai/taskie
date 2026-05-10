from flask import Blueprint, request, jsonify
from src.services.tag_service import TagService
from src.auth.jwt import require_auth, optional_auth

tags_bp = Blueprint('tags', __name__)


@tags_bp.route('/tags', methods=['GET'])
@optional_auth
def list_tags():
    return jsonify(TagService.list(
        q=request.args.get('q'),
        limit=request.args.get('limit', default=50, type=int),
    ))


@tags_bp.route('/tags', methods=['POST'])
@require_auth
def create_tag():
    data = request.get_json() or {}
    if not data.get('name'):
        return jsonify({'error': 'name is required'}), 400
    res = TagService.create(data['name'])
    if isinstance(res, dict) and 'error' in res:
        return jsonify(res), 400
    return jsonify(res), 201


@tags_bp.route('/tags/<int:tag_id>', methods=['DELETE'])
@require_auth
def delete_tag(tag_id):
    if not TagService.delete(tag_id):
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'deleted': True})
