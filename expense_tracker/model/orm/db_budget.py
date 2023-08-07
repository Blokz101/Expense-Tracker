# expense_tracker/orm/db_budget.py

from typing import Optional, List

from expense_tracker.model.orm import Base
from expense_tracker.model.orm.branch_table import Branch_Table

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column


class DB_Budget(Base):
    """
    SQLAlchemy budgets table

    Stores budgets that can be applied to different amounts.
    """

    __tablename__ = "budgets"

    # Database columns
    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        unique=True,
        nullable=False,
    )
    default_monthly_goal: Mapped[Optional[float]] = mapped_column(
        nullable=True,
    )
    default_start_day: Mapped[Optional[int]] = mapped_column(
        nullable=True,
    )

    # ORM objects
    month_budgets: Mapped[List["Month_Budget"]] = relationship(
        back_populates="budget",
    )
    accounts: Mapped[List["Account"]] = relationship(
        secondary=Branch_Table.budget_account,
        back_populates="budgets",
    )
    tags: Mapped[List["Tag"]] = relationship(
        secondary=Branch_Table.budget_tag,
        back_populates="budgets",
    )
