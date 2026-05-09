from flask import Blueprint, request, jsonify
from src.services.folder_service import FolderService
from src.auth.jwt import require_auth, optional_auth

folders_bp = Blueprint('folders', __name__)


@folders_bp.route('/folders', methods=['GET'])
@optional_auth
def list_folders():
    return jsonify(FolderService.list(
        space=request.args.get('space'),
        project_id=request.args.get('project_id', type=int),
    ))


@folders_bp.route('/folders/<int:folder_id>', methods=['GET'])
@optional_auth
def get_folder(folder_id):
    f = FolderService.get(folder_id)
    if not f:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(f)


@folders_bp.route('/folders', methods=['POST'])
@require_auth
def create_folder():
    data = request.get_json() or {}
    if not data.get('name'):
        return jsonify({'error': 'name is required'}), 400
    res = FolderService.create(data)
    if isinstance(res, dict) and 'error' in res:
        return jsonify(res), 400
    return jsonify(res), 201


@folders_bp.route('/folders/<int:folder_id>', methods=['PATCH'])
@require_auth
def update_folder(folder_id):
    data = request.get_json() or {}
    res = FolderService.update(folder_id, data)
    if res is None:
        return jsonify({'error': 'Not found'}), 404
    if isinstance(res, dict) and 'error' in res:
        return jsonify(res), 400
    return jsonify(res)


@folders_bp.route('/folders/<int:folder_id>', methods=['DELETE'])
@require_auth
def delete_folder(folder_id):
    recursive = request.args.get('recursive', '').lower() in ('1', 'true', 'yes')
    res = FolderService.delete(folder_id, recursive=recursive)
    if res is None:
        return jsonify({'error': 'Not found'}), 404
    if res == 'non_empty':
        return jsonify({'error': 'Folder not empty; pass ?recursive=true'}), 409
    return jsonify({'deleted': True})
