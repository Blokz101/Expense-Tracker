# expense_tracker/presenter/merchant.py

from sqlalchemy.orm import Session

from datetime import datetime

from enum import Enum

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


class Merchant:
    """
    Merchant presenter
    """

    class Column(Enum):
        ID: int = 0
        NAME: int = 1
        NAMING_RULE: int = 2

    @staticmethod
    def get_all() -> list[tuple[int, ...]]:
        """
        Returns a list of all merchants as a list of tuples of strings
        """

        display_list: list[tuple[int, ...]] = []

        with Session(engine) as session:
            for entry in session.query(DB_Merchant).all():
                display_list.append(
                    (
                        entry.id,
                        entry.name,
                        entry.naming_rule,
                    )
                )

        return display_list
