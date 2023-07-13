# expense_tracker/cli/merchants.py

import typer

from typing import Optional, List

from typing_extensions import Annotated

from expense_tracker.cli import console

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
        name: Annotated[str, typer.Argument(help="Name of merchant to be deleted")]
    ) -> None:
        """
        Attempt to delete an existing merchant.
        """
        
        merchant_list: List[str] = Merchant_Database.get_all()
        merchant_name_list: List[str] = [merchant.name for merchant in merchant_list]

        target_index: int = Print_Utils.input_from_options(
                    merchant_name_list, input=name
        )
        target_merchant: Merchant = merchant_list[target_index]

        try:
            Merchant_Database.delete(target_merchant)
            Print_Utils.success_message(f"Deleted merchant '{target_merchant.name}'")

        except Exception as error:
            Print_Utils.error_message(
                f"Unable to delete merchant, likley because one or more transactions reference it.",
                error_message=error,
            )
            
    @app.command()
    def rename(
        name: Annotated[str, typer.Argument(help="Current name of merchant to be renamed")]
    ) -> None:
        """
        Attempt to delete an existing merchant.
        """
        
        merchant_list: List[str] = Merchant_Database.get_all()
        merchant_name_list: List[str] = [merchant.name for merchant in merchant_list]

        target_index: int = Print_Utils.input_from_options(
                    merchant_name_list, input=name
        )
        target_merchant: Merchant = merchant_list[target_index]
        
        new_name: str = console.input("New merchant name >>> ")

        try:
            Merchant_Database.rename(target_merchant, new_name)
            Print_Utils.success_message(f"Renamed merchant '{name}' to \'{new_name}\'")

        except Exception as error:
            Print_Utils.error_message(
                f"Unable to rename merchant.",
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
