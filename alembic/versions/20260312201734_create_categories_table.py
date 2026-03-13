"""create_categories_table

Revision ID: 7fe9ffb2b7dc
Revises: 
Create Date: 2026-03-12 20:17:34.508907

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7fe9ffb2b7dc'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("categories")
