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

from expense_tracker.model import Base
from expense_tracker.model import engine
from expense_tracker.model.merchant import Merchant
from expense_tracker.model.amount import Amount
from expense_tracker.model.merchant_location import Merchant_Location
from expense_tracker.model.transaction import Transaction
from expense_tracker.model.tag import Tag
from expense_tracker.model.account import Account


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

    @staticmethod
    @app.command()
    def add(
        photo: Annotated[
            bool,
            typer.Option("--photo", help="Create transactions based on photos."),
        ] = True,
        auto: Annotated[
            bool,
            typer.Option(
                "--auto",
                help="Automatically create transactions based on photos and bank statement.",
            ),
        ] = False,
    ) -> None:
        """
        Create new transactions.
        """

        console.print("Add")

        # TODO Finish this method

    @staticmethod
    @app.command()
    def reconcile() -> None:
        """
        Reconcile new transactions with bank statement.
        """

        print("Reconcile")

        # TODO Finish this method