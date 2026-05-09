from flask import g, has_request_context
from src.models import db, Folder, Document


class FolderService:

    @staticmethod
    def _actor_id():
        if has_request_context():
            return getattr(g, 'user_id', None)
        return None

    @staticmethod
    def _serialize(f):
        return {
            'id': f.id, 'name': f.name,
            'parent_folder_id': f.parent_folder_id,
            'space_type': f.space_type, 'project_id': f.project_id,
            'sort_order': f.sort_order,
            'created_at': str(f.created_at), 'updated_at': str(f.updated_at),
            'created_by': f.created_by, 'updated_by': f.updated_by,
        }

    @staticmethod
    def list(space=None, project_id=None):
        q = Folder.query
        if space:
            q = q.filter(Folder.space_type == space)
        if project_id is not None:
            q = q.filter(Folder.project_id == project_id)
        return [FolderService._serialize(f)
                for f in q.order_by(Folder.sort_order, Folder.name).all()]

    @staticmethod
    def get(folder_id):
        f = Folder.query.get(folder_id)
        return FolderService._serialize(f) if f else None

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
        parent_folder_id = data.get('parent_folder_id')
        if parent_folder_id is not None:
            parent = Folder.query.get(parent_folder_id)
            if not parent:
                return {'error': 'parent_folder_id not found'}
            if parent.space_type != space or parent.project_id != project_id:
                return {'error': 'parent_folder_id is in a different space'}
        actor = FolderService._actor_id()
        f = Folder(
            name=data['name'],
            parent_folder_id=data.get('parent_folder_id'),
            space_type=space,
            project_id=project_id,
            sort_order=data.get('sort_order', 0),
            created_by=actor,
            updated_by=actor,
        )
        db.session.add(f)
        db.session.flush()
        from src.services.history_service import HistoryService
        HistoryService.log(entity_type='folder', entity_id=f.id,
                           field_name='folder_created', new_value=f.name)
        db.session.commit()
        return FolderService._serialize(f)

    @staticmethod
    def update(folder_id, data):
        f = Folder.query.get(folder_id)
        if not f:
            return None
        from src.services.history_service import HistoryService
        changed = False
        if 'parent_folder_id' in data:
            new_parent = data['parent_folder_id']
            if new_parent == folder_id:
                return {'error': 'cycle: folder cannot be its own parent'}
            if new_parent is not None:
                parent = Folder.query.get(new_parent)
                if not parent:
                    return {'error': 'parent_folder_id not found'}
                if parent.space_type != f.space_type or parent.project_id != f.project_id:
                    return {'error': 'parent_folder_id is in a different space'}
            # Walk up from new_parent; if we ever hit folder_id, the move would
            # create a cycle. Tree is assumed acyclic — Fix 3 guards against
            # dangling parents.
            cur = new_parent
            while cur is not None:
                if cur == folder_id:
                    return {'error': 'cycle: would create a folder loop'}
                row = Folder.query.get(cur)
                if row is None:
                    return {'error': 'parent chain references a missing folder; refuse to reparent'}
                cur = row.parent_folder_id
            old_val = f.parent_folder_id
            if str(old_val) != str(new_parent):
                f.parent_folder_id = new_parent
                HistoryService.log(entity_type='folder', entity_id=f.id,
                                   field_name='parent_folder_id',
                                   old_value=old_val, new_value=new_parent)
                changed = True
        for field in ('name', 'sort_order'):
            if field in data:
                old_val = getattr(f, field)
                new_val = data[field]
                if str(old_val) != str(new_val):
                    setattr(f, field, new_val)
                    HistoryService.log(entity_type='folder', entity_id=f.id,
                                       field_name=field,
                                       old_value=old_val, new_value=new_val)
                    changed = True
        if changed:
            f.updated_by = FolderService._actor_id()
        db.session.commit()
        return FolderService._serialize(f)

    @staticmethod
    def delete(folder_id, recursive=False):
        f = Folder.query.get(folder_id)
        if not f:
            return None
        has_children = (Folder.query.filter_by(parent_folder_id=folder_id).first()
                        is not None)
        has_docs = Document.query.filter_by(folder_id=folder_id).first() is not None
        if (has_children or has_docs) and not recursive:
            return 'non_empty'
        if recursive:
            FolderService._delete_recursive(folder_id)
        else:
            db.session.delete(f)
        from src.services.history_service import HistoryService
        HistoryService.log(entity_type='folder', entity_id=folder_id,
                           field_name='folder_deleted', old_value=f.name)
        db.session.commit()
        return True

    @staticmethod
    def _delete_recursive(folder_id):
        """Depth-first cascade: child folders + their documents, then this folder."""
        for child in Folder.query.filter_by(parent_folder_id=folder_id).all():
            FolderService._delete_recursive(child.id)
        from src.services.document_service import DocumentService
        for doc in Document.query.filter_by(folder_id=folder_id).all():
            DocumentService.delete(doc.id)
        f = Folder.query.get(folder_id)
        if f:
            db.session.delete(f)
