# expense_tracker/orm/transaction.py

from datetime import datetime

from typing import List

from expense_tracker.orm import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column


class Transaction(Base):
    """
    SQLAlchemy transactions table
    """

    __tablename__ = "transactions"

    # Database columns
    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
    )
    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id"),
        nullable=False,
    )
    transfer_account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id"),
        unique=True,
        nullable=True,
    )
    description: Mapped[str] = mapped_column(
        unique=True,
        nullable=True,
    )
    merchant_id: Mapped[int] = mapped_column(
        ForeignKey("merchants.id"),
        nullable=False,
    )
    date: Mapped[datetime] = mapped_column(
        nullable=False,
    )
    reconciled_status: Mapped[bool] = mapped_column(
        nullable=False,
    )
    statement_name: Mapped[str] = mapped_column(
        unique=True,
        nullable=True,
    )
    receipt_photo_path: Mapped[str] = mapped_column(
        unique=True,
        nullable=True,
    )
    x_coord: Mapped[float] = mapped_column(
        nullable=True,
    )
    y_coord: Mapped[float] = mapped_column(
        nullable=True,
    )

    # ORM objects
    merchant: Mapped["Merchant"] = relationship(
        back_populates="transactions",
    )
    amounts: Mapped[List["Amount"]] = relationship(
        back_populates="transaction",
    )
    account: Mapped["Account"] = relationship(
        back_populates="transactions",
        foreign_keys=[account_id],
    )
    transfer_account: Mapped["Account"] = relationship(
        back_populates="transfer_transactions",
        foreign_keys=[transfer_account_id],
    )
