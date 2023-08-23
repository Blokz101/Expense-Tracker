# expense_tracker/model/db_util.py

from sqlalchemy.orm import Session

import re

from typing import Optional

from expense_tracker.model.orm import engine
from expense_tracker.model.orm.db_transaction import DB_Transaction
from expense_tracker.model.orm.db_merchant import DB_Merchant
from expense_tracker.model.orm.db_amount import DB_Amount
from expense_tracker.model.orm.db_account import DB_Account
from expense_tracker.model.orm.db_merchant_location import DB_Merchant_Location
from expense_tracker.model.orm.db_tag import DB_Tag
from expense_tracker.model.orm.db_budget import DB_Budget
from expense_tracker.model.orm.db_month_budget import DB_Month_Budget


class DB_Util:
    """
    Database manipulation utility functions.
    """

    @staticmethod
    def get_merchant_from_description(description: str) -> Optional[DB_Merchant]:
        """
        Uses existing merchant naming rules to try to find a merchant for a given statement description.

        Args:
            description: Statement row description.

        Return: DB_Merchant if one was found.
        """
        with Session(engine) as session:
            for merchant in session.query(DB_Merchant).all():
                if not merchant.naming_rule:
                    continue

                if re.search(merchant.naming_rule, description):
                    return merchant

        return None

    @staticmethod
    def get_transaction_amount(transaction: DB_Transaction) -> float:
        """
        Get the total amount for a transaction.

        Args:
            transaction: Transaction whose amounts should be totaled.

        Return: Amount total.
        """

        with Session(engine) as session:
            return sum(
                amount.amount
                for amount in session.query(DB_Amount)
                .where(DB_Amount.transaction == transaction)
                .all()
            )
