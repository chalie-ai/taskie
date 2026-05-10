from sqlalchemy.exc import IntegrityError
from src.models import db, Tag, DocumentTag


def _escape_like(s):
    """Escape LIKE/ILIKE wildcards so a user-supplied prefix like '%' or '_'
    matches literally instead of acting as a wildcard."""
    return s.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')


def _get_or_create_tag(norm):
    """Idempotent get-or-create. Retries on IntegrityError to survive
    concurrent INSERTs against the unique(name) constraint on PG/MySQL."""
    tag = Tag.query.filter_by(name=norm).first()
    if tag:
        return tag
    try:
        tag = Tag(name=norm)
        db.session.add(tag)
        db.session.flush()
        return tag
    except IntegrityError:
        db.session.rollback()
        return Tag.query.filter_by(name=norm).first()


class TagService:

    @staticmethod
    def _serialize(t):
        return {'id': t.id, 'name': t.name, 'created_at': str(t.created_at)}

    @staticmethod
    def list(q=None, limit=None):
        query = Tag.query
        if q:
            safe = _escape_like(q.lower())
            query = query.filter(Tag.name.ilike(f'{safe}%', escape='\\'))
        query = query.order_by(Tag.name)
        if limit is not None:
            query = query.limit(limit)
        return [TagService._serialize(t) for t in query.all()]

    @staticmethod
    def create(name):
        norm = (name or '').strip().lower()
        if not norm:
            return {'error': 'name is required'}
        tag = _get_or_create_tag(norm)
        db.session.commit()
        return TagService._serialize(tag)

    @staticmethod
    def delete(tag_id):
        t = Tag.query.get(tag_id)
        if not t:
            return False
        old_name = t.name
        affected = DocumentTag.query.filter_by(tag_id=tag_id).count()
        DocumentTag.query.filter_by(tag_id=tag_id).delete(synchronize_session=False)
        db.session.delete(t)
        from src.services.history_service import HistoryService
        HistoryService.log(entity_type='tag', entity_id=tag_id,
                           field_name='tag_deleted',
                           old_value=old_name, new_value=str(affected))
        db.session.commit()
        return True

    @staticmethod
    def attach(doc_id, name):
        """Attach a tag to a document. Flush-only — caller commits.
        Idempotent on (doc_id, tag_id)."""
        norm = (name or '').strip().lower()
        if not norm:
            return None
        tag = _get_or_create_tag(norm)
        existing = DocumentTag.query.filter_by(
            document_id=doc_id, tag_id=tag.id
        ).first()
        if not existing:
            db.session.add(DocumentTag(document_id=doc_id, tag_id=tag.id))
        db.session.flush()
        return TagService._serialize(tag)

    @staticmethod
    def detach(doc_id, name):
        norm = (name or '').strip().lower()
        tag = Tag.query.filter_by(name=norm).first()
        if not tag:
            return False
        DocumentTag.query.filter_by(document_id=doc_id, tag_id=tag.id).delete(
            synchronize_session=False)
        db.session.commit()
        return True

    @staticmethod
    def set_for_document(doc_id, names):
        """Replace the document's tag set atomically. Single commit at the end
        so a failure mid-loop rolls back the delete plus any partial attaches."""
        DocumentTag.query.filter_by(document_id=doc_id).delete(synchronize_session=False)
        for n in names:
            TagService.attach(doc_id, n)
        db.session.commit()

    @staticmethod
    def list_for_document(doc_id):
        rows = (db.session.query(Tag.name)
                .join(DocumentTag, DocumentTag.tag_id == Tag.id)
                .filter(DocumentTag.document_id == doc_id)
                .order_by(Tag.name).all())
        return [r[0] for r in rows]
