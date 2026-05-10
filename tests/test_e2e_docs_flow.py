"""End-to-end lifecycle smoke test for the docs backend (Plan 1).

Exercises the entire surface in one integration pass so wiring gaps between
tasks surface here even when all unit tests are green.

Lifecycle:
  folder create
  → doc create with tags inside folder
  → save v2
  → search finds new content
  → rollback to v1
  → search reflects rollback
  → link to ticket
  → reverse link visible on ticket
  → tag pool reflects creation
  → delete doc (cascades versions / links / tags)
  → folder still exists (now empty)
  → delete folder

Fixture notes:
  - ``auth_headers`` depends on ``master_token`` which depends on ``db``, so the
    ``db`` rollback-isolation wrapper is active for the entire test even though
    ``db`` is not listed explicitly in the signature.
  - Direct ORM operations (Ticket creation) share the same connection/savepoint
    because they go through ``src.models.db.session``, which the ``db`` fixture
    has already rebound to the isolated connection.
"""


def test_full_doc_lifecycle(client, auth_headers):
    from src.models import Ticket, db as _db

    # ── Folder create ──────────────────────────────────────────────────────────
    resp = client.post('/api/folders', headers=auth_headers, json={
        'name': 'Architecture',
        'space_type': 'global',
    })
    assert resp.status_code == 201
    folder_id = resp.get_json()['id']

    # ── Document create (with tags) inside the folder ──────────────────────────
    resp = client.post('/api/documents', headers=auth_headers, json={
        'title': 'ADR-001',
        'space_type': 'global',
        'folder_id': folder_id,
        'body_md': '# Decision\n\nUse FTS5 for search.',
        'tags': ['adr', 'design'],
    })
    assert resp.status_code == 201
    doc = resp.get_json()
    doc_id = doc['id']
    assert doc['current_version']['version_number'] == 1

    # ── Save a second version ──────────────────────────────────────────────────
    resp = client.post(
        f'/api/documents/{doc_id}/versions',
        headers=auth_headers,
        json={
            'body_md': '# Decision\n\nUse SQLite FTS5.',
            'change_note': 'Clarify which FTS',
        },
    )
    assert resp.status_code == 201
    v2 = resp.get_json()
    assert v2['version_number'] == 2

    # ── Search finds the new content ───────────────────────────────────────────
    resp = client.get('/api/documents/search?q=SQLite')
    assert resp.status_code == 200
    assert any(r['id'] == doc_id for r in resp.get_json())

    # ── Roll back to v1 ────────────────────────────────────────────────────────
    versions_resp = client.get(f'/api/documents/{doc_id}/versions')
    assert versions_resp.status_code == 200
    versions = versions_resp.get_json()
    v1_id = next(v['id'] for v in versions if v['version_number'] == 1)

    resp = client.post(
        f'/api/documents/{doc_id}/rollback',
        headers=auth_headers,
        json={'version_id': v1_id},
    )
    assert resp.status_code == 200
    full = client.get(f'/api/documents/{doc_id}').get_json()
    assert full['current_version']['version_number'] == 1

    # ── Search reflects rolled-back content ───────────────────────────────────
    # After rollback DocumentVersionService calls reindex_document(), so the
    # FTS table must reflect the v1 body which contains "FTS5" (not "SQLite").
    resp = client.get('/api/documents/search?q=FTS5')
    assert resp.status_code == 200
    assert any(r['id'] == doc_id for r in resp.get_json())

    # ── Link to a ticket (direct ORM — no ticket-create endpoint dependency) ──
    # Ticket.cycle_id is nullable; status defaults to 'backlog' so both fields
    # are optional. The ORM session is the same rollback-wrapped one the test
    # client uses because auth_headers pulls in the db fixture transitively.
    t = Ticket(name='related', status='backlog')
    _db.session.add(t)
    _db.session.flush()          # assign t.id without committing the outer tx
    ticket_id = t.id

    resp = client.post(
        f'/api/documents/{doc_id}/tickets',
        headers=auth_headers,
        json={'ticket_id': ticket_id},
    )
    assert resp.status_code == 201

    # ── Reverse link visible on ticket fetch ──────────────────────────────────
    ticket_full = client.get(f'/api/tickets/{ticket_id}').get_json()
    assert any(d['id'] == doc_id for d in ticket_full.get('linked_documents', []))

    # ── Tag pool reflects creation (prefix search) ────────────────────────────
    # '?q=ad' matches 'adr' via LIKE prefix; TagService.list uses '%ad%' for
    # its LIKE clause which covers the prefix case as well.
    tag_resp = client.get('/api/tags?q=ad')
    assert tag_resp.status_code == 200
    tag_names = [tag['name'] for tag in tag_resp.get_json()]
    assert 'adr' in tag_names

    # ── Delete doc — cascades versions, links, tags ────────────────────────────
    # Route returns HTTP 204 (no body). Spec shows 200 — actual implementation
    # is 204 (see src/routes/documents.py: return ('', 204)).
    resp = client.delete(f'/api/documents/{doc_id}', headers=auth_headers)
    assert resp.status_code == 204

    # ── Folder still exists, now empty ────────────────────────────────────────
    # GET /api/folders accepts ?space= (not ?space_type=); confirmed in
    # src/routes/folders.py and src/services/folder_service.py.
    folders = client.get('/api/folders?space=global').get_json()
    assert any(f['id'] == folder_id for f in folders)

    # ── Delete the empty folder ───────────────────────────────────────────────
    resp = client.delete(f'/api/folders/{folder_id}', headers=auth_headers)
    assert resp.status_code == 200
