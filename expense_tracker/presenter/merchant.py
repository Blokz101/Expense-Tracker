# expense_tracker/presenter/merchant.py

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


class Merchant(Presenter):
    """
    Merchant presenter
    """

    class Column(Enum):
        ID: int = 0
        NAME: int = 1
        NAMING_RULE: int = 2
        DEFAULT_TAGS: int = 3

    @staticmethod
    def _format(merchant_list: list[DB_Merchant]) -> list[tuple[int, ...]]:
        """
        Formats raw database transaction into a tuple
        """
        display_list: list[tuple[int, ...]] = []

        for entry in merchant_list:
            display_list.append(
                (
                    entry.id,
                    entry.name,
                    entry.naming_rule,
                )
            )

        return display_list

    @staticmethod
    def get_all() -> list[tuple[int, ...]]:
        """
        Returns a list of all merchants as a list of tuples of strings
        """
        with Session(engine) as session:
            return Merchant._format(session.query(DB_Merchant).all())

    @staticmethod
    def set_value(id: int, column: Column, new_value: any) -> any:
        """
        Updates cell in the database
        """
        with Session(engine) as session:
            merchant: DB_Merchant = (
                session.query(DB_Merchant).where(DB_Merchant.id == id).first()
            )

            # new_value will be an str
            if column == Merchant.Column.NAME or column == Merchant.Column.NAMING_RULE:
                merchant.name = new_value
                session.commit()
                return merchant.name

        Presenter.set_value(id, column, new_value)
