import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app, g, has_request_context
from src.models import db, Ticket, Attachment
from src.services.history_service import HistoryService


MAX_FILE_BYTES = 25 * 1024 * 1024  # 25MB


class AttachmentService:

    @staticmethod
    def _storage_root():
        """Per-instance attachment dir under <basedir>/instance/attachments."""
        basedir = current_app.config.get('basedir', os.path.dirname(current_app.root_path))
        root = os.path.join(basedir, 'instance', 'attachments')
        os.makedirs(root, exist_ok=True)
        return root

    @staticmethod
    def _storage_root_for_doc():
        basedir = current_app.config.get('basedir', os.path.dirname(current_app.root_path))
        root = os.path.join(basedir, 'instance', 'attachments', 'docs')
        os.makedirs(root, exist_ok=True)
        return root

    @staticmethod
    def _serialize(a):
        return {
            'id': a.id,
            'ticket_id': a.ticket_id,
            'document_id': a.document_id,
            'filename': a.filename,
            'content_type': a.content_type,
            'size_bytes': a.size_bytes,
            'uploader_name': a.uploader_name,
            'user_id': a.user_id,
            'created_at': str(a.created_at),
            'download_url': (
                f'/api/tickets/{a.ticket_id}/attachments/{a.id}/download'
                if a.ticket_id
                else f'/api/documents/{a.document_id}/attachments/{a.id}/download'
            ),
        }

    @staticmethod
    def list_attachments(ticket_id):
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            return None
        return [AttachmentService._serialize(a) for a in ticket.attachments.all()]

    @staticmethod
    def add_attachment(ticket_id, file_storage):
        """Persist an uploaded werkzeug FileStorage to disk + DB.

        Returns dict on success, {'error': ...} for validation, None for missing ticket.
        """
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            return None
        if not file_storage or not file_storage.filename:
            return {'error': 'No file provided'}

        # Streaming size check: read up to MAX+1 bytes to detect oversize without
        # buffering full uncapped uploads. Werkzeug already enforces MAX_CONTENT_LENGTH
        # at the WSGI layer, but we double-check here so the API returns a clean 413
        # instead of an opaque werkzeug error.
        file_storage.stream.seek(0, os.SEEK_END)
        size = file_storage.stream.tell()
        file_storage.stream.seek(0)
        if size > MAX_FILE_BYTES:
            return {'error': f'File too large (max {MAX_FILE_BYTES // (1024*1024)}MB)'}
        if size == 0:
            return {'error': 'Empty file'}

        original = secure_filename(file_storage.filename) or 'file'
        ext = os.path.splitext(original)[1]
        # Random storage filename keeps collisions impossible and avoids leaking
        # the original name onto disk; we display the original via DB.
        stored_name = f'{uuid.uuid4().hex}{ext}'
        storage_root = AttachmentService._storage_root()
        full_path = os.path.join(storage_root, stored_name)
        file_storage.save(full_path)

        uploader = None
        uid = None
        if has_request_context():
            uploader = getattr(g, 'user_name', None)
            uid = getattr(g, 'user_id', None)
        if not uploader:
            uploader = 'Anonymous'

        a = Attachment(
            ticket_id=ticket_id,
            filename=original,
            content_type=file_storage.mimetype or 'application/octet-stream',
            size_bytes=size,
            storage_path=stored_name,
            uploader_name=uploader,
            user_id=uid,
        )
        db.session.add(a)
        db.session.flush()
        HistoryService.log_ticket(ticket_id, 'attachment_added', None, original)
        db.session.commit()
        return AttachmentService._serialize(a)

    @staticmethod
    def list_for_document(doc_id):
        from src.models import Document
        if not Document.query.get(doc_id):
            return None
        rows = (Attachment.query.filter_by(document_id=doc_id)
                .order_by(Attachment.created_at).all())
        return [AttachmentService._serialize(a) for a in rows]

    @staticmethod
    def add_for_document(doc_id, file_storage):
        from src.models import Document
        if not Document.query.get(doc_id):
            return None
        if not file_storage or not file_storage.filename:
            return {'error': 'No file provided'}
        file_storage.stream.seek(0, os.SEEK_END)
        size = file_storage.stream.tell()
        file_storage.stream.seek(0)
        if size > MAX_FILE_BYTES:
            return {'error': f'File too large (max {MAX_FILE_BYTES // (1024*1024)}MB)'}
        if size == 0:
            return {'error': 'Empty file'}
        original = secure_filename(file_storage.filename) or 'file'
        ext = os.path.splitext(original)[1]
        stored_name = f'{uuid.uuid4().hex}{ext}'
        storage_root = AttachmentService._storage_root_for_doc()
        full_path = os.path.join(storage_root, stored_name)
        file_storage.save(full_path)
        uploader, uid = (None, None)
        if has_request_context():
            uploader = getattr(g, 'user_name', None)
            uid = getattr(g, 'user_id', None)
        if not uploader:
            uploader = 'Anonymous'
        a = Attachment(
            document_id=doc_id, filename=original,
            content_type=file_storage.mimetype or 'application/octet-stream',
            size_bytes=size,
            storage_path=os.path.join('docs', stored_name),  # path includes subdir
            uploader_name=uploader, user_id=uid,
        )
        db.session.add(a)
        db.session.flush()
        HistoryService.log(entity_type='document', entity_id=doc_id,
                           field_name='attachment_added', new_value=original)
        db.session.commit()
        return AttachmentService._serialize(a)

    @staticmethod
    def get_attachment(attachment_id):
        return Attachment.query.get(attachment_id)

    @staticmethod
    def storage_full_path(attachment):
        basedir = current_app.config.get('basedir', os.path.dirname(current_app.root_path))
        return os.path.join(basedir, 'instance', 'attachments', attachment.storage_path)

    @staticmethod
    def delete_attachment(attachment_id):
        a = Attachment.query.get(attachment_id)
        if not a:
            return False
        full = AttachmentService.storage_full_path(a)
        filename = a.filename
        if a.ticket_id:
            HistoryService.log(entity_type='ticket', entity_id=a.ticket_id,
                               field_name='attachment_removed', old_value=filename)
        else:
            HistoryService.log(entity_type='document', entity_id=a.document_id,
                               field_name='attachment_removed', old_value=filename)
        db.session.delete(a)
        db.session.commit()
        try:
            if os.path.exists(full):
                os.remove(full)
        except OSError as e:
            current_app.logger.warning(
                "attachment file unlink failed id=%s path=%s err=%s",
                attachment_id, full, e,
            )
        return True
