"""Regression tests for `flask reindex-docs` CLI command (commit d35beb7).

Each test drives the real CLI runner through the real DB and real
DocumentSearchService — no mocks anywhere in the stack.
"""
from sqlalchemy import text


def test_reindex_full_rebuild_after_fts_corruption(app, db):
    """reindex-docs without flags rebuilds all docs, restoring corrupted FTS entries."""
    from src.models import db as _db
    from src.services.document_service import DocumentService
    from src.services.document_search_service import DocumentSearchService

    d1 = DocumentService.create({
        'title': 'Unique-alpha-word doc', 'space_type': 'global',
        'body_md': 'uniquealphaword content here',
    })
    d2 = DocumentService.create({
        'title': 'Unique-beta-word doc', 'space_type': 'global',
        'body_md': 'uniquebetaword content here',
    })
    d3 = DocumentService.create({
        'title': 'Unique-gamma-word doc', 'space_type': 'global',
        'body_md': 'uniquegammaword content here',
    })

    # All three must be findable before corruption
    assert any(r['id'] == d1['id'] for r in DocumentSearchService.search(q='uniquealphaword'))
    assert any(r['id'] == d2['id'] for r in DocumentSearchService.search(q='uniquebetaword'))
    assert any(r['id'] == d3['id'] for r in DocumentSearchService.search(q='uniquegammaword'))

    # Corrupt: remove d2 from FTS
    _db.session.execute(
        text("DELETE FROM document_fts WHERE document_id = :id"),
        {"id": d2['id']},
    )
    _db.session.commit()

    # d2 no longer findable
    assert not any(r['id'] == d2['id'] for r in DocumentSearchService.search(q='uniquebetaword'))

    # Rebuild
    runner = app.test_cli_runner()
    result = runner.invoke(args=['reindex-docs'])
    assert result.exit_code == 0, f"reindex-docs failed: {result.output}"

    # d2 findable again
    assert any(r['id'] == d2['id'] for r in DocumentSearchService.search(q='uniquebetaword'))
    # Others still findable
    assert any(r['id'] == d1['id'] for r in DocumentSearchService.search(q='uniquealphaword'))
    assert any(r['id'] == d3['id'] for r in DocumentSearchService.search(q='uniquegammaword'))


def test_reindex_space_global_filter(app, db):
    """--space global only reindexes global docs; project docs remain absent from FTS."""
    from src.models import db as _db, Project
    from src.services.document_service import DocumentService
    from src.services.document_search_service import DocumentSearchService

    p = Project(name='FilterTestProject')
    _db.session.add(p)
    _db.session.flush()

    dg = DocumentService.create({
        'title': 'Global filter doc', 'space_type': 'global',
        'body_md': 'globalfiltertoken',
    })
    dp = DocumentService.create({
        'title': 'Project filter doc', 'space_type': 'project',
        'project_id': p.id, 'body_md': 'projectfiltertoken',
    })

    # Wipe FTS completely
    _db.session.execute(text("DELETE FROM document_fts"))
    _db.session.commit()

    assert not any(r['id'] == dg['id'] for r in DocumentSearchService.search(q='globalfiltertoken'))
    assert not any(r['id'] == dp['id'] for r in DocumentSearchService.search(q='projectfiltertoken'))

    runner = app.test_cli_runner()
    result = runner.invoke(args=['reindex-docs', '--space', 'global'])
    assert result.exit_code == 0, f"reindex-docs --space global failed: {result.output}"

    # Global doc is now searchable
    assert any(r['id'] == dg['id'] for r in DocumentSearchService.search(q='globalfiltertoken'))
    # Project doc is still absent (not reindexed by --space global)
    assert not any(r['id'] == dp['id'] for r in DocumentSearchService.search(q='projectfiltertoken'))


def test_reindex_project_id_filter(app, db):
    """--project-id N only reindexes docs in project N."""
    from src.models import db as _db, Project
    from src.services.document_service import DocumentService
    from src.services.document_search_service import DocumentSearchService

    pa = Project(name='ProjectA-reindex')
    pb = Project(name='ProjectB-reindex')
    _db.session.add(pa)
    _db.session.add(pb)
    _db.session.flush()

    da1 = DocumentService.create({
        'title': 'PA doc one', 'space_type': 'project',
        'project_id': pa.id, 'body_md': 'projectatokenone',
    })
    da2 = DocumentService.create({
        'title': 'PA doc two', 'space_type': 'project',
        'project_id': pa.id, 'body_md': 'projectatokentwo',
    })
    dbp = DocumentService.create({
        'title': 'PB doc', 'space_type': 'project',
        'project_id': pb.id, 'body_md': 'projectbtoken',
    })

    # Wipe FTS completely
    _db.session.execute(text("DELETE FROM document_fts"))
    _db.session.commit()

    runner = app.test_cli_runner()
    result = runner.invoke(args=['reindex-docs', '--project-id', str(pa.id)])
    assert result.exit_code == 0, f"reindex-docs --project-id failed: {result.output}"

    # Project A docs are searchable
    assert any(r['id'] == da1['id'] for r in DocumentSearchService.search(q='projectatokenone'))
    assert any(r['id'] == da2['id'] for r in DocumentSearchService.search(q='projectatokentwo'))
    # Project B doc is still absent
    assert not any(r['id'] == dbp['id'] for r in DocumentSearchService.search(q='projectbtoken'))


def test_reindex_empty_db_exits_cleanly(app, db):
    """reindex-docs on a DB with no documents exits 0 and does not raise."""
    from src.models import db as _db

    # Wipe FTS; no documents created in this test
    _db.session.execute(text("DELETE FROM document_fts"))
    _db.session.commit()

    runner = app.test_cli_runner()
    result = runner.invoke(args=['reindex-docs'])
    assert result.exit_code == 0, f"reindex-docs on empty DB failed: {result.output}"
    assert 'Error' not in result.output and 'Traceback' not in result.output
