# expense_tracker/cli/cli_accounts.py

import typer

from typing import Optional, List

from typing_extensions import Annotated

from sqlalchemy.orm import Session

from expense_tracker.model import engine
from expense_tracker.model.merchant import Merchant
from expense_tracker.model.amount import Amount
from expense_tracker.model.merchant_location import Merchant_Location
from expense_tracker.model.transaction import Transaction
from expense_tracker.model.tag import Tag
from expense_tracker.model.account import Account

from expense_tracker.cli import console
from expense_tracker.cli.cli_utils import Print_Utils, Print_Tables

from rich.table import Table


class CLI_Accounts:
    app: typer.Typer = typer.Typer()

    @app.command()
    def create(
        name: Annotated[str, typer.Argument(help="Name of the account")]
    ) -> None:
        """
        Create a new account.
        """

        try:
            with Session(engine) as session:
                session.add(Account(name=name))
                session.commit()

            Print_Utils.success_message(f"Created '{name}' account")

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
            account_list: List[str] = session.query(Account).all()

            target_account: Account = account_list[
                Print_Utils.input_from_options(
                    [account.name for account in account_list], input=name
                )
            ]

            try:
                session.delete(target_account)
                session.commit()

                Print_Utils.success_message(f"Deleted account '{target_account.name}'")

            except Exception as error:
                Print_Utils.error_message(
                    f"Unable to delete account, likley because one or more transactions reference it",
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
            account_list: List[str] = session.query(Account).all()

            target_account: Account = account_list[
                Print_Utils.input_from_options(
                    [account.name for account in account_list], input=name
                )
            ]

            new_name: str = console.input("New account name >>> ")

            try:
                target_account.name = new_name
                session.commit()

                Print_Utils.success_message(f"Renamed account '{name}' to '{new_name}'")

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
            table: Table = Print_Tables.account_table

            for account in session.query(Account).all():
                table.add_row(str(account.id), account.name)

            console.print(table)

    @app.callback()
    def callback() -> None:
        """
        Edits accounts, to add or remove locations from each account use "exptrack location".
        """
