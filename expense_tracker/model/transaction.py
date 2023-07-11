# expense_tracker/model/transaction.py

from datetime import datetime

from typing import Optional, List

from expense_tracker.model import Base
from expense_tracker.model.branch_table import Branch_Table

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column


class Transaction(Base):
    """ """

    __tablename__ = "transactions"

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
    amount: Mapped[float] = mapped_column(
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

    merchant: Mapped["Merchant"] = relationship(
        back_populates="transactions",
    )
    tags: Mapped[List["Tag"]] = relationship(
        secondary=Branch_Table.transaction_tag,
        back_populates="transactions",
    )
    # transaction_tag_branches: Mapped[List["Transaction_Tag_Branch"]] = relationship(
    #     back_populates="transaction",
    # )
    account: Mapped["Account"] = relationship(
        back_populates="transactions",
        foreign_keys=[account_id],
    )
    transfer_account: Mapped["Account"] = relationship(
        back_populates="transfer_transactions",
        foreign_keys=[transfer_account_id],
    )
