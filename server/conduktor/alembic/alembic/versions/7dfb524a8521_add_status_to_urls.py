"""Add status to URLs

Revision ID: 7dfb524a8521
Revises: 7f42b2cc9624
Create Date: 2018-07-19 03:17:21.398541

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7dfb524a8521'
down_revision = '7f42b2cc9624'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('urls', sa.Column('active', sa.Boolean, nullable=False, server_default=sa.true()))


def downgrade():
    op.drop_column('urls', 'active')
