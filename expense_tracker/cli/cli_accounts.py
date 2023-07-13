# expense_tracker/cli/cli_accounts.py

import typer

from typing import Optional, List

from typing_extensions import Annotated

from expense_tracker.cli import console

from expense_tracker.cli.cli_utils import Print_Utils

from expense_tracker.model.account_database import Account_Database
from expense_tracker.orm.account import Account


class CLI_Accounts:
    app: typer.Typer = typer.Typer()

    @app.command()
    def create(
        name: Annotated[str, typer.Argument(help="Name of the account.")]
    ) -> None:
        """
        Create a new account.
        """

        try:
            Account_Database.create(name)

            Print_Utils.success_message(f"Created '{name}' account.")

        except Exception as error:
            Print_Utils.error_message("Unable to create account.", error_message=error)

    @app.command()
    def delete(
        name: Annotated[str, typer.Argument(help="Name of account to be deleted")]
    ) -> None:
        """
        Attempt to delete an existing account.
        """

        account_list: List[str] = Account_Database.get_all()
        target_account: Account = account_list[
            Print_Utils.input_from_options(
                [account.name for account in account_list], input=name
            )
        ]

        try:
            Account_Database.delete(target_account)
            Print_Utils.success_message(f"Deleted account '{target_account.name}'")

        except Exception as error:
            Print_Utils.error_message(
                f"Unable to delete account, likley because one or more transactions reference it.",
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

        account_list: List[str] = Account_Database.get_all()
        target_account: Account = account_list[
            Print_Utils.input_from_options(
                [account.name for account in account_list], input=name
            )
        ]

        new_name: str = console.input("New account name >>> ")

        try:
            Account_Database.rename(target_account, new_name)
            Print_Utils.success_message(f"Renamed account '{name}' to '{new_name}'")

        except Exception as error:
            Print_Utils.error_message(
                f"Unable to rename account.",
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

        accounts_list: List[Account]

        if filter:
            accounts_list = Account_Database.get_filterd_by_name(filter)
        else:
            accounts_list = Account_Database.get_all()

        Print_Utils.account_table(accounts_list)

    @app.callback()
    def callback() -> None:
        """
        Edits accounts, to add or remove locations from each account use "exptrack location".
        """
