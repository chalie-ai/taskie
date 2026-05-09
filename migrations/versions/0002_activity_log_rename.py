"""rename ticket_history to activity_log polymorphic

Revision ID: 0002_activity_log_rename
Revises: 0001_baseline
Create Date: 2026-05-09

Renames the ticket-only ``ticket_history`` table to a polymorphic
``activity_log`` keyed by ``entity_type`` + ``entity_id`` so the docs section
(folders, documents, doc-versions, etc.) can share one audit log.

batch_alter_table is required because SQLite cannot DROP COLUMN in place;
alembic emulates it by rebuilding the table.

The upgrade backfills existing rows with ``entity_type='ticket'`` and
``entity_id=ticket_id`` before dropping the legacy ``ticket_id`` column. The
downgrade reverses the mapping for entity_type='ticket' rows; non-ticket
rows (post-rename) cannot be represented in the old schema and would be
lost — acceptable for a one-way refactor.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0002_activity_log_rename'
down_revision = '0001_baseline'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('ticket_history', 'activity_log')
    with op.batch_alter_table('activity_log') as batch:
        batch.add_column(sa.Column('entity_type', sa.String(length=20), nullable=True))
        batch.add_column(sa.Column('entity_id', sa.Integer(), nullable=True))
    op.execute("UPDATE activity_log SET entity_type='ticket', entity_id=ticket_id")
    with op.batch_alter_table('activity_log') as batch:
        batch.alter_column('entity_type', nullable=False, existing_type=sa.String(length=20))
        batch.alter_column('entity_id', nullable=False, existing_type=sa.Integer())
        batch.drop_column('ticket_id')
        batch.create_index('ix_activity_log_entity', ['entity_type', 'entity_id'])


def downgrade():
    with op.batch_alter_table('activity_log') as batch:
        batch.drop_index('ix_activity_log_entity')
        batch.add_column(sa.Column('ticket_id', sa.Integer(), nullable=True))
    op.execute("UPDATE activity_log SET ticket_id=entity_id WHERE entity_type='ticket'")
    # Drop rows that can't round-trip back to the ticket-only schema before
    # we tighten ticket_id to NOT NULL. Without this, batch rebuild would
    # fail when copying NULLs into a NOT NULL column.
    op.execute("DELETE FROM activity_log WHERE ticket_id IS NULL")
    with op.batch_alter_table('activity_log') as batch:
        batch.alter_column('ticket_id', nullable=False, existing_type=sa.Integer())
        batch.drop_column('entity_type')
        batch.drop_column('entity_id')
    op.rename_table('activity_log', 'ticket_history')
