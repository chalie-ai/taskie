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
