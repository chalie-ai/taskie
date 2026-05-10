from . import db, utcnow


class Attachment(db.Model):
    __tablename__ = 'attachments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id',
                                                       ondelete='CASCADE'),
                            nullable=True)
    filename = db.Column(db.String(255), nullable=False)
    content_type = db.Column(db.String(120))
    size_bytes = db.Column(db.Integer, nullable=False)
    storage_path = db.Column(db.String(500), nullable=False, unique=True)
    uploader_name = db.Column(db.String(255))
    user_id = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=utcnow)

    __table_args__ = (
        db.CheckConstraint(
            '(ticket_id IS NOT NULL AND document_id IS NULL) OR '
            '(ticket_id IS NULL AND document_id IS NOT NULL)',
            name='ck_attachment_one_parent',
        ),
    )
