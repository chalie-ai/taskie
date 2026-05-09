from . import db, utcnow


class DocumentVersion(db.Model):
    __tablename__ = 'document_versions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False)
    version_number = db.Column(db.Integer, nullable=False)
    body_md = db.Column(db.Text, default='')
    change_note = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    document = db.relationship(
        'Document',
        foreign_keys=[document_id],
        back_populates='versions',
    )

    __table_args__ = (
        db.UniqueConstraint('document_id', 'version_number',
                            name='uq_document_version_number'),
    )
