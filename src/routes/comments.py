from flask import Blueprint, request, jsonify
from src.services.comment_service import CommentService
from src.auth.jwt import require_auth

comments_bp = Blueprint('comments', __name__)


@comments_bp.route('/tickets/<int:ticket_id>/comments', methods=['GET'])
def list_comments(ticket_id):
    c = CommentService.list_comments(ticket_id)
    if c is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(c)


@comments_bp.route('/tickets/<int:ticket_id>/comments', methods=['POST'])
@require_auth
def add_comment(ticket_id):
    data = request.get_json()
    if not data or not data.get('body'):
        return jsonify({'error': 'body is required'}), 400
    result = CommentService.add_comment(ticket_id, data)
    if result is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(result), 201
