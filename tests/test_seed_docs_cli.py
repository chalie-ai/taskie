"""Regression tests for `flask seed-docs` CLI command (commit d35beb7).

Tests run through the real CLI runner, real DB, and real services.
No mocks anywhere.
"""
from sqlalchemy import text


def test_seed_docs_fresh_db(app, db):
    """seed-docs populates folders, documents, tags, and FTS on a fresh DB."""
    from src.models import db as _db, Folder, Document, DocumentTag

    runner = app.test_cli_runner()
    result = runner.invoke(args=['seed-docs'])
    assert result.exit_code == 0, f"seed-docs failed:\n{result.output}"

    # At least 3 root folders must exist in global space
    global_root_folders = Folder.query.filter_by(
        space_type='global', parent_folder_id=None
    ).count()
    assert global_root_folders >= 3, \
        f"Expected at least 3 root folders, got {global_root_folders}"

    # At least 5 global documents
    global_doc_count = Document.query.filter_by(space_type='global').count()
    assert global_doc_count >= 5, \
        f"Expected at least 5 global docs, got {global_doc_count}"

    # At least one document has tags
    tagged_doc_count = (
        _db.session.query(DocumentTag.document_id)
        .distinct()
        .count()
    )
    assert tagged_doc_count >= 1, "Expected at least one tagged document after seed"

    # FTS5 has at least as many entries as there are global documents
    fts_count = _db.session.execute(
        text("SELECT COUNT(*) FROM document_fts")
    ).scalar()
    assert fts_count >= global_doc_count, \
        f"FTS5 count ({fts_count}) must be >= document count ({global_doc_count})"


def test_seed_docs_idempotent_second_call(app, db):
    """seed-docs called twice does not create duplicate folders."""
    from src.models import Folder

    runner = app.test_cli_runner()

    result1 = runner.invoke(args=['seed-docs'])
    assert result1.exit_code == 0, f"First seed-docs call failed:\n{result1.output}"

    count_after_first = Folder.query.filter_by(space_type='global').count()
    assert count_after_first >= 3

    result2 = runner.invoke(args=['seed-docs'])
    assert result2.exit_code == 0, f"Second seed-docs call failed:\n{result2.output}"

    count_after_second = Folder.query.filter_by(space_type='global').count()
    assert count_after_second == count_after_first, \
        "Second seed-docs call must not create additional folders (idempotent)"


def test_seed_docs_force_rebuilds(app, db):
    """seed-docs --force wipes existing data and re-seeds the canonical amount."""
    from src.models import Folder, Document

    runner = app.test_cli_runner()

    # First seed
    result = runner.invoke(args=['seed-docs'])
    assert result.exit_code == 0, f"Initial seed-docs failed:\n{result.output}"

    canonical_folder_count = Folder.query.filter_by(space_type='global').count()
    canonical_doc_count = Document.query.filter_by(space_type='global').count()
    assert canonical_folder_count >= 3

    # Force reseed
    result = runner.invoke(args=['seed-docs', '--force'])
    assert result.exit_code == 0, f"seed-docs --force failed:\n{result.output}"

    after_force_folders = Folder.query.filter_by(space_type='global').count()
    after_force_docs = Document.query.filter_by(space_type='global').count()

    # Should be same canonical amounts, not double
    assert after_force_folders == canonical_folder_count, \
        f"--force must rebuild to {canonical_folder_count} folders, got {after_force_folders}"
    assert after_force_docs == canonical_doc_count, \
        f"--force must rebuild to {canonical_doc_count} docs, got {after_force_docs}"
