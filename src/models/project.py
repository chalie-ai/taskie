from . import db, utcnow


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(500))
    description = db.Column(db.Text)
    agent_instructions = db.Column(db.Text)
    color = db.Column(db.String(50), default='oklch(0.55 0.15 265)')
    git_repo_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=utcnow)
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow)
    user_id = db.Column(db.Integer, nullable=True)

    tickets = db.relationship('Ticket', backref='project', lazy='dynamic')
