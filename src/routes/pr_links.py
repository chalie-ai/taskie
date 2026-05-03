from flask import Blueprint, request, jsonify
from src.services.pr_link_service import PRLinkService
from src.auth.jwt import require_auth

pr_links_bp = Blueprint('pr_links', __name__)


@pr_links_bp.route('/tickets/<int:ticket_id>/pr-links', methods=['GET'])
def list_pr_links(ticket_id):
    p = PRLinkService.list_pr_links(ticket_id)
    if p is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(p)


@pr_links_bp.route('/tickets/<int:ticket_id>/pr-links', methods=['POST'])
@require_auth
def add_pr_link(ticket_id):
    data = request.get_json()
    if not data or not data.get('url'):
        return jsonify({'error': 'url is required'}), 400
    result = PRLinkService.add_pr_link(ticket_id, data)
    if result is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(result), 201


@pr_links_bp.route('/tickets/<int:ticket_id>/pr-links/<int:pr_id>', methods=['DELETE'])
@require_auth
def delete_pr_link(ticket_id, pr_id):
    if not PRLinkService.delete_pr_link(pr_id):
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'deleted': True})
