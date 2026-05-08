from . import db, utcnow


class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    display_id = db.Column(db.String(20))
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.String(20), default='feature')
    priority = db.Column(db.String(20), default='none')
    status = db.Column(db.String(20), default='backlog')
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    cycle_id = db.Column(db.Integer, db.ForeignKey('cycles.id'), nullable=True)
    assignee = db.Column(db.String(255), nullable=True)
    assignee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=utcnow)
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow)
    user_id = db.Column(db.Integer, nullable=True)

    comments = db.relationship('Comment', backref='ticket', lazy='dynamic',
                               order_by='Comment.created_at', cascade='all, delete-orphan')
    pr_links = db.relationship('PRLink', backref='ticket', lazy='dynamic', cascade='all, delete-orphan')
    attachments = db.relationship('Attachment', backref='ticket', lazy='dynamic',
                                  order_by='Attachment.created_at', cascade='all, delete-orphan')
    assignee_user = db.relationship('User', backref='assigned_tickets', foreign_keys=[assignee_id])
