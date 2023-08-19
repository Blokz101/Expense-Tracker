# expense_tracker/model/reconcile_session.py

from pathlib import Path

from typing import Optional

from copy import copy

from dataclasses import dataclass

from sqlalchemy.orm import Session

from expense_tracker.model.statement_manager import Statement, ST_Transaction
from expense_tracker.model.db_util import DB_Util

from expense_tracker.model.orm import engine
from expense_tracker.model.orm.db_transaction import DB_Transaction
from expense_tracker.model.orm.db_merchant import DB_Merchant
from expense_tracker.model.orm.db_amount import DB_Amount
from expense_tracker.model.orm.db_account import DB_Account
from expense_tracker.model.orm.db_merchant_location import DB_Merchant_Location
from expense_tracker.model.orm.db_tag import DB_Tag
from expense_tracker.model.orm.db_budget import DB_Budget
from expense_tracker.model.orm.db_month_budget import DB_Month_Budget


class Reconcile_Session:
    """
    Transaction reconcile session.
    """

    @dataclass
    class Row:
        statement_trans: ST_Transaction
        matched_trans: Optional[DB_Transaction] = None
        flagged_trans: Optional[list[DB_Transaction]] = None

    def __init__(self, statement_path: Path, account_id: int) -> None:
        """
        Initializes the class.

        Args:
            statement_path: Path to statement.
            account_id: ID of the account that the statement belongs to.
        """

        self._account_id: int = account_id

        self.db_trans_list: list[DB_Transaction] = self._get_unreconciled_transactions()
        self.st_trans_list: list[ST_Transaction] = Statement(
            statement_path, self._account_id
        ).get_all()

        self.reconcile_row_list: list[Reconcile_Session.Row]
        self.orphan_list: list[DB_Transaction]

        self.match()

    def _get_unreconciled_transactions(self) -> list[DB_Transaction]:
        """
        TODO Fill this in
        """

        with Session(engine) as session:
            return (
                session.query(DB_Transaction)
                .where(DB_Transaction.reconciled_status == False)
                .where(DB_Transaction.account_id == self._account_id)
                .all()
            )

    def match(self) -> None:
        """
        TODO Fill this in
        """

        # Clear the reconcile row list and orphan list to rewrite them
        self.reconcile_row_list = list(
            Reconcile_Session.Row(st_trans) for st_trans in self.st_trans_list
        )
        self.orphan_list = []

        # Create a list to keep track of the remaining database transactions
        remaining_db_trans: list[DB_Transaction] = copy(self.db_trans_list)

        # For each row check for matches, if there are any then record them and remove the database transaction form the remaining transactions list
        for row in self.reconcile_row_list:
            # Check for match, if there is one then set the row's matched transaction and remove the database transaction from the remaining transactions list
            match: DB_Transaction = self._find_match(
                row.statement_trans, remaining_db_trans
            )
            if match:
                row.matched_trans = match
                remaining_db_trans.remove(match)

    def _find_match(
        self, st_trans: ST_Transaction, remaining_db_trans: list[DB_Transaction]
    ) -> Optional[DB_Transaction]:
        """
        TODO Fill this in
        """

        # Check the statement trans against the remaining database trans, if one is a match return it.
        for db_trans in remaining_db_trans:
            if self.matching_trans_fields(st_trans, db_trans) == 3:
                return db_trans

        # No matches were found
        return None

    def matching_trans_fields(
        self, st_trans: ST_Transaction, db_trans: DB_Transaction
    ) -> int:
        """
        TODO Fill this in
        """

        matching_fields: int = 0

        with Session(engine) as session:
            session.add(db_trans)

            # Check the amount
            if st_trans.amount == DB_Util.get_transaction_amount(db_trans):
                matching_fields = +1

            # Check date
            if st_trans.date.date() == db_trans.date.date():
                matching_fields = +1

            # Check merchant
            if (
                DB_Util.get_merchant_from_description(st_trans.description)
                == db_trans.merchant
            ):
                matching_fields = +1

        return matching_fields
