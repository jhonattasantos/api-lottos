from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class PrizeRule(Base):
    __tablename__ = "prize_rules"

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"), nullable=False, index=True
    )
    label: Mapped[str] = mapped_column(String(50), nullable=False)
    hits: Mapped[int] = mapped_column(nullable=False)

    category: Mapped["Category"] = relationship(back_populates="prize_rules")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(150), nullable=False, unique=True, index=True)
    min_number: Mapped[int] = mapped_column(nullable=False)
    max_number: Mapped[int] = mapped_column(nullable=False)
    picks: Mapped[int] = mapped_column(nullable=False)
    draws: Mapped[int] = mapped_column(nullable=False)

    prize_rules: Mapped[list["PrizeRule"]] = relationship(
        back_populates="category",
        cascade="all, delete-orphan",
        order_by="PrizeRule.hits.desc()",
        lazy="noload",
    )
