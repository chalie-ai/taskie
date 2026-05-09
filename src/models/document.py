from . import db, utcnow


class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(500), nullable=False)
    space_type = db.Column(db.String(10), nullable=False)  # 'global' | 'project'
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)
    folder_id = db.Column(db.Integer, db.ForeignKey('folders.id'), nullable=True)
    # FK to document_versions — uses use_alter=True to break the circular DDL
    # dependency (document_versions.document_id → documents.id).
    current_version_id = db.Column(
        db.Integer,
        db.ForeignKey('document_versions.id', name='fk_documents_current_version',
                      use_alter=True),
        nullable=True,
    )
    created_at = db.Column(db.DateTime, default=utcnow)
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    current_version = db.relationship(
        'DocumentVersion',
        foreign_keys=[current_version_id],
        post_update=True,
    )
    versions = db.relationship(
        'DocumentVersion',
        foreign_keys='DocumentVersion.document_id',
        back_populates='document',
        lazy='dynamic',
        cascade='all, delete-orphan',
    )

    __table_args__ = (
        db.CheckConstraint(
            "(space_type = 'project' AND project_id IS NOT NULL) OR "
            "(space_type = 'global' AND project_id IS NULL)",
            name='ck_document_space_consistency',
        ),
    )
