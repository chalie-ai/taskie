from flask import Blueprint, request, jsonify
from services import Services

tickets_bp = Blueprint('tickets', __name__)


@tickets_bp.route('/tickets', methods=['GET'])
def list_tickets():
    return jsonify(Services.list_tickets(
        cycle_id=request.args.get('cycle_id', type=int),
        project_id=request.args.get('project_id', type=int),
        status=request.args.get('status'),
        assignee=request.args.get('assignee'),
        search=request.args.get('search'),
    ))


@tickets_bp.route('/tickets/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    t = Services.get_ticket(ticket_id)
    if not t:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(t)


@tickets_bp.route('/tickets', methods=['POST'])
def create_ticket():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'name is required'}), 400
    t = Services.create_ticket(data)
    return jsonify(t), 201


@tickets_bp.route('/tickets/<int:ticket_id>', methods=['PATCH'])
def update_ticket(ticket_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400
    t = Services.update_ticket(ticket_id, data)
    if not t:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(t)


@tickets_bp.route('/tickets/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    ok = Services.delete_ticket(ticket_id)
    if not ok:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'deleted': True})


@tickets_bp.route('/tickets/reorder', methods=['PUT'])
def reorder_tickets():
    data = request.get_json()
    if not data or not data.get('items'):
        return jsonify({'error': 'items is required'}), 400
    return jsonify(Services.reorder_tickets(data['items']))


@tickets_bp.route('/tickets/<int:ticket_id>/relationships', methods=['GET'])
def list_relationships(ticket_id):
    r = Services.list_relationships(ticket_id)
    if r is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(r)


@tickets_bp.route('/tickets/<int:ticket_id>/relationships', methods=['POST'])
def add_relationship(ticket_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400
    result = Services.add_relationship(ticket_id, data)
    if result is None:
        return jsonify({'error': 'Not found'}), 404
    if isinstance(result, dict) and 'error' in result:
        return jsonify(result), 400
    return jsonify(result), 201


@tickets_bp.route('/tickets/<int:ticket_id>/relationships/<int:rel_id>', methods=['DELETE'])
def remove_relationship(ticket_id, rel_id):
    ok = Services.remove_relationship(rel_id)
    if not ok:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'deleted': True})


@tickets_bp.route('/tickets/<int:ticket_id>/history', methods=['GET'])
def get_ticket_history(ticket_id):
    h = Services.get_ticket_history(ticket_id)
    if h is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(h)
