# expense_tracker/presenter/merchant.py

from sqlalchemy.orm import Session

from enum import Enum

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
    def _format(merchant: DB_Merchant) -> tuple[int, ...]:
        """
        Formats raw database transaction into a tuple
        """
        return (
            merchant.id,
            merchant.name,
            merchant.naming_rule,
        )

    @staticmethod
    def get_all() -> list[tuple[int, ...]]:
        """
        Returns a list of all merchants as a list of tuples of strings
        """
        with Session(engine) as session:
            return list(
                Merchant._format(merchant)
                for merchant in session.query(DB_Merchant).all()
            )

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
            if column == Merchant.Column.NAME:
                merchant.name = new_value
                session.commit()
                return merchant.name

            # new_value will be an str
            if column == Merchant.Column.NAMING_RULE:
                merchant.naming_rule = new_value
                session.commit()
                return merchant.naming_rule

        Presenter.set_value(id, column, new_value)
