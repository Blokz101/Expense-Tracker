# expense_tracker/orm/db_merchant.py

from typing import Optional, List

from expense_tracker.orm import Base
from expense_tracker.orm.branch_table import Branch_Table

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column


class DB_Merchant(Base):
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
    name: Mapped[str] = mapped_column(
        unique=True,
        nullable=False,
    )
    naming_rule: Mapped[Optional[str]] = mapped_column(
        unique=False,
        nullable=True,
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
