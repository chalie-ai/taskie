from . import db, utcnow


class TicketRelationship(db.Model):
    __tablename__ = 'ticket_relationships'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    related_ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    relationship_type = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow)
    user_id = db.Column(db.Integer, nullable=True)

    ticket = db.relationship('Ticket', foreign_keys=[ticket_id], backref='relationships')
    related_ticket = db.relationship('Ticket', foreign_keys=[related_ticket_id])
