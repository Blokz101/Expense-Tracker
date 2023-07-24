# expense_tracker/cli/cli_accounts.py

import typer

from typing import Optional, List

from typing_extensions import Annotated

from sqlalchemy.orm import Session

from expense_tracker.orm import engine
from expense_tracker.orm.merchant import Merchant
from expense_tracker.orm.amount import Amount
from expense_tracker.orm.merchant_location import Merchant_Location
from expense_tracker.orm.transaction import Transaction
from expense_tracker.orm.tag import Tag
from expense_tracker.orm.account import Account
from expense_tracker.orm.budget import Budget
from expense_tracker.orm.month_budget import Month_Budget

from expense_tracker.cli import console
from expense_tracker.cli.cli_utils import Print_Utils, Print_Tables

from rich.table import Table


class CLI_Accounts:
    """
    Commands to edit the accounts database.
    """

    app: typer.Typer = typer.Typer()

    @app.command()
    def create(
        name: Annotated[str, typer.Argument(help="Name of the account")]
    ) -> None:
        """
        Create a new account.
        """

        # Attempt to create the account
        try:
            with Session(engine) as session:
                session.add(Account(name=name))
                session.commit()

            Print_Utils.success_message(f"Created '{name}' account")

        # If an error occurs, catch it and print the message
        except Exception as error:
            Print_Utils.error_message("Unable to create account", error_message=error)

    @app.command()
    def delete(
        name: Annotated[str, typer.Argument(help="Name of account to be deleted")]
    ) -> None:
        """
        Attempt to delete an existing account.
        """

        with Session(engine) as session:
            # Get a list of accounts from the database
            account_list: List[str] = session.query(Account).all()

            # Prompt the user to select an account and set it as the target account
            target_account: Account = Print_Utils.input_from_options(
                account_list,
                lambda x: x.name,
                prompt_message="Select an account",
                first_input=name,
            )

            # Attempt to delete the account
            try:
                session.delete(target_account)
                session.commit()

                Print_Utils.success_message(f"Deleted account '{target_account.name}'")

            # If an error occurred, catch it and print the message
            except Exception as error:
                Print_Utils.error_message(
                    f"Unable to delete account, likely because one or more transactions reference it",
                    error_message=error,
                )

    @app.command()
    def rename(
        name: Annotated[
            str, typer.Argument(help="Current name of account to be renamed")
        ]
    ) -> None:
        """
        Attempt to delete an existing account.
        """

        with Session(engine) as session:
            # Get a list of accounts from the database
            account_list: List[str] = session.query(Account).all()

            # Prompt the user to select an account and set it as the target account
            target_account: Account = Print_Utils.input_from_options(
                account_list,
                lambda x: x.name,
                prompt_message="Select an account",
                first_input=name,
            )

            # Prompt the user for a new name
            new_name: str = console.input("New account name >>> ")

            # Attempt to commit the rename
            try:
                target_account.name = new_name
                session.commit()

                Print_Utils.success_message(f"Renamed account '{name}' to '{new_name}'")

            # If an error occurs, catch it and print the message
            except Exception as error:
                Print_Utils.error_message(
                    f"Unable to rename account",
                    error_message=error,
                )

    @app.command()
    def list(
        filter: Annotated[
            Optional[str],
            typer.Argument(help="Filter by string found in account names"),
        ] = None
    ) -> None:
        """
        List all accounts, filter by name if needed
        """

        with Session(engine) as session:
            # Get the empty table object and populate it
            table: Table = Print_Tables.account_table
            for account in session.query(Account).all():
                table.add_row(str(account.id), account.name)

            # Print the table
            console.print(table)

    @app.callback()
    def callback() -> None:
        """
        Edits accounts, to add or remove locations from each account use "exptrack location".
        """
