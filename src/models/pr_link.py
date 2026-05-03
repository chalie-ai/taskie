from . import db, utcnow


class PRLink(db.Model):
    __tablename__ = 'pr_links'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)
    url = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(255))
    status = db.Column(db.String(20), default='open')
    created_at = db.Column(db.DateTime, default=utcnow)
    user_id = db.Column(db.Integer, nullable=True)
