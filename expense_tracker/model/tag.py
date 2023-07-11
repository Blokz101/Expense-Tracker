# expense_tracker/model/tag.py

from typing import Optional, List

from expense_tracker.model import Base
from expense_tracker.model.branch_table import Branch_Table

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column


class Tag(Base):
    """
    SQLAlchemy tags table
    
    Stores tags that can be applied to different amounts.
    """

    __tablename__ = "tags"

    # Database columns
    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
    )
    name: Mapped[Optional[str]] = mapped_column(
        unique=True,
        nullable=False,
    )

    # ORM objects
    amounts: Mapped[List["Amount"]] = relationship(
        secondary=Branch_Table.amount_tag,
        back_populates="tags",
    )
    default_merchants: Mapped[List["Merchant"]] = relationship(
        secondary=Branch_Table.merchant_tag_default,
        back_populates="default_tags",
    )
