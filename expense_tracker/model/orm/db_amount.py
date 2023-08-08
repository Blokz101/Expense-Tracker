# expense_tracker/orm/db_amount.py

from typing import List

from expense_tracker.model.orm import Base
from expense_tracker.model.orm.branch_table import Branch_Table

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column


class DB_Amount(Base):
    """
    SQLAlchemy amounts table

    Stores amounts, allows a transaction to be split into different amounts and each amount tagged with its own tags.
    """

    __tablename__ = "amounts"

    # Database columns
    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        unique=True,
        nullable=True,
    )
    transaction_id: Mapped[int] = mapped_column(
        ForeignKey("transactions.id"),
        nullable=False,
    )
    amount: Mapped[float] = mapped_column(
        nullable=False,
    )

    # ORM objects
    transaction: Mapped["DB_Transaction"] = relationship(
        back_populates="amounts",
    )
    tags: Mapped[List["DB_Tag"]] = relationship(
        secondary=Branch_Table.amount_tag,
        back_populates="amounts",
    )
