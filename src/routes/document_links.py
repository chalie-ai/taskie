from flask import Blueprint, request, jsonify
from src.services.document_link_service import DocumentLinkService
from src.auth.jwt import require_auth

document_links_bp = Blueprint('document_links', __name__)


@document_links_bp.route('/documents/<int:doc_id>/tickets', methods=['POST'])
@require_auth
def link_ticket(doc_id):
    data = request.get_json() or {}
    ticket_id = data.get('ticket_id')
    # Strict type check: a string ticket_id (e.g. 'TKT-42') would otherwise
    # silently coerce into a 404 instead of returning a clean 400.
    if not isinstance(ticket_id, int) or ticket_id <= 0:
        return jsonify({'error': 'ticket_id must be a positive integer'}), 400
    res = DocumentLinkService.link(doc_id, ticket_id)
    if res is None:
        return jsonify({'error': 'Not found'}), 404
    # 201 only when a new link row was created; idempotent re-link returns 200.
    status = 201 if res is True else 200
    return jsonify({'linked': True}), status


@document_links_bp.route('/documents/<int:doc_id>/tickets/<int:ticket_id>',
                         methods=['DELETE'])
@require_auth
def unlink_ticket(doc_id, ticket_id):
    if not DocumentLinkService.unlink(doc_id, ticket_id):
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'unlinked': True})
