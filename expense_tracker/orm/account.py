# expense_tracker/orm/account.py

from typing import Optional, List

from expense_tracker.orm import Base
from expense_tracker.orm.branch_table import Branch_Table

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column


class Account(Base):
    """
    SQLAlchemy accounts table

    Stores accounts that can be assigned to a transaction.
    """

    __tablename__ = "accounts"

    # Database columns
    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        unique=True,
        nullable=False,
    )
    statement_description_column_index: Mapped[Optional[int]] = mapped_column(
        nullable=False,
    )
    statement_amount_column_index: Mapped[Optional[int]] = mapped_column(
        nullable=False,
    )
    statement_date_column_index: Mapped[Optional[int]] = mapped_column(
        nullable=False,
    )

    # ORM objects
    transactions: Mapped[List["Transaction"]] = relationship(
        back_populates="account",
        foreign_keys="Transaction.account_id",
    )
    transfer_transactions: Mapped[List["Transaction"]] = relationship(
        foreign_keys="Transaction.transfer_account_id",
        back_populates="transfer_account",
    )
    budgets: Mapped[List["Budget"]] = relationship(
        secondary=Branch_Table.budget_account,
        back_populates="accounts",
    )
