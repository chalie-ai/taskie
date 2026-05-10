import os
from flask import Blueprint, request, jsonify, send_file
from src.services.attachment_service import AttachmentService
from src.auth.jwt import require_auth, optional_auth

document_attachments_bp = Blueprint('document_attachments', __name__)


@document_attachments_bp.route('/documents/<int:doc_id>/attachments',
                                methods=['GET'])
@optional_auth
def list_doc_attachments(doc_id):
    res = AttachmentService.list_for_document(doc_id)
    if res is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(res)


@document_attachments_bp.route('/documents/<int:doc_id>/attachments',
                                methods=['POST'])
@require_auth
def add_doc_attachment(doc_id):
    if 'file' not in request.files:
        return jsonify({'error': "No 'file' field in multipart body"}), 400
    file = request.files['file']
    res = AttachmentService.add_for_document(doc_id, file)
    if res is None:
        return jsonify({'error': 'Not found'}), 404
    if isinstance(res, dict) and 'error' in res:
        code = 413 if 'too large' in res['error'].lower() else 400
        return jsonify(res), code
    return jsonify(res), 201


@document_attachments_bp.route(
    '/documents/<int:doc_id>/attachments/<int:attachment_id>',
    methods=['DELETE'])
@require_auth
def delete_doc_attachment(doc_id, attachment_id):
    a = AttachmentService.get_attachment(attachment_id)
    if not a or a.document_id != doc_id:
        return jsonify({'error': 'Not found'}), 404
    AttachmentService.delete_attachment(attachment_id)
    return jsonify({'deleted': True})


@document_attachments_bp.route(
    '/documents/<int:doc_id>/attachments/<int:attachment_id>/download',
    methods=['GET'])
@optional_auth
def download_doc_attachment(doc_id, attachment_id):
    a = AttachmentService.get_attachment(attachment_id)
    if not a or a.document_id != doc_id:
        return jsonify({'error': 'Not found'}), 404
    full = AttachmentService.storage_full_path(a)
    return send_file(
        full,
        mimetype=a.content_type or 'application/octet-stream',
        as_attachment=True,
        download_name=a.filename,
    )
