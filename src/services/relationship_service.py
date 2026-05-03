from src.models import db, Ticket, TicketRelationship


class RelationshipService:

    @staticmethod
    def list_relationships(ticket_id):
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            return None
        return [{
            'id': r.id, 'ticket_id': r.ticket_id,
            'related_ticket_id': r.related_ticket_id,
            'relationship_type': r.relationship_type,
            'related_ticket_display_id': r.related_ticket.display_id,
            'related_ticket_name': r.related_ticket.name,
            'related_ticket_status': r.related_ticket.status,
            'created_at': str(r.created_at),
        } for r in ticket.relationships]

    @staticmethod
    def add_relationship(ticket_id, data):
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            return None
        rel_type = data.get('relationship_type')
        if rel_type not in ('related', 'blocked_by', 'blocks'):
            return {'error': "relationship_type must be 'related', 'blocked_by', or 'blocks'"}
        related_id = data.get('related_ticket_id')
        if not related_id or not Ticket.query.get(related_id):
            return {'error': 'related_ticket_id is invalid'}
        if ticket_id == related_id:
            return {'error': 'Cannot relate a ticket to itself'}
        existing = TicketRelationship.query.filter_by(
            ticket_id=ticket_id, related_ticket_id=related_id,
            relationship_type=rel_type).first()
        if existing:
            return {'error': 'Relationship already exists'}
        r = TicketRelationship(
            ticket_id=ticket_id,
            related_ticket_id=related_id,
            relationship_type=rel_type,
        )
        db.session.add(r)
        db.session.commit()
        return RelationshipService.list_relationships(ticket_id)

    @staticmethod
    def remove_relationship(relationship_id):
        r = TicketRelationship.query.get(relationship_id)
        if not r:
            return False
        db.session.delete(r)
        db.session.commit()
        return True
