from datetime import date
from src.models import db, Cycle, CycleProject, Ticket


class CycleService:

    @staticmethod
    def _parse_date(val):
        if val is None:
            return None
        if isinstance(val, date):
            return val
        if isinstance(val, str):
            return date.fromisoformat(val)
        return None

    @staticmethod
    def _serialize(c):
        total = c.tickets.count()
        done = c.tickets.filter(Ticket.status.in_(['done', 'cancel'])).count()
        return {
            'id': c.id, 'title': c.title, 'description': c.description,
            'status': c.status,
            'start_date': str(c.start_date) if c.start_date else None,
            'end_date': str(c.end_date) if c.end_date else None,
            'active': c.status == 'in_progress',
            'total': total, 'done': done,
            'ticket_count': total,
            'project_ids': [p.id for p in c.projects],
            'projects': [{'id': p.id, 'name': p.name, 'color': p.color} for p in c.projects],
            'created_at': str(c.created_at), 'updated_at': str(c.updated_at),
        }

    @staticmethod
    def list_cycles(project_id=None, status=None):
        q = Cycle.query
        if project_id:
            q = q.join(CycleProject).filter(CycleProject.project_id == project_id)
        if status:
            q = q.filter(Cycle.status == status)
        cycles = q.order_by(Cycle.created_at.desc()).all()
        return [CycleService._serialize(c) for c in cycles]

    @staticmethod
    def get_cycle(cycle_id):
        c = db.session.get(Cycle, cycle_id)
        if not c:
            return None
        return CycleService._serialize(c)

    @staticmethod
    def _set_project_ids(cycle, project_ids):
        if project_ids is None:
            return
        from src.models import Project
        valid = Project.query.filter(Project.id.in_(project_ids)).all()
        cycle.projects = valid

    @staticmethod
    def create_cycle(data):
        c = Cycle(
            title=data['title'],
            description=data.get('description'),
            status=data.get('status', 'pending'),
            start_date=CycleService._parse_date(data.get('start_date')),
            end_date=CycleService._parse_date(data.get('end_date')),
        )
        db.session.add(c)
        db.session.flush()
        if 'project_ids' in data:
            CycleService._set_project_ids(c, data.get('project_ids') or [])
        db.session.commit()
        return CycleService.get_cycle(c.id)

    @staticmethod
    def update_cycle(cycle_id, data):
        c = db.session.get(Cycle, cycle_id)
        if not c:
            return None
        for field in ['title', 'description', 'status']:
            if field in data:
                setattr(c, field, data[field])
        for field in ['start_date', 'end_date']:
            if field in data:
                setattr(c, field, CycleService._parse_date(data[field]))
        if 'project_ids' in data:
            CycleService._set_project_ids(c, data.get('project_ids') or [])
        db.session.commit()
        return CycleService.get_cycle(c.id)

    @staticmethod
    def delete_cycle(cycle_id):
        c = db.session.get(Cycle, cycle_id)
        if not c:
            return False
        db.session.delete(c)
        db.session.commit()
        return True
