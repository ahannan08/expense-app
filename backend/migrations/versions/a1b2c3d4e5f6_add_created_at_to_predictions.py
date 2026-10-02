"""add created_at to predictions

Revision ID: a1b2c3d4e5f6
Revises: 6a990b948262
Create Date: 2026-03-20 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "a1b2c3d4e5f6"
down_revision = "6a990b948262"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("predictions", schema=None) as batch_op:
        batch_op.add_column(sa.Column("created_at", sa.DateTime(), nullable=True))


def downgrade():
    with op.batch_alter_table("predictions", schema=None) as batch_op:
        batch_op.drop_column("created_at")
