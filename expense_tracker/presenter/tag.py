# expense_tracker/presenter/tag.py

from sqlalchemy.orm import Session

from datetime import datetime

from enum import Enum

from expense_tracker.constants import Constants

from expense_tracker.presenter.presenter import Presenter

from expense_tracker.model.orm import engine
from expense_tracker.model.orm.db_transaction import DB_Transaction
from expense_tracker.model.orm.db_merchant import DB_Merchant
from expense_tracker.model.orm.db_amount import DB_Amount
from expense_tracker.model.orm.db_account import DB_Account
from expense_tracker.model.orm.db_merchant_location import DB_Merchant_Location
from expense_tracker.model.orm.db_tag import DB_Tag
from expense_tracker.model.orm.db_budget import DB_Budget
from expense_tracker.model.orm.db_month_budget import DB_Month_Budget


class Tag(Presenter):
    """
    Merchant presenter
    """

    class Column(Enum):
        ID: int = 0
        NAME: int = 1
        INSTANCE_TAG: int = 2

    @staticmethod
    def _format(tag_list: list[DB_Tag]) -> list[tuple[int, ...]]:
        """
        Formats raw database tags into a tuple
        """

        display_list: list[tuple[int, ...]] = []

        for entry in tag_list:
            display_list.append(
                (
                    entry.id,
                    entry.name,
                    entry.instance_tag,
                )
            )

        return display_list

    @staticmethod
    def get_all() -> list[tuple[int, ...]]:
        """
        Returns a list of all merchants as a list of tuples of strings
        """

        with Session(engine) as session:
            return Tag._format(session.query(DB_Tag).all())

    # TODO Edit this entire method to work with multiple amounts
    @staticmethod
    def get_tags_from_transaction(id: int) -> list[tuple[int, str]]:
        """
        Gets the tags from the first amount that a transaction has
        """

        with Session(engine) as session:
            transaction: DB_Transaction = (
                session.query(DB_Transaction).where(DB_Transaction.id == id).first()
            )
            amount: DB_Amount = (
                session.query(DB_Amount).where(DB_Amount.id == transaction.id).first()
            )
            tag_list: list[DB_Tag] = (
                session.query(DB_Tag).where(DB_Tag.amounts.contains(amount)).all()
            )

            return Tag._format(tag_list)
