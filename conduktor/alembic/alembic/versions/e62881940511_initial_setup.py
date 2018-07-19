"""Initial setup

Revision ID: e62881940511
Revises: 
Create Date: 2018-07-19 01:15:44.917713

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e62881940511'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'urls',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('slug', sa.String(), nullable=False, index=True, unique=True),
        sa.Column('redirect', sa.String(length=4096), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'url_log',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('url_id', sa.Integer(), nullable=True),
        sa.Column('date_created', sa.DateTime(), nullable=True),
        sa.Column('log_info', sa.String(length=4096), nullable=False),
        sa.ForeignKeyConstraint(['url_id'], ['urls.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_url_log_url_id_date_created', 'url_id', 'date_created')
    )

    op.create_table(
        'url_stats',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('url_id', sa.Integer(), nullable=True),
        sa.Column('date_created', sa.DateTime(), nullable=True),
        sa.Column('count', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['url_id'], ['urls.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_url_stats_url_id_date_created', 'url_id', 'date_created')
    )


def downgrade():
    op.drop_table('url_stats')
    op.drop_table('url_log')
    op.drop_table('urls')
