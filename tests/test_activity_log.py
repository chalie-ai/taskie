"""Activity log: polymorphic rename of ticket_history.

Tests both the strict polymorphic ``log()`` API and the ``log_ticket()``
convenience wrapper that every existing service in src/services/ now uses.
"""

import pytest


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


def test_log_ticket_wrapper(db):
    """log_ticket() is the convenience wrapper for ticket audit entries."""
    from src.services.history_service import HistoryService
    from src.models import Ticket, ActivityLog
    t = Ticket(name='y', status='backlog')
    db.session.add(t)
    db.session.flush()
    HistoryService.log_ticket(t.id, 'status', 'backlog', 'todo')
    db.session.commit()
    rows = ActivityLog.query.filter_by(entity_type='ticket', entity_id=t.id).all()
    assert len(rows) == 1


def test_log_ticket_with_author_kwarg(db):
    """Mirrors comment_service.py / pr_link_service.py call shape:
    log_ticket(ticket_id, field, old, new, author_name='X')."""
    from src.services.history_service import HistoryService
    from src.models import Ticket, ActivityLog
    t = Ticket(name='z', status='backlog')
    db.session.add(t)
    db.session.flush()
    HistoryService.log_ticket(t.id, 'comment_added', None, 'preview text',
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
    HistoryService.log_ticket(t.id, 'ticket_created', None, 'compat')
    db.session.commit()
    entries = HistoryService.get_ticket_history(t.id)
    assert entries is not None
    assert len(entries) == 1
    assert entries[0]['field_name'] == 'ticket_created'
    # missing ticket → None (preserves 404 path in routes/tickets.py)
    assert HistoryService.get_ticket_history(999999) is None


def test_log_rejects_missing_entity_type(db):
    """The strict log() must reject calls that omit entity_type/entity_id —
    this is the safety net that prevents docs-section code from accidentally
    routing audit entries under entity_type='ticket'."""
    from src.services.history_service import HistoryService
    with pytest.raises(TypeError, match="entity_type and entity_id"):
        HistoryService.log(entity_type=None, entity_id=42, field_name='x')
    with pytest.raises(TypeError, match="entity_type and entity_id"):
        HistoryService.log(entity_type='document', entity_id=None, field_name='x')
