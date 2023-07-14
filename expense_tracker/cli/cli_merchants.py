# expense_tracker/cli/cli_merchants.py

import typer

from typing import Optional, List

from typing_extensions import Annotated

from sqlalchemy.orm import Session

from expense_tracker.model import engine
from expense_tracker.model.merchant import Merchant
from expense_tracker.model.amount import Amount
from expense_tracker.model.merchant_location import Merchant_Location
from expense_tracker.model.transaction import Transaction
from expense_tracker.model.tag import Tag
from expense_tracker.model.account import Account

from expense_tracker.cli import console
from expense_tracker.cli.cli_utils import Print_Utils, Print_Tables

from rich.table import Table


class CLI_Merchants:
    app: typer.Typer = typer.Typer()

    @app.command()
    def create(
        name: Annotated[str, typer.Argument(help="Name of the merchant.")]
    ) -> None:
        """
        Create a new merchant.
        """

        try:
            with Session(engine) as session:
                session.add(Merchant(name=name))
                session.commit()

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

        with Session(engine) as session:
            merchant_list: List[str] = session.query(Merchant).all()

            target_merchant: Merchant = merchant_list[
                Print_Utils.input_from_options(
                    [merchant.name for merchant in merchant_list], input=name
                )
            ]

            try:
                session.delete(target_merchant)
                session.commit()

                Print_Utils.success_message(f"Deleted merchant '{target_merchant.name}'")

            except Exception as error:
                Print_Utils.error_message(
                    f"Unable to delete merchant, likley because one or more transactions reference it.",
                    error_message=error,
                )

    @app.command()
    def rename(
        name: Annotated[
            str, typer.Argument(help="Current name of merchant to be renamed")
        ]
    ) -> None:
        """
        Attempt to delete an existing merchant.
        """

        with Session(engine) as session:
            merchant_list: List[str] = session.query(Merchant).all()

            target_merchant: Merchant = merchant_list[
                Print_Utils.input_from_options(
                    [merchant.name for merchant in merchant_list], input=name
                )
            ]

            new_name: str = console.input("New merchant name >>> ")

            try:
                target_merchant.name = new_name
                session.commit()

                Print_Utils.success_message(f"Renamed merchant '{name}' to '{new_name}'")

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

        with Session(engine) as session:

            table: Table = Print_Tables.merchant_table
            
            for merchant in session.query(Merchant).all():
                table.add_row(str(merchant.id), merchant.name)
                
            console.print(table)
            

    @app.callback()
    def callback() -> None:
        """
        Edits merchants, to add or remove locations from each merchant use "exptrack location".
        """
