# expense_tracker/cli/merchants.py


import typer

from typing import Optional

from expense_tracker.model.merchant_database import Merchant_Database
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

        try:
            Merchant_Database.create(
                configs.get("files", "database_path"),
                name,
            )

            StatusPrint.success(f"Created '{name}' merchant.")

        except Exception as error:
            StatusPrint.error("Unable to create merchant.", error_message=error)

    # @app.command()
    # def delete(
    #     id: Annotated[int, typer.Option(prompt=True, help="Name of the merchant.")]
    # ) -> None:
    #     """
    #     Attempt to delete an existing merchant.
    #     """

    #     try:
    #         Merchant_Database.delete_merchant(configs.get("files", "database_path"), id)

    #         StatusPrint.success("Deleted merchant.")

    #     except Exception as error:
    #         StatusPrint.error("Unable to delete merchant.", error_message=error)

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

        result: tuple

        if filter:
            result = Merchant_Database.get_filterd_by_name(
                configs.get("files", "database_path"), filter
            )

        else:
            result = Merchant_Database.get_all(configs.get("files", "database_path"))

        console.print(result)

    @app.callback()
    def callback() -> None:
        """
        Edits merchants, to add or remove locations from each merchant use "exptrack location".
        """
