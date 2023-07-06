# expense_tracker/cli/cil.py

from typing_extensions import Annotated

import typer

from configparser import NoOptionError

from sqlite3 import OperationalError

from expense_tracker import __app_name__, __version__
from expense_tracker.cli import configs, console
from expense_tracker.model.database import Database
from expense_tracker.exceptions import DatabaseAlreadyExists, DatabaseNotFound
from expense_tracker.cli.merchants import Merchants
from expense_tracker.cli.tags import Tags
from expense_tracker.cli.cli_utils import StatusPrint
from expense_tracker.constants import StatusMessage as msg


class CLI:
    """
    ViewController for the application. Deals with command line user interaction.
    """

    app: typer.Typer = typer.Typer()
    app.add_typer(Merchants.app, name="merchant")
    app.add_typer(Tags.app, name="tag")

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
                Database.create_database(configs.get("files", "database_path"))

                StatusPrint.success(msg.DATABASE_CREATION_SUCCESS)
                
            except DatabaseAlreadyExists as error:
                StatusPrint.error(msg.DATABASE_ALREADY_ESISTS, error_message = error)
                
            except DatabaseNotFound as error:
                StatusPrint.error(msg.DATABASE_NOT_FOUND, error_message = error)
                
            except NoOptionError as error:
                StatusPrint.error(msg.SETTING_OPTION_NOT_FOUND, error_message = error)
                
            except OperationalError as error:
                StatusPrint.error(msg.CANNOT_OPEN_DATABASE, error_message = error)

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

    @staticmethod
    @app.command()
    def reconcile() -> None:
        """
        Reconcile new transactions with bank statement.
        """

        print("Reconcile")
