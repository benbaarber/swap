"""Init database

Revision ID: 8752199ef05a
Revises: 
Create Date: 2022-05-14 15:59:27.276732

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision = "8752199ef05a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "swap_user",
        sa.Column("username", sa.Text, primary_key=True),
        sa.Column("balance", sa.Float, nullable=False),
        sa.Column("swap_metadata", JSONB, nullable=True),
    )

    op.create_table(
        "investment",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("username", sa.Text, nullable=False),
        sa.Column("coin", sa.String, nullable=False),
        sa.Column("amount", sa.Float, nullable=False),
        sa.Column("date", sa.DateTime, nullable=False),
    )


def downgrade():
    pass
