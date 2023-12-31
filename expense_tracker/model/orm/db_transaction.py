# expense_tracker/orm/db_transaction.py

from datetime import datetime

from typing import List

from expense_tracker.model.orm import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column


class DB_Transaction(Base):
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
        unique=False,
        nullable=False,
    )
    merchant_id: Mapped[int] = mapped_column(
        ForeignKey("merchants.id"),
        nullable=False,
    )
    merchant_location_id: Mapped[int] = mapped_column(
        ForeignKey("merchant_locations.id"),
        nullable=True,
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

    # ORM objects
    merchant: Mapped["DB_Merchant"] = relationship(
        back_populates="transactions",
    )
    amounts: Mapped[List["DB_Amount"]] = relationship(
        back_populates="transaction",
        cascade="all, delete-orphan",
    )
    account: Mapped["DB_Account"] = relationship(
        back_populates="transactions",
        foreign_keys=[account_id],
    )
    transfer_account: Mapped["DB_Account"] = relationship(
        back_populates="transfer_transactions",
        foreign_keys=[transfer_account_id],
    )
