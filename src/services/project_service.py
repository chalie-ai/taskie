from src.models import db, Project, CycleProject, Ticket


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
        db.session.delete(p)
        db.session.commit()
        return True
