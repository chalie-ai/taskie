from flask import g, has_request_context
from src.models import db, ActivityLog, Ticket


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
    def log(entity_type, entity_id, field_name, old_value=None, new_value=None,
            author_name=None, user_id=None):
        """Persist a polymorphic activity entry. Both ``entity_type`` and
        ``entity_id`` are required; pass them by name or positionally."""
        if entity_type is None or entity_id is None:
            raise TypeError(
                "HistoryService.log requires entity_type and entity_id; "
                "for ticket audit entries use HistoryService.log_ticket()."
            )
        if author_name is None or user_id is None:
            actor_name, actor_id = HistoryService._actor()
            if author_name is None:
                author_name = actor_name
            if user_id is None:
                user_id = actor_id
        h = ActivityLog(
            entity_type=entity_type,
            entity_id=entity_id,
            author_name=author_name,
            field_name=field_name,
            old_value=str(old_value) if old_value is not None else None,
            new_value=str(new_value) if new_value is not None else None,
            user_id=user_id,
        )
        db.session.add(h)
        return h

    @staticmethod
    def log_ticket(ticket_id, field_name, old_value=None, new_value=None,
                   author_name=None, user_id=None):
        """Convenience wrapper for ticket audit entries."""
        return HistoryService.log(
            'ticket', ticket_id, field_name,
            old_value=old_value, new_value=new_value,
            author_name=author_name, user_id=user_id,
        )

    @staticmethod
    def list_for_entity(entity_type, entity_id):
        """Polymorphic lookup. Returns serialized rows in chronological order."""
        rows = ActivityLog.query.filter_by(
            entity_type=entity_type, entity_id=entity_id
        ).order_by(ActivityLog.created_at).all()
        return [{
            'id': h.id, 'author_name': h.author_name,
            'field_name': h.field_name, 'old_value': h.old_value,
            'new_value': h.new_value, 'created_at': str(h.created_at),
        } for h in rows]

    # Compat alias: existing callers (routes/tickets.py, ticket_service.py)
    # use get_ticket_history(ticket_id). Returns None when the ticket is
    # missing so the route's 404 path keeps working.
    @staticmethod
    def get_ticket_history(ticket_id):
        if db.session.get(Ticket, ticket_id) is None:
            return None
        return HistoryService.list_for_entity('ticket', ticket_id)
