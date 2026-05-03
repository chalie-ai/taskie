from flask import Blueprint, request, jsonify
from src.services.project_service import ProjectService
from src.auth.jwt import require_auth

projects_bp = Blueprint('projects', __name__)


@projects_bp.route('/projects', methods=['GET'])
def list_projects():
    return jsonify(ProjectService.list_projects(
        cycle_id=request.args.get('cycle_id', type=int)))


@projects_bp.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    p = ProjectService.get_project(project_id)
    if not p:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(p)


@projects_bp.route('/projects', methods=['POST'])
@require_auth
def create_project():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'name is required'}), 400
    return jsonify(ProjectService.create_project(data)), 201


@projects_bp.route('/projects/<int:project_id>', methods=['PUT'])
@require_auth
def update_project(project_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400
    p = ProjectService.update_project(project_id, data)
    if not p:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(p)


@projects_bp.route('/projects/<int:project_id>', methods=['DELETE'])
@require_auth
def delete_project(project_id):
    if not ProjectService.delete_project(project_id):
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'deleted': True})
