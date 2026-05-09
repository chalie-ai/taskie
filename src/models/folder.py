from . import db, utcnow


class Folder(db.Model):
    __tablename__ = 'folders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    parent_folder_id = db.Column(db.Integer, db.ForeignKey('folders.id'), nullable=True)
    space_type = db.Column(db.String(10), nullable=False)  # 'global' | 'project'
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=utcnow)
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    children = db.relationship('Folder', backref=db.backref('parent', remote_side=[id]),
                               lazy='dynamic')

    __table_args__ = (
        db.UniqueConstraint('parent_folder_id', 'name', 'space_type', 'project_id',
                            name='uq_folder_sibling'),
        db.CheckConstraint(
            "(space_type = 'project' AND project_id IS NOT NULL) OR "
            "(space_type = 'global' AND project_id IS NULL)",
            name='ck_folder_space_consistency',
        ),
    )
