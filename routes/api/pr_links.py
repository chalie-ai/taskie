from flask import Blueprint, request, jsonify
from services import Services

pr_links_bp = Blueprint('pr_links', __name__)


@pr_links_bp.route('/tickets/<int:ticket_id>/pr-links', methods=['GET'])
def list_pr_links(ticket_id):
    links = Services.list_pr_links(ticket_id)
    if links is None:
        return jsonify({'error': 'Ticket not found'}), 404
    return jsonify(links)


@pr_links_bp.route('/tickets/<int:ticket_id>/pr-links', methods=['POST'])
def add_pr_link(ticket_id):
    data = request.get_json()
    if not data or not data.get('url'):
        return jsonify({'error': 'url is required'}), 400
    pr = Services.add_pr_link(ticket_id, data)
    if pr is None:
        return jsonify({'error': 'Ticket not found'}), 404
    return jsonify(pr), 201


@pr_links_bp.route('/tickets/<int:ticket_id>/pr-links/<int:pr_id>', methods=['DELETE'])
def delete_pr_link(ticket_id, pr_id):
    ok = Services.delete_pr_link(pr_id)
    if not ok:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'deleted': True})
