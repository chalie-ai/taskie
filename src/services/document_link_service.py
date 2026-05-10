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
        """Returns:
        - None  if doc or ticket is missing (404)
        - 'exists'  if the link already exists (idempotent no-op; HTTP 200)
        - True  if a new link row was created (HTTP 201)
        Activity log is only written on actual state change."""
        if not Document.query.get(document_id) or not Ticket.query.get(ticket_id):
            return None
        existing = DocumentTicketLink.query.filter_by(
            document_id=document_id, ticket_id=ticket_id).first()
        if existing:
            # Idempotent: no new row, no audit entry — only state changes are audited.
            return 'exists'
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
        # Single JOIN — composite-PK lookup on the link table starts with
        # document_id, so the ix_document_ticket_links_ticket_id index from
        # 0003 is what makes this efficient.
        rows = (db.session.query(Document)
                .join(DocumentTicketLink,
                      DocumentTicketLink.document_id == Document.id)
                .filter(DocumentTicketLink.ticket_id == ticket_id)
                .all())
        return [{
            'id': d.id, 'title': d.title,
            'space_type': d.space_type, 'project_id': d.project_id,
            'folder_id': d.folder_id,
        } for d in rows]
