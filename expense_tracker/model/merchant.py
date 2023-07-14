# expense_tracker/model/merchant.py

from typing import Optional, List

from expense_tracker.model import Base
from expense_tracker.model.branch_table import Branch_Table

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column


class Merchant(Base):
    """
    SQLAlchemy merchants table

    Stores merchants that can be assigned to transactions
    """

    __tablename__ = "merchants"

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
    transactions: Mapped[List["Transaction"]] = relationship(
        back_populates="merchant",
    )
    merchant_locations: Mapped[List["Merchant_Location"]] = relationship(
        back_populates="merchant",
    )
    default_tags: Mapped[List["Tag"]] = relationship(
        secondary=Branch_Table.merchant_tag_default,
        back_populates="default_merchants",
    )
