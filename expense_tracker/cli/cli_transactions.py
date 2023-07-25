# expense_tracker/cli/cli_transactions.py

import typer

from pathlib import Path

from typing import Optional, List, Tuple

from typing_extensions import Annotated

from sqlalchemy.orm import Session

from expense_tracker.config_manager import ConfigManager
from expense_tracker.constants import GeneralConstants

from expense_tracker.orm import engine
from expense_tracker.orm.merchant import Merchant
from expense_tracker.orm.amount import Amount
from expense_tracker.orm.merchant_location import Merchant_Location
from expense_tracker.orm.transaction import Transaction
from expense_tracker.orm.tag import Tag
from expense_tracker.orm.account import Account
from expense_tracker.orm.budget import Budget
from expense_tracker.orm.month_budget import Month_Budget

from expense_tracker.model.photo_manager import Photo_Manager

from expense_tracker.cli import console
from expense_tracker.cli.cli_utils import Print_Utils, Print_Tables
from expense_tracker.cli.cli_transaction_utils import CLI_Transaction_Utils

from datetime import datetime

from rich.table import Table

import re

import os


class CLI_Transactions:
    """
    Commands to edit the transactions database.
    """

    app: typer.Typer = typer.Typer()

    @app.command()
    def create(
        income: Annotated[
            bool,
            typer.Option("--income", help="Set mark the transaction as income."),
        ] = False,
    ) -> None:
        """
        Create a new transaction.
        """

        photo_path: Optional[Path] = None

        # Get the user input and clean it
        user_input: str = Print_Utils.input_rule("Path to photo")
        user_input = re.sub("'", "", user_input)

        # Attempt to convert user input to path
        try:
            photo_path = Path(user_input)
        except:
            pass

        # Print a message based on if a photo is being used or not
        if photo_path and os.path.isfile(photo_path):
            Print_Utils.success_message(
                f"Importing information from photo at '{photo_path}'."
            )
        else:
            photo_path = None

        CLI_Transaction_Utils._create_transaction(photo_path=photo_path, income=income)

    @app.command()
    def list(
        account_name: Annotated[str, typer.Argument(help="Name of the account")]
    ) -> None:
        """
        List transactions from an account.
        """

        with Session(engine) as session:
            # Get a list of transactions that have the specified account
            target_account: Account = Print_Utils.input_from_options(
                session.query(Account).all(),
                lambda x: x.name,
                prompt_message="Select an account",
                first_input=account_name,
            )
            transaction_list: List[Transaction] = session.query(Transaction).where(
                Transaction.account_id == target_account.id
            )

            table: Table = Print_Tables.transaction_table

            # TODO Edit the method of adding rows so it accounts for multiple amounts and tags

            for transaction in transaction_list:
                table.add_row(
                    str(transaction.id),
                    str(transaction.reconciled_status),
                    transaction.description,
                    transaction.merchant.name,
                    datetime.strftime(transaction.date, GeneralConstants.DATE_FORMAT),
                    str(transaction.amounts[0].amount),
                    ", ".join(tag.name for tag in transaction.amounts[0].tags),
                )

            console.print(table)

    @app.command()
    def delete(
        id: Annotated[int, typer.Argument(help="ID of transaction to be deleted")],
    ) -> None:
        """
        Attempt to delete an existing transaction.
        """

        with Session(engine) as session:
            # Attempt to delete the transaction
            target_transaction: Transaction = (
                session.query(Transaction).where(Transaction.id == id).first()
            )
            try:
                session.delete(target_transaction)
                session.commit()

                Print_Utils.success_message("Deleted transaction.")

            # If an error occurred, catch it and print the message
            except Exception as error:
                Print_Utils.error_message(
                    "Unable to delete the transaction", error_message=error
                )
