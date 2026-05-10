import io


def _fake_filestorage(filename, data):
    from werkzeug.datastructures import FileStorage
    import io
    return FileStorage(stream=io.BytesIO(data), filename=filename,
                       content_type='text/plain')


def test_upload_doc_attachment(client, auth_headers, db):
    from src.services.document_service import DocumentService
    doc = DocumentService.create({'title': 't', 'space_type': 'global',
                                  'body_md': 'x'})
    data = {'file': (io.BytesIO(b'hello world'), 'note.txt')}
    resp = client.post(f'/api/documents/{doc["id"]}/attachments',
                       data=data, content_type='multipart/form-data',
                       headers=auth_headers)
    assert resp.status_code == 201
    body = resp.get_json()
    assert body['filename'] == 'note.txt'
    assert body['document_id'] == doc['id']
    assert body['ticket_id'] is None


def test_list_doc_attachments(client, auth_headers, db):
    from src.services.document_service import DocumentService
    from src.services.attachment_service import AttachmentService
    doc = DocumentService.create({'title': 't', 'space_type': 'global',
                                  'body_md': 'x'})
    AttachmentService.add_for_document(doc['id'], _fake_filestorage('a.txt', b'A'))
    AttachmentService.add_for_document(doc['id'], _fake_filestorage('b.txt', b'B'))
    resp = client.get(f'/api/documents/{doc["id"]}/attachments',
                      headers=auth_headers)
    rows = resp.get_json()
    assert len(rows) == 2
    assert sorted(r['filename'] for r in rows) == ['a.txt', 'b.txt']


def test_delete_doc_attachment(client, auth_headers, db):
    from src.services.document_service import DocumentService
    import io
    doc = DocumentService.create({'title': 't', 'space_type': 'global',
                                  'body_md': 'x'})
    data = {'file': (io.BytesIO(b'hello'), 'note.txt')}
    upload = client.post(f'/api/documents/{doc["id"]}/attachments',
                         data=data, content_type='multipart/form-data',
                         headers=auth_headers)
    assert upload.status_code == 201
    attachment_id = upload.get_json()['id']

    resp = client.delete(
        f'/api/documents/{doc["id"]}/attachments/{attachment_id}',
        headers=auth_headers)
    assert resp.status_code == 200
    assert resp.get_json() == {'deleted': True}

    list_resp = client.get(f'/api/documents/{doc["id"]}/attachments',
                           headers=auth_headers)
    assert list_resp.get_json() == []
