from flask import Blueprint, request, jsonify
from src.services.cycle_service import CycleService
from src.auth.jwt import require_auth

cycles_bp = Blueprint('cycles', __name__)


@cycles_bp.route('/cycles', methods=['GET'])
def list_cycles():
    return jsonify(CycleService.list_cycles(
        project_id=request.args.get('project_id', type=int),
        status=request.args.get('status'),
    ))


@cycles_bp.route('/cycles/<int:cycle_id>', methods=['GET'])
def get_cycle(cycle_id):
    c = CycleService.get_cycle(cycle_id)
    if not c:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(c)


@cycles_bp.route('/cycles', methods=['POST'])
@require_auth
def create_cycle():
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({'error': 'title is required'}), 400
    if not data.get('project_ids'):
        return jsonify({'error': 'At least one project is required'}), 400
    return jsonify(CycleService.create_cycle(data)), 201


@cycles_bp.route('/cycles/<int:cycle_id>', methods=['PUT'])
@require_auth
def update_cycle(cycle_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400
    c = CycleService.update_cycle(cycle_id, data)
    if not c:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(c)


@cycles_bp.route('/cycles/<int:cycle_id>', methods=['DELETE'])
@require_auth
def delete_cycle(cycle_id):
    if not CycleService.delete_cycle(cycle_id):
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'deleted': True})
