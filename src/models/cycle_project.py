from . import db


class CycleProject(db.Model):
    __tablename__ = 'cycle_projects'

    cycle_id = db.Column(db.Integer, db.ForeignKey('cycles.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), primary_key=True)
