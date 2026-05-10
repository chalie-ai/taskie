from src.models import db, Tag, DocumentTag


class TagService:

    @staticmethod
    def _serialize(t):
        return {'id': t.id, 'name': t.name, 'created_at': str(t.created_at)}

    @staticmethod
    def list(q=None, limit=None):
        query = Tag.query
        if q:
            query = query.filter(Tag.name.ilike(f'{q.lower()}%'))
        query = query.order_by(Tag.name)
        if limit:
            query = query.limit(limit)
        return [TagService._serialize(t) for t in query.all()]

    @staticmethod
    def create(name):
        norm = (name or '').strip().lower()
        if not norm:
            return {'error': 'name is required'}
        existing = Tag.query.filter_by(name=norm).first()
        if existing:
            return TagService._serialize(existing)
        t = Tag(name=norm)
        db.session.add(t)
        db.session.commit()
        return TagService._serialize(t)

    @staticmethod
    def delete(tag_id):
        t = Tag.query.get(tag_id)
        if not t:
            return False
        DocumentTag.query.filter_by(tag_id=tag_id).delete(synchronize_session=False)
        db.session.delete(t)
        db.session.commit()
        return True

    @staticmethod
    def attach(doc_id, name):
        norm = (name or '').strip().lower()
        if not norm:
            return None
        tag = Tag.query.filter_by(name=norm).first()
        if not tag:
            tag = Tag(name=norm)
            db.session.add(tag)
            db.session.flush()
        existing = DocumentTag.query.filter_by(
            document_id=doc_id, tag_id=tag.id
        ).first()
        if not existing:
            db.session.add(DocumentTag(document_id=doc_id, tag_id=tag.id))
        db.session.commit()
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
        DocumentTag.query.filter_by(document_id=doc_id).delete(synchronize_session=False)
        for n in names:
            TagService.attach(doc_id, n)

    @staticmethod
    def list_for_document(doc_id):
        rows = (db.session.query(Tag.name)
                .join(DocumentTag, DocumentTag.tag_id == Tag.id)
                .filter(DocumentTag.document_id == doc_id)
                .order_by(Tag.name).all())
        return [r[0] for r in rows]
