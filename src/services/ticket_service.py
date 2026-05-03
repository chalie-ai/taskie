from datetime import datetime
from src.models import db, Ticket, TicketHistory
from src.services.relationship_service import RelationshipService
from src.services.history_service import HistoryService


class TicketService:

    @staticmethod
    def ticker():
        latest = Ticket.query.order_by(Ticket.id.desc()).first()
        num = (latest.id + 1) if latest else 1
        return f"TKT-{num:02d}"

    @staticmethod
    def _serialize(t, include_details=False):
        base = {
            'id': t.id, 'display_id': t.display_id, 'name': t.name,
            'description': t.description, 'type': t.type, 'priority': t.priority,
            'status': t.status, 'project_id': t.project_id, 'cycle_id': t.cycle_id,
            'assignee': t.assignee,
            'due_date': str(t.due_date) if t.due_date else None,
            'sort_order': t.sort_order,
            'comment_count': t.comments.count(),
            'created_at': str(t.created_at), 'updated_at': str(t.updated_at),
        }
        if t.project:
            base['project_name'] = t.project.name
            base['project_color'] = t.project.color
        if include_details:
            base['comments'] = [{
                'id': c.id, 'body': c.body, 'author_type': c.author_type,
                'author_name': c.author_name, 'created_at': str(c.created_at),
                'pr_link': {
                    'id': c.pr_link.id, 'url': c.pr_link.url, 'title': c.pr_link.title,
                    'status': c.pr_link.status,
                } if c.pr_link else None,
            } for c in t.comments.all()]
            base['pr_links'] = [{
                'id': p.id, 'url': p.url, 'title': p.title, 'status': p.status,
                'created_at': str(p.created_at),
            } for p in t.pr_links.all()]
            base['relationships'] = RelationshipService.list_relationships(t.id)
            base['history'] = HistoryService.get_ticket_history(t.id)
        return base

    @staticmethod
    def list_tickets(cycle_id=None, project_id=None, status=None, assignee=None, search=None):
        q = Ticket.query
        if cycle_id:
            q = q.filter(Ticket.cycle_id == cycle_id)
        if project_id:
            q = q.filter(Ticket.project_id == project_id)
        if status:
            q = q.filter(Ticket.status == status)
        if assignee:
            q = q.filter(Ticket.assignee == assignee)
        if search:
            like = f'%{search}%'
            q = q.filter(
                db.or_(
                    Ticket.name.ilike(like),
                    Ticket.description.ilike(like),
                    Ticket.display_id.ilike(like),
                )
            )
        tickets = q.order_by(Ticket.sort_order, Ticket.created_at.desc()).all()
        return [TicketService._serialize(t) for t in tickets]

    @staticmethod
    def get_ticket(ticket_id):
        t = Ticket.query.get(ticket_id)
        if not t:
            return None
        return TicketService._serialize(t, include_details=True)

    @staticmethod
    def create_ticket(data):
        due_date = data.get('due_date')
        if isinstance(due_date, str) and due_date:
            due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
        elif due_date == '':
            due_date = None
        max_order = db.session.query(db.func.max(Ticket.sort_order)).filter(
            Ticket.status == data.get('status', 'backlog')).scalar() or 0
        t = Ticket(
            display_id=TicketService.ticker(),
            name=data['name'],
            description=data.get('description'),
            type=data.get('type', 'feature'),
            priority=data.get('priority', 'none'),
            status=data.get('status', 'backlog'),
            project_id=data.get('project_id'),
            cycle_id=data.get('cycle_id'),
            assignee=data.get('assignee'),
            due_date=due_date,
            sort_order=max_order + 1,
        )
        db.session.add(t)
        db.session.commit()
        return TicketService.get_ticket(t.id)

    @staticmethod
    def update_ticket(ticket_id, data):
        t = Ticket.query.get(ticket_id)
        if not t:
            return None
        author = data.get('author_name', 'Dylan')
        allowed = ['name', 'description', 'type', 'priority', 'status',
                   'project_id', 'cycle_id', 'assignee', 'due_date', 'sort_order']
        for field in allowed:
            if field in data:
                old_val = getattr(t, field)
                new_val = data[field]
                if field == 'due_date' and isinstance(new_val, str):
                    if new_val:
                        new_val = datetime.strptime(new_val, '%Y-%m-%d').date()
                    else:
                        new_val = None
                if str(old_val) != str(new_val):
                    setattr(t, field, new_val)
                    h = TicketHistory(
                        ticket_id=ticket_id, author_name=author,
                        field_name=field,
                        old_value=str(old_val) if old_val is not None else None,
                        new_value=str(new_val),
                    )
                    db.session.add(h)
        db.session.commit()
        return TicketService.get_ticket(ticket_id)

    @staticmethod
    def reorder_tickets(items):
        for item in items:
            t = Ticket.query.get(item['id'])
            if t:
                if 'status' in item:
                    t.status = item['status']
                if 'sort_order' in item:
                    t.sort_order = item['sort_order']
        db.session.commit()
        return {'ok': True}

    @staticmethod
    def delete_ticket(ticket_id):
        t = Ticket.query.get(ticket_id)
        if not t:
            return False
        db.session.delete(t)
        db.session.commit()
        return True
