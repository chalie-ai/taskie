from flask import Blueprint, request, jsonify
from src.services.document_version_service import DocumentVersionService
from src.auth.jwt import require_auth, optional_auth

document_versions_bp = Blueprint('document_versions', __name__)


@document_versions_bp.route('/documents/<int:doc_id>/versions', methods=['GET'])
@optional_auth
def list_versions(doc_id):
    return jsonify(DocumentVersionService.list(doc_id))


@document_versions_bp.route('/documents/<int:doc_id>/versions', methods=['POST'])
@require_auth
def save_version(doc_id):
    data = request.get_json() or {}
    res = DocumentVersionService.save(doc_id, data)
    if res is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(res), 201


@document_versions_bp.route('/documents/<int:doc_id>/versions/<int:version_id>', methods=['GET'])
@optional_auth
def get_version(doc_id, version_id):
    v = DocumentVersionService.get(version_id)
    if not v or v['document_id'] != doc_id:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(v)


@document_versions_bp.route('/documents/<int:doc_id>/rollback', methods=['POST'])
@require_auth
def rollback(doc_id):
    data = request.get_json() or {}
    version_id = data.get('version_id')
    if not version_id:
        return jsonify({'error': 'version_id is required'}), 400
    res = DocumentVersionService.rollback(doc_id, version_id)
    if res is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(res)
