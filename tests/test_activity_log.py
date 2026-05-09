"""Activity log: polymorphic rename of ticket_history.

Tests both the new entity_type/entity_id surface and the legacy positional
ticket_id call shape used by every existing service in src/services/.
"""


def test_log_for_ticket_uses_polymorphic_columns(db):
    from src.services.history_service import HistoryService
    from src.models import Ticket, ActivityLog
    t = Ticket(name='x', status='backlog')
    db.session.add(t)
    db.session.flush()
    HistoryService.log(entity_type='ticket', entity_id=t.id,
                       field_name='created', new_value='x')
    db.session.commit()
    rows = ActivityLog.query.filter_by(entity_type='ticket', entity_id=t.id).all()
    assert len(rows) == 1
    assert rows[0].field_name == 'created'


def test_legacy_ticket_id_kwarg_still_works(db):
    """Compat shim: old call sites pass ticket_id as a positional/keyword arg."""
    from src.services.history_service import HistoryService
    from src.models import Ticket, ActivityLog
    t = Ticket(name='y', status='backlog')
    db.session.add(t)
    db.session.flush()
    HistoryService.log(t.id, 'status', 'backlog', 'todo')
    db.session.commit()
    rows = ActivityLog.query.filter_by(entity_type='ticket', entity_id=t.id).all()
    assert len(rows) == 1


def test_legacy_log_with_author_kwarg(db):
    """Mirrors comment_service.py / pr_link_service.py call shape:
    log(ticket_id, field, old, new, author_name='X')."""
    from src.services.history_service import HistoryService
    from src.models import Ticket, ActivityLog
    t = Ticket(name='z', status='backlog')
    db.session.add(t)
    db.session.flush()
    HistoryService.log(t.id, 'comment_added', None, 'preview text',
                       author_name='Alice')
    db.session.commit()
    rows = ActivityLog.query.filter_by(entity_type='ticket', entity_id=t.id).all()
    assert len(rows) == 1
    assert rows[0].author_name == 'Alice'
    assert rows[0].new_value == 'preview text'


def test_get_ticket_history_compat_alias(db):
    """Ticket route still calls HistoryService.get_ticket_history(ticket_id)."""
    from src.services.history_service import HistoryService
    from src.models import Ticket
    t = Ticket(name='compat', status='backlog')
    db.session.add(t)
    db.session.flush()
    HistoryService.log(t.id, 'ticket_created', None, 'compat')
    db.session.commit()
    entries = HistoryService.get_ticket_history(t.id)
    assert entries is not None
    assert len(entries) == 1
    assert entries[0]['field_name'] == 'ticket_created'
    # missing ticket → None (preserves 404 path in routes/tickets.py)
    assert HistoryService.get_ticket_history(999999) is None
