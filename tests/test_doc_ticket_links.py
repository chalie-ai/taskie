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
