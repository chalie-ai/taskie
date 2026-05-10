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
        body = (cv.body_md if cv else '') or ''
        tags = ' '.join(TagService.list_for_document(doc_id))
        if DocumentSearchService._dialect() == 'sqlite':
            # DELETE+INSERT pattern. SQLite serialises writers (single-writer model),
            # so two concurrent reindex_document() calls for the same doc cannot
            # interleave their DELETE/INSERT pairs. On MySQL the path is a single
            # UPDATE on documents.search_body (no DELETE+INSERT, no race surface).
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
        """Remove a document from the FTS index.

        On SQLite this issues an explicit DELETE on document_fts.
        On MySQL this is a no-op: search_body lives on the documents row,
        so deleting the row removes the index entry transitively. Callers
        that want to forcibly clear search_body without deleting the row
        must do so themselves.

        MUST be called AFTER the caller's db.session.commit() — this method
        issues its own commit.
        """
        if DocumentSearchService._dialect() == 'sqlite':
            db.session.execute(
                text("DELETE FROM document_fts WHERE document_id = :id"),
                {'id': doc_id},
            )
            db.session.commit()

    @staticmethod
    def _fts5_quote(q):
        """Quote each whitespace-separated token in `q` as an FTS5 phrase so
        that hyphens and other operator-like characters are treated literally,
        while still allowing multi-word AND-style matching across tokens.

        Without per-token quoting, FTS5 parses `full-text` as `full NOT text`
        and `python flask` as a single exact phrase. Per-token quoting fixes
        both: `"full-text"` and `"python" "flask"` (implicit AND).
        """
        tokens = (q or '').split()
        return ' '.join('"' + t.replace('"', '""') + '"' for t in tokens)

    @staticmethod
    def search(q, space=None, project_id=None, tag=None, limit=20):
        limit = min(max(1, limit or 20), 100)
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
        # MySQL: innodb_ft_min_token_size defaults to 3 — queries shorter than
        # that silently return [] with no error. Set innodb_ft_min_token_size=1
        # in my.cnf and rebuild the FULLTEXT index for short-term/acronym support.
        rows = db.session.execute(text("""
            SELECT id AS document_id,
                   SUBSTRING(search_body, 1, 200) AS snippet,
                   -MATCH(search_body, title) AGAINST (:q IN NATURAL LANGUAGE MODE) AS rank
              FROM documents
             WHERE MATCH(search_body, title) AGAINST (:q IN NATURAL LANGUAGE MODE)
             ORDER BY rank LIMIT :lim
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
