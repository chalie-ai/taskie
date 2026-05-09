from . import db, utcnow


class ActivityLog(db.Model):
    """Polymorphic audit trail. Replaces the legacy ``ticket_history`` table.

    ``entity_type`` + ``entity_id`` keep the row pointable at any first-class
    object (ticket, document, folder, doc-version, etc.) without requiring a
    foreign-key column per kind. The composite ``ix_activity_log_entity``
    index supports the common ``filter_by(entity_type=, entity_id=)`` lookup.
    """

    __tablename__ = 'activity_log'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    entity_type = db.Column(db.String(20), nullable=False, index=True)
    entity_id = db.Column(db.Integer, nullable=False, index=True)
    author_name = db.Column(db.String(255), default='System')
    field_name = db.Column(db.String(50), nullable=False)
    old_value = db.Column(db.Text)
    new_value = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=utcnow)
    user_id = db.Column(db.Integer, nullable=True)

    __table_args__ = (
        db.Index('ix_activity_log_entity', 'entity_type', 'entity_id'),
    )
