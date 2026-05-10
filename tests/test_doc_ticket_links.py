def test_link_doc_to_ticket(db):
    from src.services.document_service import DocumentService
    from src.services.document_link_service import DocumentLinkService
    from src.models import Ticket
    doc = DocumentService.create({'title': 't', 'space_type': 'global',
                                  'body_md': 'x'})
    ticket = Ticket(name='thing', status='backlog')
    db.session.add(ticket); db.session.flush()
    DocumentLinkService.link(doc['id'], ticket.id)
    assert DocumentLinkService.list_ticket_ids(doc['id']) == [ticket.id]
    assert DocumentLinkService.list_documents_for_ticket(ticket.id)[0]['id'] == doc['id']


def test_unlink_idempotent(db):
    from src.services.document_service import DocumentService
    from src.services.document_link_service import DocumentLinkService
    from src.models import Ticket
    doc = DocumentService.create({'title': 't', 'space_type': 'global',
                                  'body_md': 'x'})
    ticket = Ticket(name='thing', status='backlog')
    db.session.add(ticket); db.session.flush()
    DocumentLinkService.link(doc['id'], ticket.id)
    assert DocumentLinkService.unlink(doc['id'], ticket.id) is True
    assert DocumentLinkService.unlink(doc['id'], ticket.id) is False  # already gone


def test_ticket_serialize_includes_linked_documents(db):
    from src.services.document_service import DocumentService
    from src.services.document_link_service import DocumentLinkService
    from src.services.ticket_service import TicketService
    from src.models import Ticket
    doc = DocumentService.create({'title': 'design', 'space_type': 'global',
                                  'body_md': 'x'})
    ticket = Ticket(name='thing', status='backlog')
    db.session.add(ticket); db.session.flush()
    DocumentLinkService.link(doc['id'], ticket.id)
    full = TicketService.get_ticket(ticket.id)
    assert any(d['id'] == doc['id'] for d in full.get('linked_documents', []))


def test_link_returns_exists_on_idempotent_relink(db):
    """Re-linking an existing pair must return the 'exists' sentinel so the
    REST layer can map it to 200 instead of 201."""
    from src.services.document_service import DocumentService
    from src.services.document_link_service import DocumentLinkService
    from src.models import Ticket
    doc = DocumentService.create({'title': 't', 'space_type': 'global',
                                  'body_md': 'x'})
    ticket = Ticket(name='thing', status='backlog')
    db.session.add(ticket); db.session.flush()
    assert DocumentLinkService.link(doc['id'], ticket.id) is True
    assert DocumentLinkService.link(doc['id'], ticket.id) == 'exists'


def test_link_returns_none_for_missing_doc_or_ticket(db):
    from src.services.document_service import DocumentService
    from src.services.document_link_service import DocumentLinkService
    from src.models import Ticket
    doc = DocumentService.create({'title': 't', 'space_type': 'global',
                                  'body_md': 'x'})
    ticket = Ticket(name='thing', status='backlog')
    db.session.add(ticket); db.session.flush()
    assert DocumentLinkService.link(99999, ticket.id) is None
    assert DocumentLinkService.link(doc['id'], 99999) is None


def test_ticket_delete_cleans_up_links(db):
    """Deleting a ticket must clean up DocumentTicketLink rows. SQLite has
    PRAGMA foreign_keys=OFF, so the FK CASCADE never fires — TicketService
    must do the cleanup explicitly, like it already does for ActivityLog
    and TicketRelationship."""
    from src.services.document_service import DocumentService
    from src.services.document_link_service import DocumentLinkService
    from src.services.ticket_service import TicketService
    from src.models import Ticket, DocumentTicketLink
    doc = DocumentService.create({'title': 't', 'space_type': 'global',
                                  'body_md': 'x'})
    ticket = Ticket(name='thing', status='backlog')
    db.session.add(ticket); db.session.flush()
    ticket_id = ticket.id
    DocumentLinkService.link(doc['id'], ticket_id)
    assert DocumentTicketLink.query.filter_by(ticket_id=ticket_id).count() == 1
    TicketService.delete_ticket(ticket_id)
    assert DocumentTicketLink.query.filter_by(ticket_id=ticket_id).count() == 0
