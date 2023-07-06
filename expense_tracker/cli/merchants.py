# expense_tracker/cli/merchants.py


import typer

from expense_tracker.model.merchant_database import Merchant_Database
from expense_tracker.cli import configs
from expense_tracker.cli.cli_utils import StatusPrint

from typing_extensions import Annotated


class Merchants:
    app: typer.Typer = typer.Typer()

    @app.command()
    def create(
        name: Annotated[str, typer.Option(prompt=True, help="Name of the merchant.")]
    ) -> None:
        """
        Create a new merchant
        """

        try:
            Merchant_Database.create_merchant(
                configs.get("files", "database_path"),
                name,
            )

            StatusPrint.success(f"Created '{name}' merchant.")

        except Exception as error:
            StatusPrint.error("Unable to create merchant.", error_message=error)

    @app.callback()
    def main() -> None:
        """
        Edits merchants, to add or remove locations from each merchant use "exptrack location".
        """
