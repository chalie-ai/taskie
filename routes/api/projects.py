from flask import Blueprint, request, jsonify
from services import Services

projects_bp = Blueprint('projects', __name__)


@projects_bp.route('/projects', methods=['GET'])
def list_projects():
    cycle_id = request.args.get('cycle_id', type=int)
    return jsonify(Services.list_projects(cycle_id=cycle_id))


@projects_bp.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    p = Services.get_project(project_id)
    if not p:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(p)


@projects_bp.route('/projects', methods=['POST'])
def create_project():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'name is required'}), 400
    p = Services.create_project(data)
    return jsonify(p), 201


@projects_bp.route('/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400
    p = Services.update_project(project_id, data)
    if not p:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(p)


@projects_bp.route('/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    ok = Services.delete_project(project_id)
    if not ok:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'deleted': True})
