from . import db


class DocumentTag(db.Model):
    __tablename__ = 'document_tags'

    document_id = db.Column(db.Integer, db.ForeignKey('documents.id', ondelete='CASCADE'),
                            primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'),
                       primary_key=True)
