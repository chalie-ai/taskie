from flask import g, has_request_context
from src.models import Ticket, TicketHistory, db


class HistoryService:

    @staticmethod
    def _actor():
        """Resolve the current actor's name + id from the request context."""
        if not has_request_context():
            return ('System', None)
        uid = getattr(g, 'user_id', None)
        name = getattr(g, 'user_name', None)
        if not name and uid:
            from src.models.user import User
            u = db.session.get(User, uid)
            if u:
                name = u.name
        return (name or 'System', uid)

    @staticmethod
    def log(ticket_id, field_name, old_value=None, new_value=None,
            author_name=None, user_id=None):
        """Persist an activity entry. Pass field_name='comment_added',
        'pr_linked', 'relationship_added', etc. for non-field events."""
        if author_name is None or user_id is None:
            actor_name, actor_id = HistoryService._actor()
            if author_name is None:
                author_name = actor_name
            if user_id is None:
                user_id = actor_id
        h = TicketHistory(
            ticket_id=ticket_id,
            author_name=author_name,
            field_name=field_name,
            old_value=str(old_value) if old_value is not None else None,
            new_value=str(new_value) if new_value is not None else None,
            user_id=user_id,
        )
        db.session.add(h)
        return h

    @staticmethod
    def get_ticket_history(ticket_id):
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            return None
        return [{
            'id': h.id, 'author_name': h.author_name,
            'field_name': h.field_name, 'old_value': h.old_value,
            'new_value': h.new_value, 'created_at': str(h.created_at),
        } for h in ticket.history_entries]
