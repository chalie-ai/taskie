from src.models import db, Project, CycleProject, Ticket, Document, Folder


class ProjectService:

    @staticmethod
    def _serialize(p):
        return {
            'id': p.id, 'name': p.name, 'location': p.location,
            'description': p.description, 'agent_instructions': p.agent_instructions,
            'color': p.color, 'git_repo_url': p.git_repo_url,
            'ticket_count': p.tickets.count(),
            'open_count': p.tickets.filter(Ticket.status.notin_(['done', 'cancel'])).count(),
            'progress_count': p.tickets.filter(Ticket.status == 'progress').count(),
            'created_at': str(p.created_at), 'updated_at': str(p.updated_at),
        }

    @staticmethod
    def list_projects(cycle_id=None):
        q = Project.query
        if cycle_id:
            q = q.join(CycleProject).filter(CycleProject.cycle_id == cycle_id)
        return [ProjectService._serialize(p) for p in q.order_by(Project.name).all()]

    @staticmethod
    def get_project(project_id):
        p = db.session.get(Project, project_id)
        if not p:
            return None
        return ProjectService._serialize(p)

    @staticmethod
    def create_project(data):
        p = Project(
            name=data['name'],
            location=data.get('location'),
            description=data.get('description'),
            agent_instructions=data.get('agent_instructions'),
            color=data.get('color', 'oklch(0.55 0.15 265)'),
            git_repo_url=data.get('git_repo_url'),
        )
        db.session.add(p)
        db.session.commit()
        return ProjectService.get_project(p.id)

    @staticmethod
    def update_project(project_id, data):
        p = db.session.get(Project, project_id)
        if not p:
            return None
        for field in ['name', 'location', 'description', 'agent_instructions', 'color', 'git_repo_url']:
            if field in data:
                setattr(p, field, data[field])
        db.session.commit()
        return ProjectService.get_project(p.id)

    @staticmethod
    def delete_project(project_id):
        p = db.session.get(Project, project_id)
        if not p:
            return False

        # Tear down docs content first so FTS index and on-disk attachment files
        # are cleaned up. DocumentService.delete handles: document_tags,
        # document_ticket_links, attachment file removal, FTS5 deindex, and all
        # versions. Each call commits internally — that is intentional so every
        # document is fully torn down and its disk files removed before we move on.
        from src.services.document_service import DocumentService
        for doc in Document.query.filter_by(
            space_type='project', project_id=project_id
        ).all():
            DocumentService.delete(doc.id)

        # Delete root folders recursively. FolderService._delete_recursive handles
        # child folders and their documents depth-first; since we already deleted
        # all documents above, the recursive calls hit empty folders and just
        # remove them. The history log entry is written inside FolderService.delete.
        from src.services.folder_service import FolderService
        for folder in Folder.query.filter_by(
            space_type='project', project_id=project_id, parent_folder_id=None
        ).all():
            FolderService.delete(folder.id, recursive=True)

        # NOTE: project-scoped tickets and their attachments are also orphaned
        # when a project is deleted under SQLite (PRAGMA foreign_keys=OFF). That
        # is a pre-existing gap not introduced by the docs feature — ticket cascade
        # cleanup is tracked separately and is not changed here.

        db.session.delete(p)
        db.session.commit()
        return True
