# expense_tracker/model/reconcile_session.py

from pathlib import Path

from typing import Optional

from copy import deepcopy

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
        possible_match_list: Optional[list[DB_Transaction]] = None

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
        Get all unreconciled transactions.

        Returns:
            A list of transactions that have not been reconciled.
        """

        with Session(engine) as session:
            return (
                session.query(DB_Transaction)
                .where(DB_Transaction.reconciled_status == False)
                .where(DB_Transaction.account_id == self._account_id)
                .order_by(DB_Transaction.date)
                .all()
            )

    def match(self) -> None:
        """
        Match rows from the statement to transactions that have not been reconciled.
        """

        # Clear the reconcile row list and orphan list to rewrite them
        self.reconcile_row_list = list(
            Reconcile_Session.Row(st_trans) for st_trans in self.st_trans_list
        )
        self.orphan_list = []

        # Create a list to keep track of the remaining database transactions
        remaining_db_trans: list[DB_Transaction] = deepcopy(self.db_trans_list)

        with Session(engine) as session:

            session.add_all(remaining_db_trans)

            # For each row check for matches, if there are any then record them and remove the database transaction form the remaining transactions list
            for row in self.reconcile_row_list:
                match: DB_Transaction = self._find_match(
                    row.statement_trans, remaining_db_trans
                )
                if match:
                    row.matched_trans = match
                    remaining_db_trans.remove(match)

            # Find possible matches for each non matched statement transaction
            for row in self.reconcile_row_list:
                # Dont find possible matches if a confirmed one is already found
                if row.matched_trans:
                    continue

                row.possible_match_list = self._find_possible_matches(
                    row.statement_trans, remaining_db_trans
                )

        # Set the orphans list
        self.orphan_list = remaining_db_trans
        self.orphan_list.sort(key=lambda x: x.date, reverse=True)

    def _find_match(
        self, st_trans: ST_Transaction, remaining_db_trans: list[DB_Transaction]
    ) -> Optional[DB_Transaction]:
        """
        Try to find database transaction a match for a statement row.

        Match is defined as a database transaction where all columns (amount, merchant, date) are equal.

        Args:
            st_trans: Statement Row in the form of a ST_Transaction.
            remaining_db_trans: List of the database transactions that have not been reconciled or matched.

        Returns: Database transaction if one is found.
        """

        # Check the statement trans against the remaining database trans, if one is a match return it.
        for db_trans in remaining_db_trans:
            if self._matching_trans_fields(st_trans, db_trans) == 3:
                return db_trans

        # No matches were found
        return None

    def _find_possible_matches(
        self, st_trans: ST_Transaction, remaining_db_trans: list[DB_Transaction]
    ) -> list[DB_Transaction]:
        """
        Try to find database transactions that might match a statement row.

        Possible match is defined as a database transaction where two of three columns (amount, merchant, date) are equal.

        Args:
            st_trans: Statement Row in the form of a ST_Transaction.
            remaining_db_trans: List of the database transactions that have not been reconciled or matched.

        Returns: List of database transaction if it might be a possible match.
        """

        possible_matches_list: list[DB_Transaction] = []

        # Check the statement trans against the remaining database trans, if two out of three fields match then add it.
        for db_trans in remaining_db_trans:
            if self._matching_trans_fields(st_trans, db_trans) == 2:
                possible_matches_list.append(db_trans)

        # Return the list
        return possible_matches_list

    def _matching_trans_fields(
        self, st_trans: ST_Transaction, db_trans: DB_Transaction
    ) -> int:
        """
        Find the number of columns (amount, merchant, date) that match.

        Args:
            st_trans: Statement row in the form of a ST_Transaction.
            db_trans: Database transaction.

        Return: Int from 0 to 3 that represents how many columns (amount, merchant, date) are equal.
        """

        matching_fields: int = 0

        # Check the amount
        if abs(st_trans.amount) == abs(DB_Util.get_transaction_amount(db_trans)):
            matching_fields += 1

        # Check date
        if st_trans.date.date() == db_trans.date.date():
            matching_fields += 1

        # Check merchant
        if st_trans.merchant and st_trans.merchant.id == db_trans.merchant.id:
            matching_fields += 1

        return matching_fields

    def set_statement_transaction_merchant(
        self, row_id: int, new_merchant: DB_Merchant
    ) -> None:
        """
        Set the merchant for a statement transaction in the current reconcile session.

        Args:
            row_id: ID of the row to be edited.
            new_merchant: New merchant.
        """

        self.reconcile_row_list[row_id].statement_trans.merchant = new_merchant
        self.match()

    def committable(self) -> bool:
        """
        If all the statements have been matched.

        Returns:
            Boolean that represents if the session is committable.
        """

        for row in self.reconcile_row_list:
            if not row.matched_trans:
                return False

        return True

    def commit(self) -> None:
        """
        Try to commit the session.
        """

        if not self.committable():
            raise RuntimeError("Session is not committable")

        with Session(engine) as session:

            for row in self.reconcile_row_list:
                db_trans: DB_Transaction = row.matched_trans
                session.add(db_trans)
                db_trans.reconciled_status = True
            session.commit()
