# expense_tracker/presenter/transaction.py

from sqlalchemy.orm import Session

from datetime import datetime

from enum import Enum

from datetime import datetime

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


class Transaction(Presenter):
    """
    Transaction presenter
    """

    class Column(Enum):
        ID: int = 0
        RECONCILED_STATUS: int = 1
        DESCRIPTION: int = 2
        MERCHANT: int = 3
        DATE: int = 4
        AMOUNT: int = 5
        TAGS: int = 6

    @staticmethod
    def _format(transaction: DB_Transaction) -> tuple[int, ...]:
        """
        Formats raw database transaction into a tuple
        """
        return (
            transaction.id,
            transaction.reconciled_status,
            transaction.description,
            transaction.merchant.name,
            datetime.strftime(transaction.date, Constants.DATE_FORMAT),
            ", ".join(tag.name for tag in transaction.amounts[0].tags),
            # TODO Edit this to support multiple amounts
            transaction.amounts[0].amount,
        )

    @staticmethod
    def get_all() -> list[tuple[int, ...]]:
        """
        Returns a list of all transactions as a list of tuples of strings
        """

        with Session(engine) as session:
            return list(
                Transaction._format(transaction)
                for transaction in session.query(DB_Transaction).all()
            )

    @staticmethod
    def get_by_id(id: int) -> list[tuple[int, ...]]:
        """
        Returns a single object with the requested id
        """
        with Session(engine) as session:
            return Transaction._format(
                session.query(DB_Transaction).where(DB_Transaction.id == id).first()
            )

    @staticmethod
    def set_value(id: int, column: Column, new_value: any) -> any:
        """
        Updates a cell in the database.
        """
        with Session(engine) as session:
            transaction: DB_Transaction = (
                session.query(DB_Transaction).where(DB_Transaction.id == id).first()
            )

            # new_value will be an int representing the id of the new merchant
            if column == Transaction.Column.MERCHANT:
                new_merchant: DB_Merchant = (
                    session.query(DB_Merchant)
                    .where(DB_Merchant.id == new_value)
                    .first()
                )
                transaction.merchant = new_merchant
                session.commit()
                return transaction.merchant.name

            # new_value will be a str
            if column == Transaction.Column.DATE:
                new_date: datetime = datetime.strptime(
                    new_value, Constants.DATE_STRPTIME
                )
                transaction.date = new_date
                session.commit()
                return transaction.date.strftime(Constants.DATE_FORMAT)

            # new_value will be a str
            if column == Transaction.Column.DESCRIPTION:
                transaction.description = new_value
                session.commit()
                return transaction.description

            # new_value will be a str
            # TODO Edit this to support multiple amounts
            if column == Transaction.Column.AMOUNT:
                transaction.amounts[0].amount = float(new_value)
                session.commit()
                return transaction.amounts[0].amount

            # new_value will be a list of ints representing the ids of tags
            # TODO Edit this to support multiple amounts
            if column == Transaction.Column.TAGS:
                transaction.amounts[0].tags = []
                for id in new_value:
                    tag: DB_Tag = session.query(DB_Tag).where(DB_Tag.id == id).first()
                    transaction.amounts[0].tags.append(tag)
                session.commit()
                return ", ".join(tag.name for tag in transaction.amounts[0].tags)

        Presenter.set_value(id, column, new_value)
