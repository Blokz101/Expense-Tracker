# expense_tracker/cli/cil.py

from typing_extensions import Annotated

import typer

from expense_tracker.cli.cli_utils import Print_Utils

from expense_tracker import __app_name__, __version__
from expense_tracker.cli import console
from expense_tracker.cli.cli_merchants import CLI_Merchants
from expense_tracker.cli.cli_tags import CLI_Tags
from expense_tracker.cli.cli_accounts import CLI_Accounts
from expense_tracker.cli.cli_merchant_locations import CLI_Merchant_Locations
from expense_tracker.cli.cli_transactions import CLI_Transactions

from expense_tracker.orm import Base
from expense_tracker.orm import engine
from expense_tracker.orm.merchant import Merchant
from expense_tracker.orm.amount import Amount
from expense_tracker.orm.merchant_location import Merchant_Location
from expense_tracker.orm.transaction import Transaction
from expense_tracker.orm.tag import Tag
from expense_tracker.orm.account import Account


class CLI:
    """
    ViewController for the application. Deals with command line user interaction.
    """

    # Link the commands from the other classes to the main CLI application
    app: typer.Typer = typer.Typer()
    app.add_typer(CLI_Merchants.app, name="merchant")
    app.add_typer(CLI_Tags.app, name="tag")
    app.add_typer(CLI_Accounts.app, name="account")
    app.add_typer(CLI_Merchant_Locations.app, name="location")
    app.add_typer(CLI_Transactions.app, name="trans")

    def _version_callback(value: bool) -> None:
        """
        Callback for version option.
        """

        if value:
            console.print(f"{__app_name__} {__version__}")
            raise typer.Exit()

    def _init_callback(value: bool) -> None:
        """
        Callback for init option.
        """

        if value:
            Base.metadata.create_all(engine)
            Print_Utils.success_message("Created database.")
            raise typer.Exit()

    @staticmethod
    @app.callback()
    def callback(
        version: Annotated[
            bool,
            typer.Option(
                "--version",
                help="Display the version.",
                callback=_version_callback,
                is_eager=True,
            ),
        ] = False,
        init: Annotated[
            bool,
            typer.Option(
                "--init",
                help="Create the database.",
                callback=_init_callback,
            ),
        ] = False,
    ) -> None:
        """
        Reconcile and track expenses using receipt photos and bank statements.
        """
