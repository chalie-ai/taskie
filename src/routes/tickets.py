from flask import Blueprint, request, jsonify
from src.services.ticket_service import TicketService
from src.services.relationship_service import RelationshipService
from src.services.history_service import HistoryService
from src.auth.jwt import require_auth, optional_auth

tickets_bp = Blueprint('tickets', __name__)


@tickets_bp.route('/tickets', methods=['GET'])
@optional_auth
def list_tickets():
    return jsonify(TicketService.list_tickets(
        cycle_id=request.args.get('cycle_id', type=int),
        project_id=request.args.get('project_id', type=int),
        status=request.args.get('status'),
        assignee=request.args.get('assignee'),
        assignee_id=request.args.get('assignee_id', type=int),
        search=request.args.get('search'),
    ))


@tickets_bp.route('/tickets/<int:ticket_id>', methods=['GET'])
@optional_auth
def get_ticket(ticket_id):
    t = TicketService.get_ticket(ticket_id)
    if not t:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(t)


@tickets_bp.route('/tickets', methods=['POST'])
@require_auth
def create_ticket():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'name is required'}), 400
    if not data.get('cycle_id'):
        return jsonify({'error': 'cycle_id is required'}), 400
    return jsonify(TicketService.create_ticket(data)), 201


@tickets_bp.route('/tickets/<int:ticket_id>', methods=['PATCH'])
@require_auth
def update_ticket(ticket_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400
    t = TicketService.update_ticket(ticket_id, data)
    if not t:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(t)


@tickets_bp.route('/tickets/<int:ticket_id>', methods=['DELETE'])
@require_auth
def delete_ticket(ticket_id):
    if not TicketService.delete_ticket(ticket_id):
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'deleted': True})


@tickets_bp.route('/tickets/reorder', methods=['PUT'])
@require_auth
def reorder_tickets():
    data = request.get_json()
    if not data or not data.get('items'):
        return jsonify({'error': 'items is required'}), 400
    return jsonify(TicketService.reorder_tickets(data['items']))


# ── Relationships ──

@tickets_bp.route('/tickets/<int:ticket_id>/relationships', methods=['GET'])
def list_relationships(ticket_id):
    r = RelationshipService.list_relationships(ticket_id)
    if r is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(r)


@tickets_bp.route('/tickets/<int:ticket_id>/relationships', methods=['POST'])
@require_auth
def add_relationship(ticket_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400
    result = RelationshipService.add_relationship(ticket_id, data)
    if result is None:
        return jsonify({'error': 'Not found'}), 404
    if isinstance(result, dict) and 'error' in result:
        return jsonify(result), 400
    return jsonify(result), 201


@tickets_bp.route('/tickets/<int:ticket_id>/relationships/<int:rel_id>', methods=['DELETE'])
@require_auth
def remove_relationship(ticket_id, rel_id):
    if not RelationshipService.remove_relationship(rel_id):
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'deleted': True})


# ── History ──

@tickets_bp.route('/tickets/<int:ticket_id>/history', methods=['GET'])
def get_ticket_history(ticket_id):
    h = HistoryService.get_ticket_history(ticket_id)
    if h is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(h)
