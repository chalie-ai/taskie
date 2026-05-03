from flask import Blueprint, request, jsonify
from services import Services

comments_bp = Blueprint('comments', __name__)


@comments_bp.route('/tickets/<int:ticket_id>/comments', methods=['GET'])
def list_comments(ticket_id):
    comments = Services.list_comments(ticket_id)
    if comments is None:
        return jsonify({'error': 'Ticket not found'}), 404
    return jsonify(comments)


@comments_bp.route('/tickets/<int:ticket_id>/comments', methods=['POST'])
def add_comment(ticket_id):
    data = request.get_json()
    if not data or not data.get('body'):
        return jsonify({'error': 'body is required'}), 400
    comments = Services.add_comment(ticket_id, data)
    if comments is None:
        return jsonify({'error': 'Ticket not found'}), 404
    return jsonify(comments), 201
