# expense_tracker/cli/cli_transactions.py

import typer

from typing import Optional, List

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

from expense_tracker.cli import console
from expense_tracker.cli.cli_utils import Print_Utils, Print_Tables

from datetime import datetime

from rich.table import Table


class CLI_Transactions:
    """
    Commands to edit the transactions database.
    """

    app: typer.Typer = typer.Typer()

    @app.command()
    def create() -> None:
        """
        Create a new transaction using data from a photo.
        """

        # TODO Implement this method

    @app.command()
    def mancreate() -> None:
        """
        Manually create a new transaction.
        """

        with Session(engine) as session:
            # Get the account, date, merchant, and amount
            account: Account = Print_Utils.input_from_options(
                session.query(Account).all(),
                lambda x: x.name,
                "Enter a transaction account",
                default=session.query(Account).all()[
                    ConfigManager().get_default_account_id()
                ],
            )
            date: datetime = Print_Utils.input_date(
                "Enter a transaction date", default=datetime.today()
            )
            amount: float = Print_Utils.input_float("Enter an amount")
            description: str = Print_Utils.input_rule(
                "Enter a description",
            )
            merchant: Merchant = Print_Utils.input_from_options(
                session.query(Merchant).all(),
                lambda x: x.name,
                "Enter a transaction merchant",
            )
            tag_list: List[Tag] = Print_Utils.input_from_toggle_list(
                session.query(Tag).all(),
                lambda x: x.name,
                "Select a tag",
                initial_selected_list=merchant.default_tags,
            )

            # Add the new transaction
            new_transaction: Transaction = Transaction(
                account_id=account.id,
                description=description,
                merchant_id=merchant.id,
                date=date,
                reconciled_status=False,
            )
            session.add(new_transaction)
            session.flush()

            # Add the new amount, its tags, and commit
            new_amount: Amount = Amount(
                transaction_id=new_transaction.id, amount=amount
            )
            new_amount.tags = tag_list
            session.add(new_amount)
            session.commit()

        Print_Utils.success_message("Created transaction.")

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
