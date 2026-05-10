from flask import Blueprint, request, jsonify
from src.services.document_link_service import DocumentLinkService
from src.auth.jwt import require_auth

document_links_bp = Blueprint('document_links', __name__)


@document_links_bp.route('/documents/<int:doc_id>/tickets', methods=['POST'])
@require_auth
def link_ticket(doc_id):
    data = request.get_json() or {}
    ticket_id = data.get('ticket_id')
    if not ticket_id:
        return jsonify({'error': 'ticket_id is required'}), 400
    res = DocumentLinkService.link(doc_id, ticket_id)
    if res is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'linked': True}), 201


@document_links_bp.route('/documents/<int:doc_id>/tickets/<int:ticket_id>',
                         methods=['DELETE'])
@require_auth
def unlink_ticket(doc_id, ticket_id):
    if not DocumentLinkService.unlink(doc_id, ticket_id):
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'unlinked': True})
