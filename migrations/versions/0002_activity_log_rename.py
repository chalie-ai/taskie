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
downgrade refuses to run if any non-ticket rows exist (folder/document/etc.
audit entries cannot round-trip into the legacy ticket-only schema). The
operator must export or delete those rows manually before downgrading —
silently destroying audit history is the wrong default.
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
    # Refuse to downgrade if non-ticket audit rows exist — they cannot be
    # represented in the old ticket-only schema and would be silently lost.
    bind = op.get_bind()
    non_ticket = bind.execute(sa.text(
        "SELECT COUNT(*) FROM activity_log WHERE entity_type != 'ticket'"
    )).scalar()
    if non_ticket:
        raise RuntimeError(
            f"Refusing to downgrade: {non_ticket} non-ticket activity_log "
            "rows would be lost. Export or delete them manually first, then "
            "re-run the downgrade."
        )
    with op.batch_alter_table('activity_log') as batch:
        batch.drop_index('ix_activity_log_entity')
        batch.add_column(sa.Column('ticket_id', sa.Integer(), nullable=True))
    op.execute("UPDATE activity_log SET ticket_id=entity_id WHERE entity_type='ticket'")
    with op.batch_alter_table('activity_log') as batch:
        batch.alter_column('ticket_id', nullable=False, existing_type=sa.Integer())
        batch.drop_column('entity_type')
        batch.drop_column('entity_id')
    op.rename_table('activity_log', 'ticket_history')
