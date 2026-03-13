"""add_slug_to_categories

Revision ID: 3fad6b5de166
Revises: 6e6420c27780
Create Date: 2026-03-12 21:50:47.888077

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3fad6b5de166'
down_revision: Union[str, Sequence[str], None] = '6e6420c27780'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("categories", sa.Column("slug", sa.String(150), nullable=True))
    op.create_unique_constraint("uq_categories_slug", "categories", ["slug"])
    op.create_index("ix_categories_slug", "categories", ["slug"])


def downgrade() -> None:
    op.drop_index("ix_categories_slug", table_name="categories")
    op.drop_constraint("uq_categories_slug", "categories", type_="unique")
    op.drop_column("categories", "slug")
