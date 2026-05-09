from flask import g, has_request_context
from src.models import db, Document, DocumentVersion
from src.services.document_service import _slugify
from sqlalchemy import func


class DocumentVersionService:

    @staticmethod
    def _actor_id():
        if has_request_context():
            return getattr(g, 'user_id', None)
        return None

    @staticmethod
    def _serialize(v):
        return {
            'id': v.id,
            'document_id': v.document_id,
            'version_number': v.version_number,
            'title': v.title,
            'body_md': v.body_md or '',
            'change_note': v.change_note,
            'created_at': str(v.created_at),
            'created_by': v.created_by,
        }

    @staticmethod
    def list(doc_id):
        rows = (DocumentVersion.query
                .filter_by(document_id=doc_id)
                .order_by(DocumentVersion.version_number)
                .all())
        return [DocumentVersionService._serialize(v) for v in rows]

    @staticmethod
    def get(doc_id, version_id):
        v = DocumentVersion.query.filter_by(id=version_id, document_id=doc_id).first()
        return DocumentVersionService._serialize(v) if v else None

    @staticmethod
    def save(doc_id, data):
        d = Document.query.get(doc_id)
        if not d:
            return None

        new_title = data.get('title', d.title)

        # Next version_number is max existing + 1 (handles post-rollback saves)
        max_num = (db.session.query(func.max(DocumentVersion.version_number))
                   .filter(DocumentVersion.document_id == doc_id)
                   .scalar()) or 0

        actor = DocumentVersionService._actor_id()
        v = DocumentVersion(
            document_id=doc_id,
            version_number=max_num + 1,
            title=new_title,
            body_md=data.get('body_md', '') or '',
            change_note=data.get('change_note'),
            created_by=actor,
        )
        db.session.add(v)
        db.session.flush()

        d.current_version_id = v.id
        d.title = new_title
        d.slug = _slugify(new_title)
        d.updated_by = actor

        from src.services.history_service import HistoryService
        HistoryService.log(entity_type='document', entity_id=doc_id,
                           field_name='version_saved',
                           new_value=str(v.version_number))

        db.session.commit()
        return DocumentVersionService._serialize(v)

    @staticmethod
    def rollback(doc_id, version_id, change_note=None):
        d = Document.query.get(doc_id)
        if not d:
            return None
        v = DocumentVersion.query.filter_by(
            id=version_id, document_id=doc_id
        ).first()
        if not v:
            return None

        d.current_version_id = v.id
        d.title = v.title
        d.slug = _slugify(v.title)
        d.updated_by = DocumentVersionService._actor_id()

        from src.services.history_service import HistoryService
        log_value = f'v{v.version_number}'
        if change_note:
            log_value = f'{log_value}: {change_note}'
        HistoryService.log(entity_type='document', entity_id=doc_id,
                           field_name='version_rollback',
                           new_value=log_value)

        db.session.commit()
        return DocumentVersionService._serialize(v)
