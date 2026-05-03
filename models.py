from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()


class Cycle(db.Model):
    __tablename__ = 'cycles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, nullable=True)

    tickets = db.relationship('Ticket', backref='cycle', lazy='dynamic')
    projects = db.relationship('Project', secondary='cycle_projects', backref='cycles')


class CycleProject(db.Model):
    __tablename__ = 'cycle_projects'

    cycle_id = db.Column(db.Integer, db.ForeignKey('cycles.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), primary_key=True)


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(500))
    description = db.Column(db.Text)
    agent_instructions = db.Column(db.Text)
    color = db.Column(db.String(50), default='oklch(0.55 0.15 265)')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, nullable=True)

    git_repo_url = db.Column(db.String(500))

    tickets = db.relationship('Ticket', backref='project', lazy='dynamic')


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
    due_date = db.Column(db.Date, nullable=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, nullable=True)

    comments = db.relationship('Comment', backref='ticket', lazy='dynamic', order_by='Comment.created_at', cascade='all, delete-orphan')
    pr_links = db.relationship('PRLink', backref='ticket', lazy='dynamic', cascade='all, delete-orphan')


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author_type = db.Column(db.String(20), default='human')
    author_name = db.Column(db.String(255), default='Dylan')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, nullable=True)

    pr_link = db.relationship('PRLink', backref='comment', uselist=False)


class PRLink(db.Model):
    __tablename__ = 'pr_links'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)
    url = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(255))
    status = db.Column(db.String(20), default='open')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, nullable=True)


class TicketRelationship(db.Model):
    __tablename__ = 'ticket_relationships'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    related_ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    relationship_type = db.Column(db.String(20), nullable=False)  # related, blocked_by, blocks
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, nullable=True)

    ticket = db.relationship('Ticket', foreign_keys=[ticket_id], backref='relationships')
    related_ticket = db.relationship('Ticket', foreign_keys=[related_ticket_id])


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column(db.String(20), default='member')  # admin, member, viewer
    avatar_color = db.Column(db.String(50), default='oklch(0.55 0.15 265)')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class TicketHistory(db.Model):
    __tablename__ = 'ticket_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    author_name = db.Column(db.String(255), default='Dylan')
    field_name = db.Column(db.String(50), nullable=False)
    old_value = db.Column(db.Text)
    new_value = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, nullable=True)

    ticket = db.relationship('Ticket', backref='history_entries')
