# expense_tracker/presenter/transaction.py

from sqlalchemy.orm import Session

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
    TODO Fill this in later
    """

    @staticmethod
    def get_display() -> list:
        display_list: list[tuple[str, ...]] = []

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
                        entry.amounts[0].amount,
                    )
                )

        return display_list
