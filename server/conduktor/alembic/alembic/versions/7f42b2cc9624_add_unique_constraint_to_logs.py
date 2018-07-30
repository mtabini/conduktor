"""Add unique constraint to logs

Revision ID: 7f42b2cc9624
Revises: e62881940511
Create Date: 2018-07-19 02:52:36.725379

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f42b2cc9624'
down_revision = 'e62881940511'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_index('ix_url_stats_url_id_date_created', table_name='url_stats')
    op.create_index('ix_url_stats_url_id_date_created', 'url_stats', ['url_id', 'date_created'], unique=True)


def downgrade():
    op.drop_index('ix_url_stats_url_id_date_created', table_name='url_stats')
    op.create_index('ix_url_stats_url_id_date_created', 'url_stats', ['url_id', 'date_created'], unique=False)
