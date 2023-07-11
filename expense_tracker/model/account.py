# expense_tracker/model/account.py

from typing import Optional, List

from expense_tracker.model import Base

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column


class Account(Base):
    """ """

    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
    )
    name: Mapped[Optional[str]] = mapped_column(
        unique=True,
        nullable=False,
    )

    transactions: Mapped[List["Transaction"]] = relationship(
        foreign_keys="Transaction.account_id",
        back_populates="account",
    )
    transfer_transactions: Mapped[List["Transaction"]] = relationship(
        foreign_keys="Transaction.transfer_account_id",
        back_populates="transfer_account",
    )
