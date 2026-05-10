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


def test_rest_create_tag(client, auth_headers):
    resp = client.post('/api/tags', json={'name': 'roadmap'},
                       headers=auth_headers)
    assert resp.status_code == 201
    assert resp.get_json()['name'] == 'roadmap'
