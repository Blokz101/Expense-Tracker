# expense_tracker/cli/cil.py

from typing_extensions import Annotated

import typer

from expense_tracker import __app_name__, __version__
from expense_tracker.cli import configs, console
from expense_tracker.cli.cli_merchants import CLI_Merchants
from expense_tracker.constants import GeneralConstants
from expense_tracker.cli.cli_tags import CLI_Tags
from expense_tracker.cli.cli_utils import Print_Utils


class CLI:
    """
    ViewController for the application. Deals with command line user interaction.
    """

    app: typer.Typer = typer.Typer()
    app.add_typer(CLI_Merchants.app, name="merchant")
    app.add_typer(CLI_Tags.app, name="tag")

    def _version_callback(value: bool) -> None:
        """
        Callback for version option.
        """

        if value:
            print(f"{__app_name__} {__version__}")
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
    ) -> None:
        """
        Reconcile and track expenses using receipt photos and bank statements.
        """

        pass

    @staticmethod
    @app.command()
    def add(
        photo: Annotated[
            bool, typer.Option("--photo", help="Create transactions based on photos.")
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
