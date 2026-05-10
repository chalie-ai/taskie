"""docs_init: folders table (Tasks 5-8 will extend this migration with
documents, document_versions, tags, document_tags, and document_links).

Revision ID: 0003_docs_init
Revises: 0002_activity_log_rename
Create Date: 2026-05-09
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0003_docs_init'
down_revision = '0002_activity_log_rename'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'folders',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('parent_folder_id', sa.Integer(), nullable=True),
        sa.Column('space_type', sa.String(length=10), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=True),
        sa.Column('sort_order', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('updated_by', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id']),
        sa.ForeignKeyConstraint(['parent_folder_id'], ['folders.id']),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id']),
        sa.ForeignKeyConstraint(['updated_by'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('parent_folder_id', 'name', 'space_type', 'project_id',
                            name='uq_folder_sibling'),
        sa.CheckConstraint(
            "(space_type = 'project' AND project_id IS NOT NULL) OR "
            "(space_type = 'global' AND project_id IS NULL)",
            name='ck_folder_space_consistency',
        ),
    )

    # document_versions is created first. The document_id FK back to 'documents'
    # cannot be declared inline because 'documents' doesn't exist yet; SQLite
    # silently accepts forward-reference FK declarations in CREATE TABLE, so we
    # include it here. On databases that strictly validate FK declarations at
    # DDL time, use_alter=True on the ORM model handles the bootstrapping order.
    op.create_table(
        'document_versions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('document_id', sa.Integer(), nullable=False),
        sa.Column('version_number', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=300), nullable=False),
        sa.Column('body_md', sa.Text(), nullable=True),
        sa.Column('change_note', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id']),
        sa.ForeignKeyConstraint(['document_id'], ['documents.id'],
                                name='fk_document_versions_document_id',
                                ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('document_id', 'version_number',
                            name='uq_document_version_number'),
    )

    op.create_table(
        'documents',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('slug', sa.String(length=300), nullable=True),
        sa.Column('space_type', sa.String(length=10), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=True),
        sa.Column('folder_id', sa.Integer(), nullable=True),
        sa.Column('current_version_id', sa.Integer(), nullable=True),
        sa.Column('sort_order', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('updated_by', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id']),
        sa.ForeignKeyConstraint(['current_version_id'], ['document_versions.id'],
                                name='fk_documents_current_version'),
        sa.ForeignKeyConstraint(['folder_id'], ['folders.id']),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id']),
        sa.ForeignKeyConstraint(['updated_by'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('folder_id', 'slug', 'space_type', 'project_id',
                            name='uq_document_slug'),
        sa.CheckConstraint(
            "(space_type = 'project' AND project_id IS NOT NULL) OR "
            "(space_type = 'global' AND project_id IS NULL)",
            name='ck_document_space_consistency',
        ),
    )


    op.create_table(
        'tags',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )

    op.create_table(
        'document_tags',
        sa.Column('document_id', sa.Integer(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['document_id'], ['documents.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('document_id', 'tag_id'),
    )
    # Index supports `Document.list(tag=...)` joining on tag_id.
    # The composite PK only accelerates lookups starting with document_id.
    op.create_index('ix_document_tags_tag_id', 'document_tags', ['tag_id'])

    op.create_table(
        'document_ticket_links',
        sa.Column('document_id', sa.Integer(), nullable=False),
        sa.Column('ticket_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id']),
        sa.ForeignKeyConstraint(['document_id'], ['documents.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['ticket_id'], ['tickets.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('document_id', 'ticket_id'),
    )
    op.create_index('ix_document_ticket_links_ticket_id',
                    'document_ticket_links', ['ticket_id'])

    with op.batch_alter_table('attachments') as batch:
        batch.alter_column('ticket_id', nullable=True)
        batch.add_column(sa.Column('document_id', sa.Integer(), nullable=True))
        batch.create_foreign_key('fk_attachments_document', 'documents',
                                 ['document_id'], ['id'], ondelete='CASCADE')
        batch.create_check_constraint(
            'ck_attachment_one_parent',
            '(ticket_id IS NOT NULL AND document_id IS NULL) OR '
            '(ticket_id IS NULL AND document_id IS NOT NULL)',
        )
    op.create_index('ix_attachments_document_id', 'attachments', ['document_id'])

    # search_body is added to documents on all dialects so the ORM model maps
    # cleanly without dialect-conditional column presence. On SQLite it is
    # always NULL (the SQLite FTS path writes document_fts, not this column).
    # On MySQL it holds the denormalised title+body+tags text and carries the
    # combined FULLTEXT index.
    op.add_column('documents', sa.Column('search_body', sa.Text(), nullable=True))

    # FTS5 / FULLTEXT search index — dialect-aware, placed after all tables
    # exist because the virtual table conceptually depends on 'documents'.
    bind = op.get_bind()
    if bind.dialect.name == 'sqlite':
        op.execute("""
            CREATE VIRTUAL TABLE document_fts USING fts5(
                document_id UNINDEXED, title, body, tags,
                tokenize = 'porter unicode61'
            )
        """)
    elif bind.dialect.name == 'mysql':
        op.create_index('ft_documents_search', 'documents', ['search_body', 'title'],
                        mysql_prefix='FULLTEXT')


def downgrade():
    # Drop FTS / FULLTEXT objects FIRST (before documents is dropped).
    bind = op.get_bind()
    if bind.dialect.name == 'sqlite':
        op.execute("DROP TABLE IF EXISTS document_fts")
    elif bind.dialect.name == 'mysql':
        op.drop_index('ft_documents_search', table_name='documents')
    # search_body is present on all dialects — drop unconditionally.
    with op.batch_alter_table('documents') as batch:
        batch.drop_column('search_body')

    # Undo the attachments polymorphic extension NEXT because the FK references
    # documents.id — the documents table must still exist when we drop the FK.
    op.drop_index('ix_attachments_document_id', table_name='attachments', if_exists=True)
    with op.batch_alter_table('attachments') as batch:
        batch.drop_constraint('ck_attachment_one_parent', type_='check')
        batch.drop_constraint('fk_attachments_document', type_='foreignkey')
        batch.drop_column('document_id')
        batch.alter_column('ticket_id', nullable=False)

    # if_exists guards make this revision safe to downgrade on environments
    # that were stamped at 0003 before later tasks extended this migration
    # (this revision grows across Tasks 4–8). Without these, a downgrade
    # crashes on the first table that wasn't yet present when the dev
    # originally ran upgrade.
    op.drop_index('ix_document_ticket_links_ticket_id',
                  table_name='document_ticket_links', if_exists=True)
    op.drop_table('document_ticket_links', if_exists=True)
    op.drop_index('ix_document_tags_tag_id', table_name='document_tags', if_exists=True)
    op.drop_table('document_tags', if_exists=True)
    op.drop_table('tags', if_exists=True)
    op.drop_table('documents', if_exists=True)
    op.drop_table('document_versions', if_exists=True)
    op.drop_table('folders', if_exists=True)
