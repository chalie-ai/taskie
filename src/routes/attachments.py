from flask import Blueprint, request, jsonify, send_file, abort
from src.services.attachment_service import AttachmentService, MAX_FILE_BYTES
from src.auth.jwt import require_auth, optional_auth

attachments_bp = Blueprint('attachments', __name__)


@attachments_bp.route('/tickets/<int:ticket_id>/attachments', methods=['GET'])
@optional_auth
def list_attachments(ticket_id):
    items = AttachmentService.list_attachments(ticket_id)
    if items is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(items)


@attachments_bp.route('/tickets/<int:ticket_id>/attachments', methods=['POST'])
@require_auth
def upload_attachment(ticket_id):
    if 'file' not in request.files:
        return jsonify({'error': "No 'file' field in multipart body"}), 400
    f = request.files['file']
    result = AttachmentService.add_attachment(ticket_id, f)
    if result is None:
        return jsonify({'error': 'Ticket not found'}), 404
    if isinstance(result, dict) and 'error' in result:
        # 413 for the size-cap rejection so clients can render a friendly message.
        code = 413 if 'too large' in result['error'].lower() else 400
        return jsonify(result), code
    return jsonify(result), 201


@attachments_bp.route('/tickets/<int:ticket_id>/attachments/<int:attachment_id>/download', methods=['GET'])
@optional_auth
def download_attachment(ticket_id, attachment_id):
    a = AttachmentService.get_attachment(attachment_id)
    if not a or a.ticket_id != ticket_id:
        abort(404)
    full = AttachmentService.storage_full_path(a)
    return send_file(
        full,
        mimetype=a.content_type or 'application/octet-stream',
        as_attachment=True,
        download_name=a.filename,
    )


@attachments_bp.route('/tickets/<int:ticket_id>/attachments/<int:attachment_id>', methods=['DELETE'])
@require_auth
def delete_attachment(ticket_id, attachment_id):
    a = AttachmentService.get_attachment(attachment_id)
    if not a or a.ticket_id != ticket_id:
        return jsonify({'error': 'Not found'}), 404
    AttachmentService.delete_attachment(attachment_id)
    return jsonify({'deleted': True})
