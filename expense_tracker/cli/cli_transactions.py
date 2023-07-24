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

from datetime import datetime

from rich.table import Table


class CLI_Transactions:
    """
    Commands to edit the transactions database.
    """

    app: typer.Typer = typer.Typer()

    @app.command()
    def create(
        manual: Annotated[
            bool,
            typer.Option("--manual", help="Set to input all information manually."),
        ] = False,
        income: Annotated[
            bool,
            typer.Option("--income", help="Set mark the transaction as income."),
        ] = False,
    ) -> None:
        """
        Create a new transaction.
        """

        photo_path: Path
        if not manual:
            photo_path = Print_Utils.input_file_path("Path to photo")

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

            # Set the default as either today or the date that the photo was taken based no if a photo was provided
            date_default: datetime = datetime.today()
            if not manual:
                date_default = Photo_Manager.get_date(photo_path)
                Print_Utils.extract_message(
                    "Extracted date from photo:",
                    datetime.strftime(date_default, GeneralConstants.DATE_FORMAT),
                )

            # Get the date
            date: datetime = Print_Utils.input_date(
                "Enter a transaction date",
                default=date_default,
            )

            # Get the amount
            amount: float
            if income:
                amount = Print_Utils.input_float(
                    "Enter an [bold]income[/bold] amount",
                )
            else:
                amount = -1 * Print_Utils.input_float(
                    "Enter an [bold]expense[/bold] amount",
                )

            # Set the default as either today or the date that the photo was taken based no if a photo was provided
            description_default: Optional[str] = None
            if not manual:
                description_default = Photo_Manager.get_description(photo_path)
                Print_Utils.extract_message(
                    "Extracted description from photo:", description_default
                )

            # Get the description
            description: str = Print_Utils.input_rule(
                "Enter a description",
                default=description_default,
            )

            # Set the default as either today or the date that the photo was taken based no if a photo was provided
            merchant_default: Optional[Merchant] = None
            if not manual:
                # Get the photo coords and print them
                photo_coords = Photo_Manager.get_coords(photo_path)
                Print_Utils.extract_message(
                    "Extracted coords from photo:", photo_coords
                )

                # Check for any possible locations if there are any, print them
                possible_location: Optional[
                    Merchant_Location
                ] = Merchant_Location.possible_location(
                    photo_coords,
                    session.query(Merchant_Location).all(),
                    same_location__mile_radius=ConfigManager().get_same_merchant_mile_radius(),
                )
                if possible_location:
                    merchant_default = possible_location.merchant
                    console.print(f"Coordinates match possible location ", end="")
                    console.print(
                        merchant_default.name, style=GeneralConstants.HIGHLIGHTED_STYLE
                    )
                else:
                    console.print("Coordinates do not match any location.")

            # Get the merchant
            merchant: Merchant = Print_Utils.input_from_options(
                session.query(Merchant).all(),
                lambda x: x.name,
                "Enter a transaction merchant",
                default=merchant_default,
            )

            # Get the tags
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
