from . import db, utcnow


class DocumentTicketLink(db.Model):
    __tablename__ = 'document_ticket_links'

    document_id = db.Column(db.Integer,
                            db.ForeignKey('documents.id', ondelete='CASCADE'),
                            primary_key=True)
    ticket_id = db.Column(db.Integer,
                          db.ForeignKey('tickets.id', ondelete='CASCADE'),
                          primary_key=True)
    created_at = db.Column(db.DateTime, default=utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
