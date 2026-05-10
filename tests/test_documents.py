def test_create_document_creates_v1(db):
    from src.services.document_service import DocumentService
    doc = DocumentService.create({
        'title': 'ADR-001 Use FTS5',
        'space_type': 'global',
        'body_md': '# Decision\n\nUse FTS5.',
    })
    assert doc['id'] is not None
    assert doc['current_version']['version_number'] == 1
    assert 'Use FTS5' in doc['current_version']['body_md']


def test_create_document_in_project_space(db):
    from src.services.document_service import DocumentService
    from src.models import Project, db as _db
    p = Project(name='Taskie')
    _db.session.add(p)
    _db.session.flush()
    doc = DocumentService.create({
        'title': 'README', 'space_type': 'project', 'project_id': p.id,
    })
    assert doc['space_type'] == 'project'
    assert doc['project_id'] == p.id


def test_get_document_includes_tags_and_links(db):
    from src.services.document_service import DocumentService
    doc = DocumentService.create({'title': 't', 'space_type': 'global',
                                  'tags': ['design', 'adr']})
    full = DocumentService.get(doc['id'])
    assert sorted(full['tags']) == ['adr', 'design']
    assert full['linked_ticket_ids'] == []
    assert full['attachments'] == []


def test_update_metadata_does_not_create_version(db):
    from src.services.document_service import DocumentService
    doc = DocumentService.create({'title': 'a', 'space_type': 'global',
                                  'body_md': 'one'})
    DocumentService.update_metadata(doc['id'], {'title': 'b', 'tags': ['x']})
    full = DocumentService.get(doc['id'])
    assert full['title'] == 'b'
    assert full['current_version']['version_number'] == 1


def test_delete_cascades_versions(db):
    from src.services.document_service import DocumentService
    from src.models import DocumentVersion
    doc = DocumentService.create({'title': 't', 'space_type': 'global',
                                  'body_md': 'x'})
    doc_id = doc['id']
    assert DocumentVersion.query.filter_by(document_id=doc_id).count() == 1
    assert DocumentService.delete(doc_id) is True
    assert DocumentVersion.query.filter_by(document_id=doc_id).count() == 0


def test_create_validates_space_type(db):
    from src.services.document_service import DocumentService
    res = DocumentService.create({'title': 't', 'space_type': 'invalid'})
    assert 'error' in res


def test_create_project_requires_project_id(db):
    from src.services.document_service import DocumentService
    res = DocumentService.create({'title': 't', 'space_type': 'project'})
    assert 'error' in res


def test_update_metadata_no_changes_does_not_update_updated_by(db):
    from src.services.document_service import DocumentService
    doc = DocumentService.create({'title': 'a', 'space_type': 'global',
                                  'body_md': 'one'})
    before_updated_by = doc['updated_by']
    DocumentService.update_metadata(doc['id'], {})  # nothing to change
    after = DocumentService.get(doc['id'])
    assert after['updated_by'] == before_updated_by


def test_create_sets_slug_from_title(db):
    from src.services.document_service import DocumentService
    doc = DocumentService.create({
        'title': 'ADR 001: Choose FTS5!', 'space_type': 'global',
    })
    assert doc['slug'] == 'adr-001-choose-fts5'


def test_create_with_sort_order(db):
    from src.services.document_service import DocumentService
    doc = DocumentService.create({
        'title': 'a', 'space_type': 'global', 'sort_order': 5,
    })
    assert doc['sort_order'] == 5


def test_update_metadata_title_updates_slug(db):
    from src.services.document_service import DocumentService
    doc = DocumentService.create({'title': 'old', 'space_type': 'global'})
    DocumentService.update_metadata(doc['id'], {'title': 'New Title!'})
    full = DocumentService.get(doc['id'])
    assert full['slug'] == 'new-title'


def test_delete_writes_activity_log(db):
    from src.services.document_service import DocumentService
    from src.models import ActivityLog
    doc = DocumentService.create({'title': 't', 'space_type': 'global'})
    doc_id = doc['id']
    before = ActivityLog.query.filter_by(
        entity_type='document', entity_id=doc_id,
        field_name='document_deleted'
    ).count()
    DocumentService.delete(doc_id)
    after = ActivityLog.query.filter_by(
        entity_type='document', entity_id=doc_id,
        field_name='document_deleted'
    ).count()
    assert after == before + 1


def test_list_pagination_limit_offset(db):
    from src.services.document_service import DocumentService
    for i in range(5):
        DocumentService.create({
            'title': f't{i}', 'space_type': 'global', 'sort_order': i,
        })
    page = DocumentService.list(space='global', limit=2, offset=2)
    assert len(page) == 2
    assert [d['title'] for d in page] == ['t2', 't3']


def test_create_rejects_folder_in_different_space(db):
    from src.services.document_service import DocumentService
    from src.services.folder_service import FolderService
    from src.models import Project, db as _db
    p = Project(name='Other')
    _db.session.add(p); _db.session.flush()
    proj_folder = FolderService.create({
        'name': 'pf', 'space_type': 'project', 'project_id': p.id,
    })
    res = DocumentService.create({
        'title': 't', 'space_type': 'global', 'folder_id': proj_folder['id'],
    })
    assert 'error' in res


def test_update_metadata_rejects_folder_in_different_space(db):
    from src.services.document_service import DocumentService
    from src.services.folder_service import FolderService
    from src.models import Project, db as _db
    p = Project(name='Other')
    _db.session.add(p); _db.session.flush()
    proj_folder = FolderService.create({
        'name': 'pf', 'space_type': 'project', 'project_id': p.id,
    })
    doc = DocumentService.create({'title': 't', 'space_type': 'global'})
    res = DocumentService.update_metadata(doc['id'], {
        'folder_id': proj_folder['id'],
    })
    assert isinstance(res, dict) and 'error' in res


def test_update_metadata_returns_full_document_shape(db):
    from src.services.document_service import DocumentService
    doc = DocumentService.create({'title': 'a', 'space_type': 'global'})
    res = DocumentService.update_metadata(doc['id'], {'title': 'b'})
    # Full shape includes tags/linked_ticket_ids/attachments (parity with get).
    assert 'tags' in res
    assert 'linked_ticket_ids' in res
    assert 'attachments' in res
