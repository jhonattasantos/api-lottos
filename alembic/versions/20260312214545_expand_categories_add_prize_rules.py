"""expand_categories_add_prize_rules

Revision ID: 6e6420c27780
Revises: 7fe9ffb2b7dc
Create Date: 2026-03-12 21:45:45.588129

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e6420c27780'
down_revision: Union[str, Sequence[str], None] = '7fe9ffb2b7dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("categories", sa.Column("min_number", sa.Integer(), nullable=False, server_default="1"))
    op.add_column("categories", sa.Column("max_number", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("categories", sa.Column("picks", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("categories", sa.Column("draws", sa.Integer(), nullable=False, server_default="0"))

    op.alter_column("categories", "min_number", server_default=None)
    op.alter_column("categories", "max_number", server_default=None)
    op.alter_column("categories", "picks", server_default=None)
    op.alter_column("categories", "draws", server_default=None)

    op.create_table(
        "prize_rules",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("category_id", sa.Integer(), sa.ForeignKey("categories.id", ondelete="CASCADE"), nullable=False),
        sa.Column("label", sa.String(50), nullable=False),
        sa.Column("hits", sa.Integer(), nullable=False),
    )
    op.create_index("ix_prize_rules_category_id", "prize_rules", ["category_id"])


def downgrade() -> None:
    op.drop_index("ix_prize_rules_category_id", table_name="prize_rules")
    op.drop_table("prize_rules")
    op.drop_column("categories", "draws")
    op.drop_column("categories", "picks")
    op.drop_column("categories", "max_number")
    op.drop_column("categories", "min_number")
