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
        DESCRIPTION_COLUMN_INDEX: int = 2
        AMOUNT_COLUMN_INDEX: int = 3
        DATE_COLUMN_INDEX: int = 4

    @staticmethod
    def _format(amount: DB_Account) -> tuple[int, ...]:
        """
        Formats raw database transaction into a tuple
        """
        return (
            amount.id,
            amount.name,
            str(amount.statement_description_column_index),
            str(amount.statement_amount_column_index),
            str(amount.statement_date_column_index),
        )

    @staticmethod
    def get_all() -> list[tuple[int, ...]]:
        """
        Returns a list of all merchants as a list of tuples of strings
        """
        with Session(engine) as session:
            return list(
                Account._format(account) for account in session.query(DB_Account).all()
            )
            
    @staticmethod
    def create(values: dict[Enum, any]) -> tuple[int, ...]:
        """
        Create a merchant
        """
        with Session(engine) as session:
            new_account: DB_Account = DB_Account(
                name=values[Account.Column.NAME],
                statement_description_column_index=values[Account.Column.DESCRIPTION_COLUMN_INDEX],
                statement_amount_column_index=values[Account.Column.AMOUNT_COLUMN_INDEX],
                statement_date_column_index=values[Account.Column.DATE_COLUMN_INDEX]
            )
            session.add(new_account)
            session.commit()
            return Account._format(new_account)

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
        
    @staticmethod
    def get_value(value: any, column: Column) -> any:
        """
        Format or get a value based on the column it was requested for
        """

        # value will be a str
        if (
            column == Account.Column.NAME
            or column == Account.Column.DESCRIPTION_COLUMN_INDEX
            or column == Account.Column.AMOUNT_COLUMN_INDEX
            or column == Account.Column.DATE_COLUMN_INDEX
        ):
            return str(value)

        return Presenter.get_value(id, column)
