from src.models import db, Ticket, TicketRelationship


INVERSE_TYPE = {
    'related': 'related',
    'blocks': 'blocked_by',
    'blocked_by': 'blocks',
}


class RelationshipService:

    @staticmethod
    def list_relationships(ticket_id):
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            return None
        results = []
        rels = TicketRelationship.query.filter(
            db.or_(
                TicketRelationship.ticket_id == ticket_id,
                TicketRelationship.related_ticket_id == ticket_id,
            )
        ).all()
        for r in rels:
            is_inverse = (r.related_ticket_id == ticket_id)
            if is_inverse:
                display_type = INVERSE_TYPE.get(r.relationship_type, r.relationship_type)
                other_ticket = r.ticket
                other_id = r.ticket_id
            else:
                display_type = r.relationship_type
                other_ticket = r.related_ticket
                other_id = r.related_ticket_id
            results.append({
                'id': r.id,
                'ticket_id': ticket_id,
                'related_ticket_id': other_id,
                'relationship_type': display_type,
                'related_ticket_display_id': other_ticket.display_id,
                'related_ticket_name': other_ticket.name,
                'related_ticket_status': other_ticket.status,
                'created_at': str(r.created_at),
            })
        return results

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

        existing = TicketRelationship.query.filter(
            db.or_(
                db.and_(
                    TicketRelationship.ticket_id == ticket_id,
                    TicketRelationship.related_ticket_id == related_id,
                ),
                db.and_(
                    TicketRelationship.ticket_id == related_id,
                    TicketRelationship.related_ticket_id == ticket_id,
                    TicketRelationship.relationship_type == INVERSE_TYPE.get(rel_type),
                ),
            )
        ).first()
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
