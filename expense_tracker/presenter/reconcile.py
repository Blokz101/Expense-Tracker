# expense_tracker/presenter/reconcile.py

from typing import Optional, Union

from pathlib import Path

from enum import Enum
from typing import Union

from sqlalchemy.orm import Session

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

from expense_tracker.model.reconcile_session import Reconcile_Session
from expense_tracker.model.statement_manager import ST_Transaction
from expense_tracker.model.db_util import DB_Util


from typing import Union


class Reconcile:
    """
    Presenter for Reconcile_Session.
    """

    class Full_Column(Enum):
        ST_ID: int = 0
        ST_MERCHANT: int = 1
        ST_DESCRIPTION: int = 2
        ST_DATE: int = 3
        ST_AMOUNT: int = 4
        DB_ID: int = 5
        DB_DESCRIPTION: int = 6
        DB_MERCHANT: int = 7
        DB_DATE: int = 8
        DB_AMOUNT: int = 9

    class Orphan_Column(Enum):
        DB_ID: int = 0
        DB_MERCHANT: int = 2
        DB_DATE: int = 3
        DB_AMOUNT: int = 4

    reconcile_session: Optional[Reconcile_Session] = None
    statement_path: Optional[Path] = None
    account_id: Optional[Path] = None

    @staticmethod
    def ongoing_session() -> bool:
        """
        Checks if there is a session in progress.

        Return: True or false based on if there is an ongoing session.
        """
        return not Reconcile.reconcile_session is None

    @staticmethod
    def new_session(statement_path: Path, account_id: int) -> None:
        """
        Create a new session with.

        Args:
            new_session: Path to the statement csv.
            account_id: ID of the account to reconcile against a statement.
        """
        Reconcile.statement_path = statement_path
        Reconcile.account_id = account_id
        Reconcile.reconcile_session = Reconcile_Session(statement_path, account_id)

    @staticmethod
    def kill_session() -> None:
        """
        Kill the current session.
        """
        Reconcile.reconcile_session = None
        Reconcile.statement_path = None
        Reconcile.account_id = None

    @staticmethod
    def _format(
        transaction: Union[ST_Transaction, DB_Transaction]
    ) -> tuple[str, str, str, str, str]:
        """
        Formats a database or statement transaction into a list of strings.

        Args:
            transaction: Statement or database transaction to be formatted.

        Return: List of strings that can be displayed in the terminal.
        """
        if type(transaction) == ST_Transaction:
            with Session(engine) as session:
                # Do not know if the statement transaction has a merchant, if it does then bind it to the session
                if transaction.merchant:
                    session.add(transaction.merchant)

                return (
                    str(transaction.row_id),
                    transaction.description,
                    transaction.merchant.name if transaction.merchant else "None",
                    datetime.strftime(transaction.date, Constants.DATE_FORMAT),
                    str(transaction.amount),
                )

        if type(transaction) == DB_Transaction:
            with Session(engine) as session:
                # The database transaction will have a merchant, add it to the session
                session.add(transaction)

                return (
                    str(transaction.id),
                    transaction.description,
                    transaction.merchant.name,
                    datetime.strftime(transaction.date, Constants.DATE_FORMAT),
                    str(DB_Util.get_transaction_amount(transaction)),
                )

        # If the type is not DB_Transaction or ST_Transaction then throw an error
        raise TypeError(
            f"transaction must be of type DB_Transaction or ST_Transaction not {type(transaction)}"
        )

    @staticmethod
    def get_statement_list() -> (
        list[tuple[str, str, str, str, str, str, str, str, str, str]]
    ):
        """
        Get statements form the current reconcile session and format them for display:

        Return: List of strings that represent rows in the statement.
        """

        formatted_list: list[
            tuple[str, str, str, str, str, str, str, str, str, str]
        ] = []

        for row in Reconcile.reconcile_session.reconcile_row_list:
            formatted_db_trans: tuple[str, str, str, str, str] = Reconcile._format(
                row.statement_trans
            )
            formatted_st_trans: tuple[str, str, str, str, str] = (
                Reconcile._format(row.matched_trans)
                if row.matched_trans
                else ("", "", "", "", "")
            )

            formatted_list.append(formatted_db_trans + formatted_st_trans)

        return formatted_list

    @staticmethod
    def get_possible_match_list() -> (
        list[tuple[str, str, str, str, str, str, str, str, str, str]]
    ):
        """
        Get a list of possible matches for each statement transaction without a match and format them for display.

        The first tuple of strings will have the statement info as the first five string and the following tuples will have blanks for the first five strings.

        Return: List of strings, that represent the statement transaction and its possible matches.
        """

        formatted_list: list[
            tuple[str, str, str, str, str, str, str, str, str, str]
        ] = []

        for row in Reconcile.reconcile_session.reconcile_row_list:
            if row.matched_trans or not row.possible_match_list:
                continue

            formatted_list.extend(Reconcile._format_possible_row(row))

        return formatted_list

    @staticmethod
    def _format_possible_row(
        row: Reconcile_Session.Row,
    ) -> list[tuple[str, str, str, str, str, str, str, str, str, str]]:
        """
        Formats the possible matches of a reconcile row into a displayable format.

        The first tuple of strings will have the statement info as the first five string and the following tuples will have blanks for the first five strings.

        Args:
            row: Reconcile session row that contains a statement transaction and possible database transaction matches.

        Return: List of strings that can be displayed in the terminal.
        """

        # A list of all the rows needed to display one statement transaction and all its possibly matching database transactions
        display_rows: list[tuple[str, str, str, str, str, str, str, str, str, str]] = []

        for index, possible_match in enumerate(row.possible_match_list):
            statement_cells: tuple[str, str, str, str] = (
                Reconcile._format(row.statement_trans)
                if index == 0
                else (str(row.statement_trans.row_id), "", "", "")
            )
            database_cells: tuple[str, str, str, str] = Reconcile._format(
                possible_match
            )

            display_rows.append((statement_cells + database_cells))

        return display_rows

    @staticmethod
    def get_orphan_list() -> list[tuple[str, str, str, str]]:
        """
        Get a list of database transactions that are not reconciled and did not get matched and put them in a displayable format.

        Return: List of tuple of strings, each tuple is a row strings representing each database orphan.
        """

        return list(
            Reconcile._format(orphan)
            for orphan in Reconcile.reconcile_session.orphan_list
        )

    @staticmethod
    def set_value(
        row_id: int,
        column: Union[Full_Column, Orphan_Column],
        new_value: Union[int, str, datetime],
    ) -> str:
        """
        Set the value of a cell in the reconcile session.

        Args:
            row_id: ID of the row of the target cell.
            column: Column of the target cell.
            new_value: Value that the cell should be set to.

        Return: Value of the target cell after the set_value function.
        """

        with Session(engine) as session:
            if column == Reconcile.Full_Column.ST_MERCHANT:
                new_merchant: DB_Merchant = (
                    session.query(DB_Merchant)
                    .where(DB_Merchant.id == new_value)
                    .first()
                )
                Reconcile.reconcile_session.set_statement_transaction_merchant(
                    row_id, new_merchant
                )
                return Reconcile.reconcile_session.reconcile_row_list[
                    row_id
                ].statement_trans.merchant.name

        Presenter.set_value(id, column, new_value)

    @staticmethod
    def committable() -> bool:
        """
        If all the statements have been matched.

        Returns:
            Boolean that represents if the session is committable.
        """
        return Reconcile.reconcile_session.committable()

    @staticmethod
    def commit() -> None:
        """
        Commits the session.
        """
        Reconcile.reconcile_session.commit()
