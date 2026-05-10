"""Regression test: ProjectService.delete_project cascades docs/folders/attachments.

Commit 8c5e1f7 introduced the cascade. This test asserts every row class that
must be cleaned up IS gone after delete, and that unrelated rows (different
project, global space) are NOT touched.
"""
import io
import os


def test_project_delete_cascades_all_doc_content(app, db):
    """After delete_project:
    - project's folder, doc, versions, tags, ticket-links, and attachment are gone
    - the on-disk attachment file is gone
    - the FTS5 index has no entry for the deleted doc
    - the linked ticket still exists
    - the tag row itself still exists (other docs may use it)
    - the project row itself is gone
    """
    from sqlalchemy import text
    from werkzeug.datastructures import FileStorage

    from src.models import (
        db as _db, Project, Ticket,
        Folder, Document, DocumentVersion,
        DocumentTag, DocumentTicketLink, Attachment,
    )
    from src.services.project_service import ProjectService
    from src.services.folder_service import FolderService
    from src.services.document_service import DocumentService
    from src.services.document_link_service import DocumentLinkService
    from src.services.attachment_service import AttachmentService

    # ------------------------------------------------------------------
    # Setup: project + folder + doc + v2 + tag + ticket-link + attachment
    # ------------------------------------------------------------------
    p = Project(name='CascadeTest')
    _db.session.add(p)
    _db.session.flush()
    project_id = p.id

    folder_data = FolderService.create({
        'name': 'Specs',
        'space_type': 'project',
        'project_id': project_id,
    })
    assert 'id' in folder_data, folder_data
    folder_id = folder_data['id']

    doc_data = DocumentService.create({
        'title': 'Design Doc',
        'space_type': 'project',
        'project_id': project_id,
        'folder_id': folder_id,
        'body_md': 'Initial design notes.',
        'tags': ['cascade-tag'],
    })
    assert 'id' in doc_data, doc_data
    d_id = doc_data['id']

    # Save a second version
    from src.services.document_version_service import DocumentVersionService
    DocumentVersionService.save(d_id, {
        'body_md': 'Updated design notes for v2.',
        'change_note': 'v2',
    })

    # Create a ticket to link to the doc
    t = Ticket(name='linked-ticket', status='backlog')
    _db.session.add(t)
    _db.session.flush()
    ticket_id = t.id

    link_result = DocumentLinkService.link(d_id, ticket_id)
    assert link_result is not None  # None means 404

    # Upload a real attachment to the doc
    with app.app_context():
        file_content = b'attachment content for cascade test'
        fs = FileStorage(
            stream=io.BytesIO(file_content),
            filename='cascade_test.txt',
            content_type='text/plain',
        )
        att_data = AttachmentService.add_for_document(d_id, fs)
    assert 'id' in att_data, att_data
    att_id = att_data['id']

    # Capture the on-disk path BEFORE delete
    with app.app_context():
        att_row = Attachment.query.get(att_id)
        att_path = AttachmentService.storage_full_path(att_row)

    # Verify the file exists before we delete the project
    assert os.path.exists(att_path), f"Attachment file should exist at {att_path} before delete"

    # ------------------------------------------------------------------
    # Action
    # ------------------------------------------------------------------
    result = ProjectService.delete_project(project_id)
    assert result is True

    # ------------------------------------------------------------------
    # Positive assertions: everything in the project is gone
    # ------------------------------------------------------------------
    assert Folder.query.filter_by(project_id=project_id).count() == 0, \
        "All project folders must be deleted"

    assert Document.query.filter_by(project_id=project_id).count() == 0, \
        "All project documents must be deleted"

    assert DocumentVersion.query.filter(
        DocumentVersion.document_id == d_id
    ).count() == 0, "All versions for the deleted doc must be deleted"

    assert DocumentTag.query.filter_by(document_id=d_id).count() == 0, \
        "document_tags rows for the deleted doc must be deleted"

    assert DocumentTicketLink.query.filter_by(document_id=d_id).count() == 0, \
        "document_ticket_links rows for the deleted doc must be deleted"

    assert Attachment.query.filter_by(document_id=d_id).count() == 0, \
        "Attachment rows for the deleted doc must be deleted"

    # On-disk file must be removed
    assert not os.path.exists(att_path), \
        f"Attachment file must be deleted from disk at {att_path}"

    # FTS5 index must have no entry for the deleted doc
    fts_rows = _db.session.execute(
        text("SELECT document_id FROM document_fts WHERE document_id = :id"),
        {"id": d_id},
    ).fetchall()
    assert len(fts_rows) == 0, "FTS5 index must have no entry for the deleted document"

    # Project row itself is gone
    assert Project.query.get(project_id) is None, "Project row must be deleted"

    # ------------------------------------------------------------------
    # Negative assertions: unrelated rows survive
    # ------------------------------------------------------------------
    # The linked ticket is NOT deleted
    surviving_ticket = Ticket.query.get(ticket_id)
    assert surviving_ticket is not None, "Linked ticket must survive project delete"

    # The tag row itself is NOT deleted (shared resource)
    from src.models import Tag
    surviving_tag = Tag.query.filter_by(name='cascade-tag').first()
    assert surviving_tag is not None, "Tag row must survive project delete"


def test_project_delete_does_not_affect_other_projects_or_global_space(app, db):
    """Deleting project A must not touch folders/docs belonging to project B
    or the global space.
    """
    from src.models import db as _db, Project, Folder, Document
    from src.services.project_service import ProjectService
    from src.services.folder_service import FolderService
    from src.services.document_service import DocumentService

    # Project A — will be deleted
    pa = Project(name='ProjectA')
    _db.session.add(pa)
    # Project B — must survive
    pb = Project(name='ProjectB')
    _db.session.add(pb)
    _db.session.flush()

    # Folder + doc in project A
    fa = FolderService.create({
        'name': 'FolderA', 'space_type': 'project', 'project_id': pa.id,
    })
    da = DocumentService.create({
        'title': 'DocA', 'space_type': 'project', 'project_id': pa.id,
        'folder_id': fa['id'], 'body_md': 'content a',
    })

    # Folder + doc in project B
    fb = FolderService.create({
        'name': 'FolderB', 'space_type': 'project', 'project_id': pb.id,
    })
    db_data = DocumentService.create({
        'title': 'DocB', 'space_type': 'project', 'project_id': pb.id,
        'folder_id': fb['id'], 'body_md': 'content b',
    })

    # Global folder + doc
    fg = FolderService.create({'name': 'GlobalFolder', 'space_type': 'global'})
    dg = DocumentService.create({
        'title': 'GlobalDoc', 'space_type': 'global',
        'folder_id': fg['id'], 'body_md': 'content global',
    })

    # Delete only project A
    ProjectService.delete_project(pa.id)

    # Project B folder and doc survive
    assert Folder.query.get(fb['id']) is not None, "Project B folder must survive"
    assert Document.query.get(db_data['id']) is not None, "Project B doc must survive"

    # Global folder and doc survive
    assert Folder.query.get(fg['id']) is not None, "Global folder must survive"
    assert Document.query.get(dg['id']) is not None, "Global doc must survive"
