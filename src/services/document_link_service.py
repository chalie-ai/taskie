from flask import g, has_request_context
from src.models import db, Document, Ticket, DocumentTicketLink
from src.services.history_service import HistoryService


class DocumentLinkService:

    @staticmethod
    def _actor_id():
        if has_request_context():
            return getattr(g, 'user_id', None)
        return None

    @staticmethod
    def link(document_id, ticket_id):
        if not Document.query.get(document_id) or not Ticket.query.get(ticket_id):
            return None
        existing = DocumentTicketLink.query.filter_by(
            document_id=document_id, ticket_id=ticket_id).first()
        if existing:
            return True
        db.session.add(DocumentTicketLink(
            document_id=document_id, ticket_id=ticket_id,
            created_by=DocumentLinkService._actor_id(),
        ))
        HistoryService.log(entity_type='document', entity_id=document_id,
                           field_name='linked_ticket', new_value=str(ticket_id))
        HistoryService.log(entity_type='ticket', entity_id=ticket_id,
                           field_name='linked_document', new_value=str(document_id))
        db.session.commit()
        return True

    @staticmethod
    def unlink(document_id, ticket_id):
        link = DocumentTicketLink.query.filter_by(
            document_id=document_id, ticket_id=ticket_id).first()
        if not link:
            return False
        db.session.delete(link)
        HistoryService.log(entity_type='document', entity_id=document_id,
                           field_name='unlinked_ticket', old_value=str(ticket_id))
        HistoryService.log(entity_type='ticket', entity_id=ticket_id,
                           field_name='unlinked_document', old_value=str(document_id))
        db.session.commit()
        return True

    @staticmethod
    def list_ticket_ids(document_id):
        rows = DocumentTicketLink.query.filter_by(document_id=document_id).all()
        return [r.ticket_id for r in rows]

    @staticmethod
    def list_documents_for_ticket(ticket_id):
        ids = [r.document_id for r in
               DocumentTicketLink.query.filter_by(ticket_id=ticket_id).all()]
        if not ids:
            return []
        docs = Document.query.filter(Document.id.in_(ids)).all()
        return [{
            'id': d.id, 'title': d.title,
            'space_type': d.space_type, 'project_id': d.project_id,
            'folder_id': d.folder_id,
        } for d in docs]
