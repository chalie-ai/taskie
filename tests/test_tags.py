def test_create_tag_lowercases(db):
    from src.services.tag_service import TagService
    t = TagService.create('Design')
    assert t['name'] == 'design'


def test_create_tag_idempotent(db):
    from src.services.tag_service import TagService
    a = TagService.create('design')
    b = TagService.create('design')
    assert a['id'] == b['id']


def test_attach_and_list_for_document(db):
    from src.services.document_service import DocumentService
    from src.services.tag_service import TagService
    doc = DocumentService.create({'title': 't', 'space_type': 'global',
                                  'body_md': 'x'})
    TagService.attach(doc['id'], 'design')
    TagService.attach(doc['id'], 'ADR')  # should normalize to 'adr'
    names = TagService.list_for_document(doc['id'])
    assert sorted(names) == ['adr', 'design']


def test_set_for_document_replaces(db):
    from src.services.document_service import DocumentService
    from src.services.tag_service import TagService
    doc = DocumentService.create({'title': 't', 'space_type': 'global',
                                  'body_md': 'x',
                                  'tags': ['old1', 'old2']})
    TagService.set_for_document(doc['id'], ['new1', 'new2'])
    assert sorted(TagService.list_for_document(doc['id'])) == ['new1', 'new2']


def test_autocomplete_q(db):
    from src.services.tag_service import TagService
    TagService.create('design-system')
    TagService.create('design')
    TagService.create('docs')
    rows = TagService.list(q='desi')
    names = [r['name'] for r in rows]
    assert 'design' in names and 'design-system' in names
    assert 'docs' not in names


def test_rest_create_tag(client, db, auth_headers):
    # `db` fixture must be requested explicitly so the SAVEPOINT-rollback
    # covers the route handler's commit (otherwise 'roadmap' leaks into
    # the session-scoped DB and pollutes downstream tests).
    resp = client.post('/api/tags', json={'name': 'roadmap'},
                       headers=auth_headers)
    assert resp.status_code == 201
    assert resp.get_json()['name'] == 'roadmap'


def test_list_q_wildcard_is_escaped(db):
    """`q='%'` must not act as a SQL LIKE wildcard — it should match a
    literal '%' prefix (i.e. no rows for ordinary alphanumeric tags)."""
    from src.services.tag_service import TagService
    TagService.create('design')
    TagService.create('docs')
    rows = TagService.list(q='%')
    assert rows == []


def test_list_limit_zero_returns_nothing(db):
    """`limit=0` must mean 'return zero rows', not 'return all'."""
    from src.services.tag_service import TagService
    TagService.create('a'); TagService.create('b')
    assert TagService.list(limit=0) == []
    # And limit=None still returns everything.
    assert len(TagService.list(limit=None)) == 2


def test_set_for_document_atomic_on_failure(db, monkeypatch):
    """If a partial failure happens mid-loop, the tag set must roll back
    rather than leaving the document with some-but-not-all new tags."""
    from src.services.document_service import DocumentService
    from src.services.tag_service import TagService
    doc = DocumentService.create({'title': 't', 'space_type': 'global',
                                  'body_md': 'x',
                                  'tags': ['keep1', 'keep2']})
    # Make the second attach blow up.
    real_attach = TagService.attach
    calls = {'n': 0}

    def flaky_attach(doc_id, name):
        calls['n'] += 1
        if calls['n'] == 2:
            raise RuntimeError('boom')
        return real_attach(doc_id, name)

    monkeypatch.setattr(TagService, 'attach', staticmethod(flaky_attach))
    import pytest
    with pytest.raises(RuntimeError):
        TagService.set_for_document(doc['id'], ['new1', 'new2', 'new3'])
    # The original tags must still be there — failure should not have
    # left the document with a half-applied tag set.
    from src.models import db as _db
    _db.session.rollback()
    names = TagService.list_for_document(doc['id'])
    assert sorted(names) == ['keep1', 'keep2']


def test_delete_tag_reindexes_affected_documents(db):
    """When a tag is deleted, the FTS index for every affected document
    must drop that tag's text — searching for the tag must NOT return the
    formerly-tagged document."""
    from src.services.document_service import DocumentService
    from src.services.tag_service import TagService
    from src.services.document_search_service import DocumentSearchService

    # Create a doc with a unique tag.
    doc = DocumentService.create({'title': 'Architecture',
                                  'space_type': 'global',
                                  'body_md': 'doc body',
                                  'tags': ['ghost-tag-xyz']})

    # Sanity: the tag is searchable.
    rows = DocumentSearchService.search(q='ghost-tag-xyz')
    assert any(r['id'] == doc['id'] for r in rows)

    # Delete the tag.
    tag_id = TagService.list(q='ghost-tag-xyz')[0]['id']
    TagService.delete(tag_id)

    # Search for the deleted tag — the doc should NO LONGER match.
    rows = DocumentSearchService.search(q='ghost-tag-xyz')
    assert not any(r['id'] == doc['id'] for r in rows), \
        "FTS index still contains the deleted tag's text"


def test_delete_writes_activity_log(db):
    from src.services.tag_service import TagService
    from src.services.document_service import DocumentService
    from src.models import ActivityLog
    doc = DocumentService.create({'title': 't', 'space_type': 'global',
                                  'tags': ['will-go']})
    tag_id = TagService.list(q='will')[0]['id']
    TagService.delete(tag_id)
    row = (ActivityLog.query
           .filter_by(entity_type='tag', entity_id=tag_id,
                      field_name='tag_deleted')
           .order_by(ActivityLog.id.desc()).first())
    assert row is not None
    assert row.old_value == 'will-go'
    assert row.new_value == '1'  # one document was affected
