def test_search_finds_doc_by_title(db):
    from src.services.document_service import DocumentService
    from src.services.document_search_service import DocumentSearchService
    DocumentService.create({'title': 'How we use FTS5', 'space_type': 'global',
                            'body_md': 'x'})
    rows = DocumentSearchService.search(q='FTS5')
    assert any('FTS5' in r['title'] for r in rows)


def test_search_finds_doc_by_body(db):
    from src.services.document_service import DocumentService
    from src.services.document_search_service import DocumentSearchService
    DocumentService.create({'title': 'Architecture', 'space_type': 'global',
                            'body_md': 'We picked SQLite FTS5 for full-text.'})
    rows = DocumentSearchService.search(q='full-text')
    assert len(rows) >= 1
    assert 'snippet' in rows[0]


def test_search_indexes_current_version_after_save(db):
    from src.services.document_service import DocumentService
    from src.services.document_version_service import DocumentVersionService
    from src.services.document_search_service import DocumentSearchService
    doc = DocumentService.create({'title': 'doc', 'space_type': 'global',
                                  'body_md': 'old phrase'})
    DocumentVersionService.save(doc['id'], {'body_md': 'new shiny phrase'})
    assert any('shiny' in (r.get('snippet') or '').lower()
               for r in DocumentSearchService.search(q='shiny'))


def test_search_filters_by_space(db):
    from src.services.document_service import DocumentService
    from src.services.document_search_service import DocumentSearchService
    from src.models import Project, db as _db
    p = Project(name='Taskie')
    _db.session.add(p); _db.session.flush()
    DocumentService.create({'title': 'global doc', 'space_type': 'global',
                            'body_md': 'unique-phrase-aaa'})
    DocumentService.create({'title': 'project doc', 'space_type': 'project',
                            'project_id': p.id,
                            'body_md': 'unique-phrase-aaa'})
    rows = DocumentSearchService.search(q='unique-phrase-aaa', space='global')
    assert all(r['space_type'] == 'global' for r in rows)


def test_search_multiword_query_ands_tokens(db):
    from src.services.document_service import DocumentService
    from src.services.document_search_service import DocumentSearchService
    DocumentService.create({'title': 'Flask is a Python web framework',
                            'space_type': 'global', 'body_md': 'x'})
    DocumentService.create({'title': 'Just python here',
                            'space_type': 'global', 'body_md': 'x'})
    DocumentService.create({'title': 'Just flask here',
                            'space_type': 'global', 'body_md': 'x'})
    rows = DocumentSearchService.search(q='python flask')
    titles = [r['title'] for r in rows]
    # The doc with BOTH words must match. Docs with only one word must NOT.
    assert any('Flask is a Python web framework' == t for t in titles)
    assert not any('Just python here' == t for t in titles)
    assert not any('Just flask here' == t for t in titles)


def test_search_rest(client, db):
    from src.services.document_service import DocumentService
    DocumentService.create({'title': 'searchable', 'space_type': 'global',
                            'body_md': 'a unique searchable token'})
    resp = client.get('/api/documents/search?q=searchable')
    assert resp.status_code == 200
    body = resp.get_json()
    assert any('searchable' in r['title'] for r in body)
