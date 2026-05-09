import pytest


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


@pytest.mark.skip(reason="requires Task 6 (tags) + Task 7 (links) + Task 8 (attachments.document_id)")
def test_get_document_includes_tags_and_links(db):
    from src.services.document_service import DocumentService
    doc = DocumentService.create({'title': 't', 'space_type': 'global',
                                  'tags': ['design', 'adr']})
    full = DocumentService.get(doc['id'])
    assert sorted(full['tags']) == ['adr', 'design']
    assert full['linked_ticket_ids'] == []
    assert full['attachments'] == []


@pytest.mark.skip(reason="requires Task 6 (tags)")
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
