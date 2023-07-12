# expense_tracker/cli/merchants.py

import typer

from typing import Optional, List

from typing_extensions import Annotated

from expense_tracker.cli.cli_utils import Print_Utils

from expense_tracker.model.merchant_database import Merchant_Database
from expense_tracker.model.merchant import Merchant


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
            Merchant_Database.create(name)

            Print_Utils.success_message(f"Created '{name}' merchant.")

        except Exception as error:
            Print_Utils.error_message("Unable to create merchant.", error_message=error)

    @app.command()
    def delete(
        id: Annotated[int, typer.Argument(help="ID of merchant to be deleted")]
    ) -> None:
        """
        Attempt to delete an existing merchant.
        """

        target_merchant_list: List[Merchant] = Merchant_Database.get_filterd_by_id(id)

        if len(target_merchant_list) == 0:
            Print_Utils.error_message("No merchant found by that id.")
            raise typer.Exit()

        if not len(target_merchant_list) == 1:
            raise LookupError(f"Database returned more then one result for id '{id}'")

        target_merchant: Merchant = target_merchant_list[0]

        try:
            Merchant_Database.delete(target_merchant)
            Print_Utils.success_message(f"Deleted merchant '{target_merchant.name}'")

        except Exception as error:
            Print_Utils.error_message(
                f"Unable to delete merchant, likley because one or more transactions reference it.",
                error_message=error,
            )

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

        merchants_list: List[Merchant]

        if filter:
            merchants_list = Merchant_Database.get_filterd_by_name(filter)
        else:
            merchants_list = Merchant_Database.get_all()

        Print_Utils.merchant_table(merchants_list)

    @app.callback()
    def callback() -> None:
        """
        Edits merchants, to add or remove locations from each merchant use "exptrack location".
        """
