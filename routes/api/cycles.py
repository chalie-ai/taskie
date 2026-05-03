from flask import Blueprint, request, jsonify
from services import Services

cycles_bp = Blueprint('cycles', __name__)


@cycles_bp.route('/cycles', methods=['GET'])
def list_cycles():
    return jsonify(Services.list_cycles())


@cycles_bp.route('/cycles/<int:cycle_id>', methods=['GET'])
def get_cycle(cycle_id):
    c = Services.get_cycle(cycle_id)
    if not c:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(c)


@cycles_bp.route('/cycles', methods=['POST'])
def create_cycle():
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({'error': 'title is required'}), 400
    c = Services.create_cycle(data)
    return jsonify(c), 201


@cycles_bp.route('/cycles/<int:cycle_id>', methods=['PUT'])
def update_cycle(cycle_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400
    c = Services.update_cycle(cycle_id, data)
    if not c:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(c)


@cycles_bp.route('/cycles/<int:cycle_id>', methods=['DELETE'])
def delete_cycle(cycle_id):
    ok = Services.delete_cycle(cycle_id)
    if not ok:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'deleted': True})
