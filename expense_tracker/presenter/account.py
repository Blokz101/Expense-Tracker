# expense_tracker/presenter/account.py

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


class Account(Presenter):
    """
    Account presenter
    """

    class Column(Enum):
        ID: int = 0
        NAME: int = 1
        NAMING_RULE: int = 2
        DESCRIPTION_COLUMN_INDEX: int = 3
        AMOUNT_COLUMN_INDEX: int = 4
        DATE_COLUMN_INDEX: int = 5

    @staticmethod
    def _format(amount_list: list[DB_Account]) -> list[tuple[int, ...]]:
        """
        Formats raw database transaction into a tuple
        """
        display_list: list[tuple[int, ...]] = []

        for entry in amount_list:
            display_list.append(
                (
                    entry.id,
                    entry.name,
                    str(entry.statement_description_column_index),
                    str(entry.statement_amount_column_index),
                    str(entry.statement_date_column_index),
                )
            )

        return display_list

    @staticmethod
    def get_all() -> list[tuple[int, ...]]:
        """
        Returns a list of all merchants as a list of tuples of strings
        """
        with Session(engine) as session:
            return Account._format(session.query(DB_Account).all())

    @staticmethod
    def set_value(id: int, column: Column, new_value: any) -> any:
        """
        Updates cell in the database
        """
        with Session(engine) as session:
            account: DB_Account = (
                session.query(DB_Account).where(DB_Account.id == id).first()
            )

            # new_value will be an str
            if column == Account.Column.NAME:
                account.name = new_value
                session.commit()
                return account.name

            # new_value will be an str
            if column == Account.Column.DESCRIPTION_COLUMN_INDEX:
                account.statement_description_column_index = int(new_value)
                session.commit()
                return account.statement_description_column_index

            # new_value will be an str
            if column == Account.Column.AMOUNT_COLUMN_INDEX:
                account.statement_amount_column_index = int(new_value)
                session.commit()
                return account.statement_amount_column_index

            # new_value will be an str
            if column == Account.Column.DATE_COLUMN_INDEX:
                account.statement_date_column_index = int(new_value)
                session.commit()
                return account.statement_date_column_index

        Presenter.set_value(id, column, new_value)
