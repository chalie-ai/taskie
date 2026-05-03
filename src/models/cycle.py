from . import db, utcnow


class Cycle(db.Model):
    __tablename__ = 'cycles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=utcnow)
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow)
    user_id = db.Column(db.Integer, nullable=True)

    tickets = db.relationship('Ticket', backref='cycle', lazy='dynamic')
    projects = db.relationship('Project', secondary='cycle_projects', backref='cycles')
