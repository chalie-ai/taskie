from . import db, utcnow


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author_type = db.Column(db.String(20), default='human')
    author_name = db.Column(db.String(255), default='Dylan')
    created_at = db.Column(db.DateTime, default=utcnow)
    user_id = db.Column(db.Integer, nullable=True)

    pr_link = db.relationship('PRLink', backref='comment', uselist=False)
