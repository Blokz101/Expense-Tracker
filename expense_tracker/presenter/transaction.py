# expense_tracker/presenter/transaction.py

from sqlalchemy.orm import Session

from datetime import datetime

from enum import Enum

from typing import Union

from datetime import datetime

from expense_tracker.constants import Constants

from expense_tracker.presenter.presenter import Presenter
from expense_tracker.presenter.tag import Tag

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
        ACCOUNT: int = 2
        DESCRIPTION: int = 3
        MERCHANT: int = 4
        DATE: int = 5
        TAGS: int = 6
        AMOUNT: int = 7

    @staticmethod
    def _format(transaction: DB_Transaction) -> tuple[str, ...]:
        """
        Formats raw database transaction into a tuple
        """
        return (
            str(transaction.id),
            str(transaction.reconciled_status),
            transaction.account.name,
            transaction.description,
            transaction.merchant.name,
            datetime.strftime(transaction.date, Constants.DATE_FORMAT),
            ", ".join(tag.name for tag in transaction.amounts[0].tags),
            # TODO Edit this to support multiple amounts
            str(transaction.amounts[0].amount),
        )

    @staticmethod
    def get_all() -> list[tuple[str, ...]]:
        """
        Returns a list of all transactions as a list of tuples of strings
        """

        with Session(engine) as session:
            return list(
                Transaction._format(transaction)
                for transaction in session.query(DB_Transaction).all()
            )

    @staticmethod
    def get_by_id(id: int) -> list[tuple[str, ...]]:
        """
        Returns a single object with the requested id
        """
        with Session(engine) as session:
            return Transaction._format(
                session.query(DB_Transaction).where(DB_Transaction.id == id).first()
            )

    @staticmethod
    def create(values: dict[Enum, Union[int, str, datetime]]) -> tuple[str, ...]:
        """
        Create a transaction
        """

        with Session(engine) as session:
            new_transaction: DB_Transaction = DB_Transaction(
                account_id=values[Transaction.Column.ACCOUNT],
                description=values[Transaction.Column.DESCRIPTION],
                merchant_id=values[Transaction.Column.MERCHANT],
                date=values[Transaction.Column.DATE],
                reconciled_status=False,
            )
            session.add(new_transaction)
            session.flush()

            # Add the new amount and its tags
            new_amount: DB_Amount = DB_Amount(
                transaction_id=new_transaction.id,
                amount=float(values[Transaction.Column.AMOUNT]),
            )
            new_amount.tags = Transaction._get_tag_list(values[Transaction.Column.TAGS])
            session.add(new_amount)

            # Commit and return
            session.commit()
            return Transaction._format(new_transaction)

    @staticmethod
    def set_value(id: int, column: Column, new_value: Union[int, str, datetime]) -> str:
        """
        Updates a cell in the database.
        """
        with Session(engine) as session:
            transaction: DB_Transaction = (
                session.query(DB_Transaction).where(DB_Transaction.id == id).first()
            )

            # new_value will be an int representing the id of the new account
            if column == Transaction.Column.ACCOUNT:
                new_account: DB_Account = (
                    session.query(DB_Account).where(DB_Account.id == new_value).first()
                )
                transaction.account = new_account
                session.commit()
                return transaction.account.name

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

            # new_value will be a datetime object
            if column == Transaction.Column.DATE:
                transaction.date = new_value
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

        return Presenter.set_value(id, column, new_value)

    @staticmethod
    def get_value(value: Union[int, str, datetime], column: Column) -> str:
        """
        Format or get a value based on the column it was requested for
        """

        # value will be a str
        if (
            column == Transaction.Column.DESCRIPTION
            or column == Transaction.Column.AMOUNT
        ):
            return str(value)

        # value will be a date time object
        if column == Transaction.Column.DATE:
            return value.strftime(Constants.DATE_FORMAT)

        with Session(engine) as session:
            # value will be an int representing a merchant id
            if column == Transaction.Column.MERCHANT:
                merchant: DB_Merchant = (
                    session.query(DB_Merchant).where(DB_Merchant.id == value).first()
                )
                return merchant.name

            # value will be an int representing an account id
            if column == Transaction.Column.ACCOUNT:
                account: DB_Account = (
                    session.query(DB_Account).where(DB_Account.id == value).first()
                )
                return account.name

            # value will be a list of ints
            # TODO Edit this to support multiple amounts
            if column == Transaction.Column.TAGS:
                return ", ".join(tag.name for tag in Tag.get_tag_list(value))

        return Presenter.get_value(id, column)
