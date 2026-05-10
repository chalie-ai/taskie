from sqlalchemy import text
from src.models import db, Document
from src.services.tag_service import TagService


class DocumentSearchService:

    @staticmethod
    def _dialect():
        return db.engine.dialect.name

    @staticmethod
    def reindex_document(doc_id):
        """Re-emit the document into the FTS table (sqlite) or update search_body (mysql).

        If the document no longer exists (i.e. it was deleted), delegates to
        _delete_index to clean up any stale FTS rows and returns early.

        This method issues its own commit so it can be called safely after the
        caller's main transaction has already committed. It must NOT be called
        before the caller's commit — the FTS row would reference data that is
        not yet durable.
        """
        d = Document.query.get(doc_id)
        if not d:
            DocumentSearchService._delete_index(doc_id)
            return
        from src.models import DocumentVersion
        cv = DocumentVersion.query.get(d.current_version_id) if d.current_version_id else None
        body = cv.body_md if cv else ''
        tags = ' '.join(TagService.list_for_document(doc_id))
        if DocumentSearchService._dialect() == 'sqlite':
            db.session.execute(
                text("DELETE FROM document_fts WHERE document_id = :id"),
                {'id': doc_id},
            )
            db.session.execute(
                text(
                    "INSERT INTO document_fts (document_id, title, body, tags) "
                    "VALUES (:id, :title, :body, :tags)"
                ),
                {'id': doc_id, 'title': d.title, 'body': body, 'tags': tags},
            )
        else:
            d.search_body = f'{d.title}\n{body}\n{tags}'
        db.session.commit()

    @staticmethod
    def _delete_index(doc_id):
        """Remove a document from the FTS index. Called when the document row
        has already been deleted from the documents table."""
        if DocumentSearchService._dialect() == 'sqlite':
            db.session.execute(
                text("DELETE FROM document_fts WHERE document_id = :id"),
                {'id': doc_id},
            )
            db.session.commit()

    @staticmethod
    def _fts5_quote(q):
        """Wrap the user query in FTS5 double-quote phrase syntax so that
        special characters (hyphens, colons, etc.) are treated as literals
        rather than FTS5 operator tokens. Embedded double-quotes are escaped
        by doubling them per the FTS5 spec.
        """
        return '"' + q.replace('"', '""') + '"'

    @staticmethod
    def search(q, space=None, project_id=None, tag=None, limit=20):
        if not q or not q.strip():
            return []
        if DocumentSearchService._dialect() == 'sqlite':
            return DocumentSearchService._search_sqlite(q, space, project_id, tag, limit)
        return DocumentSearchService._search_mysql(q, space, project_id, tag, limit)

    @staticmethod
    def _search_sqlite(q, space, project_id, tag, limit):
        rows = db.session.execute(text("""
            SELECT document_id,
                   snippet(document_fts, 2, '<mark>', '</mark>', '…', 16) AS snippet,
                   bm25(document_fts) AS rank
              FROM document_fts WHERE document_fts MATCH :q
              ORDER BY rank LIMIT :lim
        """), {'q': DocumentSearchService._fts5_quote(q), 'lim': limit * 3}).fetchall()
        return DocumentSearchService._materialize(rows, space, project_id, tag, limit)

    @staticmethod
    def _search_mysql(q, space, project_id, tag, limit):
        rows = db.session.execute(text("""
            SELECT id AS document_id,
                   SUBSTRING(search_body, 1, 200) AS snippet,
                   MATCH(search_body, title) AGAINST (:q IN NATURAL LANGUAGE MODE) AS rank
              FROM documents
             WHERE MATCH(search_body, title) AGAINST (:q IN NATURAL LANGUAGE MODE)
             ORDER BY rank DESC LIMIT :lim
        """), {'q': q, 'lim': limit * 3}).fetchall()
        return DocumentSearchService._materialize(rows, space, project_id, tag, limit)

    @staticmethod
    def _materialize(rows, space, project_id, tag, limit):
        ids = [r.document_id for r in rows]
        if not ids:
            return []
        snippets = {r.document_id: r.snippet for r in rows}
        ranks = {r.document_id: r.rank for r in rows}
        q = Document.query.filter(Document.id.in_(ids))
        if space:
            q = q.filter(Document.space_type == space)
        if project_id is not None:
            q = q.filter(Document.project_id == project_id)
        if tag:
            from src.models import Tag, DocumentTag
            q = (q.join(DocumentTag, DocumentTag.document_id == Document.id)
                  .join(Tag, Tag.id == DocumentTag.tag_id)
                  .filter(Tag.name == tag.lower()))
        docs = q.all()
        # Preserve FTS rank order (bm25 returns negative values; lower = better).
        docs.sort(key=lambda d: ranks.get(d.id, 0))
        return [{
            'id': d.id,
            'title': d.title,
            'snippet': snippets.get(d.id, ''),
            'rank': float(ranks.get(d.id, 0)),
            'space_type': d.space_type,
            'project_id': d.project_id,
            'folder_id': d.folder_id,
        } for d in docs[:limit]]
