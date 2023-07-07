# expense_tracker/cli/merchants.py

import typer

from typing import Optional

from expense_tracker.model.merchant_database import Merchant_Database
from expense_tracker.model.database import Database
from expense_tracker.cli import configs, console
from expense_tracker.cli.cli_utils import StatusPrint

from typing_extensions import Annotated


class Merchants:
    app: typer.Typer = typer.Typer()

    @app.command()
    def create(
        name: Annotated[str, typer.Argument(help="Name of the merchant.")]
    ) -> None:
        """
        Create a new merchant.
        """

        database: Database = Database(configs.database_path())

        try:
            Merchant_Database.create(
                database,
                name,
            )

            StatusPrint.success(f"Created '{name}' merchant.")

        except Exception as error:
            StatusPrint.error("Unable to create merchant.", error_message=error)

    @app.command()
    def delete(id: Annotated[int, typer.Argument(help="ID of the merchant.")]) -> None:
        """
        Attempt to delete an existing merchant.
        """

        database: Database = Database(configs.database_path())

        try:
            console.print(Merchant_Database.get_filterd_by_id(database, id))

            if typer.confirm("Are you sure that you want to delete this merchant?"):
                Merchant_Database.delete(database, id)

                StatusPrint.success("Deleted merchant.")

        except Exception as error:
            StatusPrint.error("Unable to delete merchant.", error_message=error)

    @app.command()
    def list(
        filter: Annotated[
            Optional[str],
            typer.Argument(help="Filter by string found in merchant names"),
        ] = None
    ) -> None:
        """
        List all merchants, filter by name if needed
        """

        database: Database = Database(configs.database_path())

        result: tuple

        if filter:
            result = Merchant_Database.get_filterd_by_name(database, filter)

        else:
            result = Merchant_Database.get_all(database)

        console.print(result)

    @app.callback()
    def callback() -> None:
        """
        Edits merchants, to add or remove locations from each merchant use "exptrack location".
        """
