# expense_tracker/cil.py

from typing_extensions import Annotated

from rich.console import Console

import typer
import configparser

from expense_tracker import __app_name__, __version__
from expense_tracker.model import Database
from expense_tracker.config_manager import ConfigManager
from expense_tracker.exceptions import DatabaseNotFound, DatabaseAlreadyExists


class CLI:
    """
    ViewController for the application. Deals with command line user interaction.
    """

    app: typer.Typer = typer.Typer()

    console: Console = Console(highlight=False)
    configs: ConfigManager = ConfigManager()

    database: Database

    def _version_callback(value: bool) -> None:
        """
        Callback for version option.
        """

        if value:
            print(f"{__app_name__} {__version__}")
            raise typer.Exit()

    def _init_callback(value: bool) -> None:
        """
        Callback for init version option.
        """

        if value:

            try:
                Database.create_database(CLI.configs.get("files", "database_path"))

                CLI.console.print(
                    "\n\tSuccessfully created new database!\n", style="Green"
                )

            except DatabaseAlreadyExists as error:
                CLI.print_exception(error)

            raise typer.Exit()

    @staticmethod
    @app.callback()
    def main(
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
                help="Create a new database.",
                callback=_init_callback,
                is_eager=True,
            ),
        ] = False,
    ) -> None:
        """
        Reconcile and track expenses using receipt photos and bank statements.
        """

        try:
            CLI.database = Database()

        except (configparser.NoOptionError, DatabaseNotFound) as error:
            CLI.print_exception(error)

    @staticmethod
    @app.command()
    def add(
        photo: Annotated[
            bool, typer.Option(help="Create transactions based on photos.")
        ] = True,
        auto: Annotated[
            bool,
            typer.Option(
                help="Automatically create transactions based on photos and bank statement."
            ),
        ] = False,
    ) -> None:
        """
        Create new transactions.
        """

        print("Add")

    @staticmethod
    @app.command()
    def reconcile() -> None:
        """
        Reconcile new transactions with bank statement.
        """

        print("Reconcile")

    @staticmethod
    def print_exception(error: Exception) -> None:
        """
        Print an exception message and exit
        """
        CLI.console.print(f"\n\t{error}\n", style="red")
        raise typer.Exit()
