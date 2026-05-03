from . import db, utcnow


class TicketHistory(db.Model):
    __tablename__ = 'ticket_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    author_name = db.Column(db.String(255), default='Dylan')
    field_name = db.Column(db.String(50), nullable=False)
    old_value = db.Column(db.Text)
    new_value = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=utcnow)
    user_id = db.Column(db.Integer, nullable=True)

    ticket = db.relationship('Ticket', backref='history_entries')
