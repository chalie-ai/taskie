from src.models import Ticket


class HistoryService:

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
