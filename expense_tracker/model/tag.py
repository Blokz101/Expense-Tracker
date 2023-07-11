# expense_tracker/model/tag.py

from typing import Optional, List

from expense_tracker.model import Base
from expense_tracker.model.branch_table import Branch_Table

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column


class Tag(Base):
    """ """

    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
    )
    name: Mapped[Optional[str]] = mapped_column(
        unique=True,
        nullable=False,
    )

    transactions: Mapped[List["Transaction"]] = relationship(
        secondary=Branch_Table.transaction_tag,
        back_populates="tags",
    )
    default_merchants: Mapped[List["Merchant"]] = relationship(
        secondary=Branch_Table.merchant_tag_default,
        back_populates="default_tags",
    )
