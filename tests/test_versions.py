def test_save_creates_new_version_and_advances_pointer(db):
    from src.services.document_service import DocumentService
    from src.services.document_version_service import DocumentVersionService
    doc = DocumentService.create({'title': 't', 'space_type': 'global',
                                  'body_md': 'v1'})
    v2 = DocumentVersionService.save(doc['id'], {
        'body_md': 'v2', 'change_note': 'second pass',
    })
    assert v2['version_number'] == 2
    full = DocumentService.get(doc['id'])
    assert full['current_version']['version_number'] == 2


def test_save_returns_body(db):
    from src.services.document_service import DocumentService
    from src.services.document_version_service import DocumentVersionService
    doc = DocumentService.create({'title': 't', 'space_type': 'global',
                                  'body_md': 'v1'})
    v2 = DocumentVersionService.save(doc['id'], {'body_md': 'v2'})
    assert v2['body_md'] == 'v2'


def test_list_versions_chronological(db):
    from src.services.document_service import DocumentService
    from src.services.document_version_service import DocumentVersionService
    doc = DocumentService.create({'title': 't', 'space_type': 'global',
                                  'body_md': 'v1'})
    DocumentVersionService.save(doc['id'], {'body_md': 'v2'})
    DocumentVersionService.save(doc['id'], {'body_md': 'v3'})
    rows = DocumentVersionService.list(doc['id'])
    assert [r['version_number'] for r in rows] == [1, 2, 3]


def test_rollback_moves_pointer_does_not_create_version(db):
    from src.services.document_service import DocumentService
    from src.services.document_version_service import DocumentVersionService
    doc = DocumentService.create({'title': 't', 'space_type': 'global',
                                  'body_md': 'v1'})
    v2 = DocumentVersionService.save(doc['id'], {'body_md': 'v2'})
    DocumentVersionService.save(doc['id'], {'body_md': 'v3'})
    DocumentVersionService.rollback(doc['id'], v2['id'])
    full = DocumentService.get(doc['id'])
    assert full['current_version']['version_number'] == 2
    assert len(DocumentVersionService.list(doc['id'])) == 3


def test_save_after_rollback_is_max_plus_one(db):
    from src.services.document_service import DocumentService
    from src.services.document_version_service import DocumentVersionService
    doc = DocumentService.create({'title': 't', 'space_type': 'global',
                                  'body_md': 'v1'})
    v2 = DocumentVersionService.save(doc['id'], {'body_md': 'v2'})
    DocumentVersionService.save(doc['id'], {'body_md': 'v3'})
    DocumentVersionService.rollback(doc['id'], v2['id'])
    v4 = DocumentVersionService.save(doc['id'], {'body_md': 'v4'})
    assert v4['version_number'] == 4


def test_rollback_to_unknown_version_returns_none(db):
    from src.services.document_service import DocumentService
    from src.services.document_version_service import DocumentVersionService
    doc = DocumentService.create({'title': 't', 'space_type': 'global',
                                  'body_md': 'v1'})
    res = DocumentVersionService.rollback(doc['id'], 99999)
    assert res is None
