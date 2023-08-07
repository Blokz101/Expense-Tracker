# expense_tracker/orm/db_monthly_budget.py

from typing import Optional, List

from expense_tracker.model.orm import Base
from expense_tracker.model.orm.branch_table import Branch_Table

from datetime import datetime

from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column


class DB_Month_Budget(Base):
    """
    SQLAlchemy budgets table

    Stores budgets that can be applied to different amounts.
    """

    __tablename__ = "month_budgets"

    # Database columns
    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
    )
    budget_id: Mapped[int] = mapped_column(
        ForeignKey("budgets.id"),
        nullable=False,
    )
    goal: Mapped[float] = mapped_column(
        nullable=False,
    )
    start_date: Mapped[datetime] = mapped_column(
        nullable=False,
    )

    # ORM objects
    budget: Mapped["Budget"] = relationship(
        back_populates="month_budgets",
    )
