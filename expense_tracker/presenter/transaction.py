# expense_tracker/presenter/transaction.py

from sqlalchemy.orm import Session

from datetime import datetime

from enum import Enum

from datetime import datetime

from expense_tracker.constants import Constants

from expense_tracker.model.orm import engine
from expense_tracker.model.orm.db_transaction import DB_Transaction
from expense_tracker.model.orm.db_merchant import DB_Merchant
from expense_tracker.model.orm.db_amount import DB_Amount
from expense_tracker.model.orm.db_account import DB_Account
from expense_tracker.model.orm.db_merchant_location import DB_Merchant_Location
from expense_tracker.model.orm.db_tag import DB_Tag
from expense_tracker.model.orm.db_budget import DB_Budget
from expense_tracker.model.orm.db_month_budget import DB_Month_Budget


class Transaction:
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
    def get_display_list() -> list[tuple[int, ...]]:
        """
        Returns a list of all transactions as a list of tuples of strings
        """

        display_list: list[tuple[int, ...]] = []

        with Session(engine) as session:
            for entry in session.query(DB_Transaction).all():
                display_list.append(
                    (
                        entry.id,
                        entry.reconciled_status,
                        entry.description,
                        entry.merchant.name,
                        datetime.strftime(entry.date, Constants.DATE_FORMAT),
                        ", ".join(tag.name for tag in entry.amounts[0].tags),
                        entry.amounts[
                            0
                        ].amount,  # TODO Edit this to support multiple amounts
                    )
                )

        return display_list

    @staticmethod
    def set_value(id: int, column: Column, new_value: any) -> any:
        """
        Updates a cell in the database.
        """

        if new_value == None:
            raise TypeError("new_value must have a value")

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

        raise ValueError(f"Unable to handel an edit of database column '{column}'.")
