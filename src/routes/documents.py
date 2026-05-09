from flask import Blueprint, request, jsonify
from src.services.document_service import DocumentService
from src.auth.jwt import require_auth, optional_auth

documents_bp = Blueprint('documents', __name__)


@documents_bp.route('/documents', methods=['GET'])
@optional_auth
def list_documents():
    return jsonify(DocumentService.list(
        space=request.args.get('space'),
        project_id=request.args.get('project_id', type=int),
        folder_id=request.args.get('folder_id', type=int),
    ))


@documents_bp.route('/documents/<int:doc_id>', methods=['GET'])
@optional_auth
def get_document(doc_id):
    d = DocumentService.get(doc_id)
    if not d:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(d)


@documents_bp.route('/documents', methods=['POST'])
@require_auth
def create_document():
    data = request.get_json() or {}
    if not data.get('title'):
        return jsonify({'error': 'title is required'}), 400
    res = DocumentService.create(data)
    if isinstance(res, dict) and 'error' in res:
        return jsonify(res), 400
    return jsonify(res), 201


@documents_bp.route('/documents/<int:doc_id>', methods=['PATCH'])
@require_auth
def update_document_metadata(doc_id):
    data = request.get_json() or {}
    res = DocumentService.update_metadata(doc_id, data)
    if res is None:
        return jsonify({'error': 'Not found'}), 404
    if isinstance(res, dict) and 'error' in res:
        return jsonify(res), 400
    return jsonify(res)


@documents_bp.route('/documents/<int:doc_id>', methods=['DELETE'])
@require_auth
def delete_document(doc_id):
    res = DocumentService.delete(doc_id)
    if res is None:
        return jsonify({'error': 'Not found'}), 404
    return ('', 204)
