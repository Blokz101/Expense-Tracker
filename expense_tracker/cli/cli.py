# expense_tracker/cli/cil.py

from typing_extensions import Annotated

import typer

from expense_tracker import __app_name__, __version__
from expense_tracker.cli import configs, console
from expense_tracker.cli.merchants import Merchants

# from expense_tracker.model.database import (
#     Database,
#     DatabaseAlreadyExists,
#     DatabaseNotFound,
# )
from expense_tracker.constants import GeneralConstants
from expense_tracker.cli.tags import Tags
from expense_tracker.cli.cli_utils import StatusPrint


class CLI:
    """
    ViewController for the application. Deals with command line user interaction.
    """

    app: typer.Typer = typer.Typer()
    app.add_typer(Merchants.app, name="merchant")
    app.add_typer(Tags.app, name="tag")

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

        # TODO Impliment _init_callback

        # if value:
        #     try:
        #         database: Database = Database(configs.database_path())

        #         database.create_database(
        #             GeneralConstants.DATABASE_TEMPLATE_PATH,
        #         )

        #         StatusPrint.success("Created new database!")

        #     except DatabaseAlreadyExists as error:
        #         StatusPrint.error(error)

        #     except DatabaseNotFound as error:
        #         StatusPrint.error(error)

        #     raise typer.Exit()

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
    def main() -> None:
        console.print("WORKING")

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
