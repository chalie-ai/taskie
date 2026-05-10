def test_create_global_folder(db):
    from src.services.folder_service import FolderService
    f = FolderService.create({
        'name': 'Architecture', 'space_type': 'global',
    })
    assert f['id'] is not None
    assert f['parent_folder_id'] is None
    assert f['space_type'] == 'global'


def test_create_project_folder_requires_project_id(db):
    from src.services.folder_service import FolderService
    res = FolderService.create({'name': 'Specs', 'space_type': 'project'})
    assert 'error' in res


def test_nested_folder(db):
    from src.services.folder_service import FolderService
    parent = FolderService.create({'name': 'Docs', 'space_type': 'global'})
    child = FolderService.create({
        'name': 'ADR', 'space_type': 'global', 'parent_folder_id': parent['id'],
    })
    assert child['parent_folder_id'] == parent['id']


def test_list_folders_filtered_by_space(db):
    from src.services.folder_service import FolderService
    FolderService.create({'name': 'A', 'space_type': 'global'})
    rows = FolderService.list(space='global')
    assert any(f['name'] == 'A' for f in rows)


def test_move_folder_rejects_cycle(db):
    from src.services.folder_service import FolderService
    a = FolderService.create({'name': 'A', 'space_type': 'global'})
    b = FolderService.create({'name': 'B', 'space_type': 'global',
                              'parent_folder_id': a['id']})
    res = FolderService.update(a['id'], {'parent_folder_id': b['id']})
    assert 'error' in res and 'cycle' in res['error'].lower()


def test_delete_non_empty_requires_recursive(db):
    from src.services.folder_service import FolderService
    a = FolderService.create({'name': 'A', 'space_type': 'global'})
    FolderService.create({'name': 'B', 'space_type': 'global',
                          'parent_folder_id': a['id']})
    res = FolderService.delete(a['id'], recursive=False)
    assert res == 'non_empty'
    assert FolderService.delete(a['id'], recursive=True) is True


def test_rest_create_folder(client, auth_headers):
    resp = client.post('/api/folders', json={
        'name': 'Architecture', 'space_type': 'global',
    }, headers=auth_headers)
    assert resp.status_code == 201
    assert resp.get_json()['name'] == 'Architecture'


def test_rest_list_folders_unauthed_ok(client, db):
    resp = client.get('/api/folders?space=global')
    assert resp.status_code == 200


def test_create_rejects_nonexistent_parent(db):
    from src.services.folder_service import FolderService
    res = FolderService.create({
        'name': 'X', 'space_type': 'global', 'parent_folder_id': 99999,
    })
    assert 'error' in res and 'not found' in res['error'].lower()


def test_create_rejects_cross_space_parent(db):
    from src.services.folder_service import FolderService
    from src.models import Project, db as _db
    p = Project(name='Taskie')
    _db.session.add(p)
    _db.session.flush()
    proj_root = FolderService.create({
        'name': 'ProjRoot', 'space_type': 'project', 'project_id': p.id,
    })
    res = FolderService.create({
        'name': 'GlobalChildOfProj', 'space_type': 'global',
        'parent_folder_id': proj_root['id'],
    })
    assert 'error' in res and 'different space' in res['error'].lower()


def test_update_rejects_cross_space_reparent(db):
    from src.services.folder_service import FolderService
    from src.models import Project, db as _db
    p = Project(name='Taskie')
    _db.session.add(p)
    _db.session.flush()
    g_folder = FolderService.create({'name': 'G', 'space_type': 'global'})
    p_folder = FolderService.create({
        'name': 'P', 'space_type': 'project', 'project_id': p.id,
    })
    res = FolderService.update(g_folder['id'],
                               {'parent_folder_id': p_folder['id']})
    assert 'error' in res and 'different space' in res['error'].lower()


def test_update_rejects_nonexistent_parent(db):
    from src.services.folder_service import FolderService
    f = FolderService.create({'name': 'A', 'space_type': 'global'})
    res = FolderService.update(f['id'], {'parent_folder_id': 99999})
    assert 'error' in res and 'not found' in res['error'].lower()


def test_update_noop_does_not_write_activity_log(db):
    from src.services.folder_service import FolderService
    from src.models import ActivityLog
    f = FolderService.create({'name': 'A', 'space_type': 'global'})
    before = ActivityLog.query.filter_by(
        entity_type='folder', entity_id=f['id']
    ).count()
    # PATCH with the same values — no fields actually change
    FolderService.update(f['id'], {'name': 'A', 'sort_order': 0})
    after = ActivityLog.query.filter_by(
        entity_type='folder', entity_id=f['id']
    ).count()
    assert after == before  # no per-field change → no log entry


def test_update_logs_per_changed_field(db):
    from src.services.folder_service import FolderService
    from src.models import ActivityLog
    f = FolderService.create({'name': 'A', 'space_type': 'global'})
    FolderService.update(f['id'], {'name': 'B', 'sort_order': 5})
    rows = ActivityLog.query.filter_by(
        entity_type='folder', entity_id=f['id']
    ).all()
    fields = sorted(r.field_name for r in rows)
    # 'folder_created' from create + 'name' + 'sort_order' from update
    assert 'name' in fields and 'sort_order' in fields
