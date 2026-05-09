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


def downgrade():
    op.drop_table('documents')
    op.drop_table('document_versions')
    op.drop_table('folders')
