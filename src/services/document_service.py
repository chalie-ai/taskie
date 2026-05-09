import re
import src.models as _models
from flask import g, has_request_context
from sqlalchemy.orm import joinedload
from src.models import db, Document, DocumentVersion, Folder


def _slugify(s):
    s = (s or '').strip().lower()
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s[:200] or 'untitled'


class DocumentService:

    @staticmethod
    def _actor_id():
        if has_request_context():
            return getattr(g, 'user_id', None)
        return None

    @staticmethod
    def _serialize_version(v):
        if v is None:
            return None
        return {
            'id': v.id,
            'version_number': v.version_number,
            'title': v.title,
            'body_md': v.body_md or '',
            'change_note': v.change_note,
            'created_at': str(v.created_at),
            'created_by': v.created_by,
        }

    @staticmethod
    def _serialize(d):
        return {
            'id': d.id,
            'title': d.title,
            'slug': d.slug,
            'sort_order': d.sort_order,
            'space_type': d.space_type,
            'project_id': d.project_id,
            'folder_id': d.folder_id,
            'current_version_id': d.current_version_id,
            'current_version': DocumentService._serialize_version(d.current_version),
            'created_at': str(d.created_at),
            'updated_at': str(d.updated_at),
            'created_by': d.created_by,
            'updated_by': d.updated_by,
        }

    @staticmethod
    def list(space=None, project_id=None, folder_id=None, tag=None, limit=None, offset=None):
        q = Document.query.options(joinedload(Document.current_version))
        if space:
            q = q.filter(Document.space_type == space)
        if project_id is not None:
            q = q.filter(Document.project_id == project_id)
        if folder_id is not None:
            q = q.filter(Document.folder_id == folder_id)
        if tag:
            Tag = getattr(_models, 'Tag', None)
            DocumentTag = getattr(_models, 'DocumentTag', None)
            if Tag is not None and DocumentTag is not None:
                q = (q.join(DocumentTag, DocumentTag.document_id == Document.id)
                      .join(Tag, Tag.id == DocumentTag.tag_id)
                      .filter(Tag.name == tag.lower()))
            # else: tag filter is a no-op until Task 6 lands
        q = q.order_by(Document.sort_order, Document.title)
        if limit is not None:
            q = q.limit(limit)
        if offset is not None:
            q = q.offset(offset)
        return [DocumentService._serialize(d) for d in q.all()]

    @staticmethod
    def get(doc_id):
        d = Document.query.get(doc_id)
        if not d:
            return None
        out = DocumentService._serialize(d)

        # TODO(task-6): drop TagService import guard once tag_service lands.
        TagService = None
        # TODO(task-7): drop DocumentLinkService import guard once document_link_service lands.
        DocumentLinkService = None
        # TODO(task-8): drop AttachmentService import guard once attachment_service gains list_for_document.
        AttachmentService = None
        try:
            from src.services.tag_service import TagService  # noqa: F811
        except ImportError:
            pass
        try:
            from src.services.document_link_service import DocumentLinkService  # noqa: F811
        except ImportError:
            pass
        try:
            from src.services.attachment_service import AttachmentService  # noqa: F811
        except ImportError:
            pass

        out['tags'] = TagService.list_for_document(doc_id) if TagService else []
        out['linked_ticket_ids'] = DocumentLinkService.list_ticket_ids(doc_id) if DocumentLinkService else []
        if AttachmentService and hasattr(AttachmentService, 'list_for_document'):
            out['attachments'] = AttachmentService.list_for_document(doc_id) or []
        else:
            out['attachments'] = []
        return out

    @staticmethod
    def create(data):
        space = data.get('space_type')
        project_id = data.get('project_id')
        if space not in ('global', 'project'):
            return {'error': "space_type must be 'global' or 'project'"}
        if space == 'project' and not project_id:
            return {'error': 'project_id required when space_type=project'}
        if space == 'global' and project_id:
            return {'error': 'project_id must be null when space_type=global'}
        title = data.get('title', '').strip()
        if not title:
            return {'error': 'title is required'}

        folder_id = data.get('folder_id')
        if folder_id is not None:
            folder = Folder.query.get(folder_id)
            if not folder:
                return {'error': 'folder_id not found'}
            if folder.space_type != space or folder.project_id != project_id:
                return {'error': 'folder_id is in a different space'}

        actor = DocumentService._actor_id()
        d = Document(
            title=title,
            slug=_slugify(title),
            sort_order=data.get('sort_order', 0),
            space_type=space,
            project_id=project_id,
            folder_id=folder_id,
            created_by=actor,
            updated_by=actor,
        )
        db.session.add(d)
        db.session.flush()  # get d.id

        # Create the initial version (v1)
        v1 = DocumentVersion(
            document_id=d.id,
            version_number=1,
            title=title,
            body_md=data.get('body_md', '') or '',
            change_note=data.get('change_note'),
            created_by=actor,
        )
        db.session.add(v1)
        db.session.flush()  # get v1.id

        d.current_version_id = v1.id
        db.session.flush()

        from src.services.history_service import HistoryService
        HistoryService.log(entity_type='document', entity_id=d.id,
                           field_name='document_created', new_value=title)

        # TODO(task-6): drop guard once tag_service lands
        try:
            from src.services.tag_service import TagService
            for name in data.get('tags', []) or []:
                TagService.attach(d.id, name)
        except ImportError:
            pass

        db.session.commit()
        return DocumentService.get(d.id)

    @staticmethod
    def update_metadata(doc_id, data):
        d = Document.query.get(doc_id)
        if not d:
            return None

        from src.services.history_service import HistoryService
        changed = False

        if 'title' in data and data['title'] != d.title:
            old_val = d.title
            d.title = data['title']
            d.slug = _slugify(data['title'])
            HistoryService.log(entity_type='document', entity_id=d.id,
                               field_name='title', old_value=old_val,
                               new_value=data['title'])
            changed = True

        if 'folder_id' in data and data['folder_id'] != d.folder_id:
            new_folder_id = data['folder_id']
            if new_folder_id is not None:
                folder = Folder.query.get(new_folder_id)
                if not folder:
                    return {'error': 'folder_id not found'}
                if folder.space_type != d.space_type or folder.project_id != d.project_id:
                    return {'error': 'folder_id is in a different space'}
            old_val = d.folder_id
            d.folder_id = new_folder_id
            HistoryService.log(entity_type='document', entity_id=d.id,
                               field_name='folder_id', old_value=old_val,
                               new_value=new_folder_id)
            changed = True

        if 'sort_order' in data and data['sort_order'] != d.sort_order:
            old_val = d.sort_order
            d.sort_order = data['sort_order']
            HistoryService.log(entity_type='document', entity_id=d.id,
                               field_name='sort_order', old_value=old_val,
                               new_value=data['sort_order'])
            changed = True

        # TODO(task-6): drop guard once tag_service lands
        if 'tags' in data:
            try:
                from src.services.tag_service import TagService
                TagService.set_for_document(doc_id, data['tags'])
                changed = True
            except ImportError:
                # TagService not available yet — accept the request silently
                # but do not stamp updated_by/updated_at for a no-op.
                pass

        if changed:
            d.updated_by = DocumentService._actor_id()

        db.session.commit()
        return DocumentService.get(doc_id)

    @staticmethod
    def delete(doc_id):
        d = Document.query.get(doc_id)
        if not d:
            return None

        # TODO(task-6): drop guard once DocumentTag model lands
        DocumentTag = getattr(_models, 'DocumentTag', None)
        # TODO(task-7): drop guard once DocumentTicketLink model lands
        DocumentTicketLink = getattr(_models, 'DocumentTicketLink', None)
        # TODO(task-8): drop guard once Attachment gains document_id column
        Attachment = getattr(_models, 'Attachment', None)

        if DocumentTag is not None:
            DocumentTag.query.filter_by(document_id=doc_id).delete(synchronize_session=False)
        if DocumentTicketLink is not None:
            DocumentTicketLink.query.filter_by(document_id=doc_id).delete(synchronize_session=False)
        if Attachment is not None and hasattr(Attachment, 'document_id'):
            Attachment.query.filter_by(document_id=doc_id).delete(synchronize_session=False)

        title = d.title  # capture before delete

        # Versions cascade via ORM relationship (cascade='all, delete-orphan'),
        # but we must clear current_version_id first to avoid FK conflict when
        # SQLite enforces the use_alter FK.
        d.current_version_id = None
        db.session.flush()
        DocumentVersion.query.filter_by(document_id=doc_id).delete(synchronize_session=False)
        db.session.delete(d)

        from src.services.history_service import HistoryService
        HistoryService.log(entity_type='document', entity_id=doc_id,
                           field_name='document_deleted', old_value=title)

        db.session.commit()
        return True
