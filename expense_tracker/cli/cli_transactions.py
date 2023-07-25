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
            Print_Utils.error_message("Unable to use photo, continuing in manual mode.")
            photo_path = None

        CLI_Transactions._create_transaction(photo_path=photo_path, income=income)

    @staticmethod
    def _create_transaction(
        photo_path: Optional[Path] = None, income: bool = False
    ) -> None:
        """
        Create a transaction and submit it to the database.
        """

        date_default: datetime = None
        description_default: str = None
        merchant_default: Merchant_Location = None

        # Get the defaults for each field if a photo is provided
        if photo_path:
            date_default = CLI_Transactions._get_date_default(photo_path)
            description_default = CLI_Transactions._get_description_default(photo_path)
            merchant_default = CLI_Transactions._get_merchant_default(photo_path)

            console.print("Found defaults from photo metadata:")

            console.print(f" + Date: ", end="")
            console.print(
                datetime.strftime(date_default, GeneralConstants.DATE_FORMAT),
                style=GeneralConstants.HIGHLIGHTED_STYLE,
            )

            console.print(f" + Description: ", end="")
            console.print(description_default, style=GeneralConstants.HIGHLIGHTED_STYLE)

            console.print(f" + Merchant: ", end="")
            if merchant_default:
                console.print(
                    merchant_default.name, style=GeneralConstants.HIGHLIGHTED_STYLE
                )
            else:
                console.print("None", style="red")

        # Prompt the user to select each field
        account: Account = CLI_Transactions._get_account(
            default=CLI_Transactions._get_account_default()
        )
        date: datetime = CLI_Transactions._get_date(default=date_default)
        amount: float = CLI_Transactions._get_amount(income=income)
        description: str = CLI_Transactions._get_description(
            default=description_default
        )
        merchant: Merchant = CLI_Transactions._get_merchant(default=merchant_default)
        tag_list: List[Tag] = CLI_Transactions._get_tags(merchant=merchant)

        # Create and commit the new transaction
        with Session(engine) as session:
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

            # Add the new amount and its tags
            new_amount: Amount = Amount(
                transaction_id=new_transaction.id, amount=amount
            )
            new_amount.tags = tag_list
            session.add(new_amount)

            session.commit()

        Print_Utils.success_message("Created transaction.")

    @staticmethod
    def _get_account_default() -> Account:
        """
        Return the default account specified by the user in the settings
        """

        with Session(engine) as session:
            return session.query(Account).all()[
                ConfigManager().get_default_account_id()
            ]

    @staticmethod
    def _get_account(default: Optional[Account] = None) -> Account:
        """
        Get the account from the user
        """

        with Session(engine) as session:
            return Print_Utils.input_from_options(
                session.query(Account).all(),
                lambda x: x.name,
                "Enter a transaction account",
                default=default,
            )

    @staticmethod
    def _get_date_default(photo_path: Path) -> datetime:
        """
        Get the date default from a given photo
        """

        return Photo_Manager.get_date(photo_path)

    @staticmethod
    def _get_date(default: Optional[datetime] = None) -> datetime:
        """
        Get the date from the user
        """

        # Set the default as today if one was not provided
        date_default: datetime = default
        if not date_default:
            date_default = datetime.today()

        # Return the the date
        return Print_Utils.input_date(
            "Enter a transaction date",
            default=date_default,
        )

    @staticmethod
    def _get_amount(income=False) -> float:
        """
        Get the amount from the user
        """

        if income:
            return Print_Utils.input_float(
                "Enter an [bold]income[/bold] amount",
            )
        else:
            return -1 * Print_Utils.input_float(
                "Enter an [bold]expense[/bold] amount",
            )

    @staticmethod
    def _get_description_default(photo_path: Path) -> str:
        """
        Get the description default from a given photo
        """

        return Photo_Manager.get_description(photo_path)

    @staticmethod
    def _get_description(default: Optional[str] = None) -> str:
        """
        Get the description from the user
        """

        return Print_Utils.input_rule(
            "Enter a description",
            default=default,
        )

    @staticmethod
    def _get_merchant_default(photo_path: Path) -> Optional[Merchant]:
        """
        Get the merchant default from a given photo
        """

        # Get the photo coords and print them
        photo_coords = Photo_Manager.get_coords(photo_path)

        with Session(engine) as session:
            # Find possible locations, if there is one, return it
            possible_location: Optional[
                Merchant_Location
            ] = Merchant_Location.possible_location(
                photo_coords,
                session.query(Merchant_Location).all(),
                same_location__mile_radius=ConfigManager().get_same_merchant_mile_radius(),
            )
            if possible_location:
                return possible_location.merchant

        return None

    @staticmethod
    def _get_merchant(default: Optional[Merchant] = None) -> Merchant:
        """
        Get the merchant from the user
        """

        with Session(engine) as session:
            return Print_Utils.input_from_options(
                session.query(Merchant).all(),
                lambda x: x.name,
                "Enter a transaction merchant",
                default=default,
            )

    @staticmethod
    def _get_tags(merchant: Optional[Merchant] = None) -> List[Tag]:
        """
        Get the list of tags from the user
        """
        with Session(engine) as session:
            # If a merchant is set then get the default tags from it
            tags_default: Optional[List[Tag]] = None
            if merchant:
                session.add(merchant)
                tags_default = merchant.default_tags

            return Print_Utils.input_from_toggle_list(
                session.query(Tag).all(),
                lambda x: x.name,
                "Select a tag",
                initial_selected_list=tags_default,
            )

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
