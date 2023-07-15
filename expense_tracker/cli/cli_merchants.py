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
        name: Annotated[str, typer.Argument(help="Name of the merchant")]
    ) -> None:
        """
        Create a new merchant.
        """

        # Attempt to create the merchant
        try:
            with Session(engine) as session:
                session.add(Merchant(name=name))
                session.commit()

            Print_Utils.success_message(f"Created '{name}' merchant")

        # If an error occurs, catch it and print the message
        except Exception as error:
            Print_Utils.error_message("Unable to create merchant", error_message=error)

    @app.command()
    def delete(
        name: Annotated[str, typer.Argument(help="Name of merchant to be deleted")]
    ) -> None:
        """
        Attempt to delete an existing merchant.
        """

        with Session(engine) as session:
            # Get a list of merchants from the database
            merchant_list: List[str] = session.query(Merchant).all()

            # Prompt the user to select a merchant and set it as the target account
            target_merchant: Merchant = merchant_list[
                Print_Utils.input_from_options(
                    [merchant.name for merchant in merchant_list], input=name
                )
            ]

            # Attempt to delete the merchant
            try:
                session.delete(target_merchant)
                session.commit()

                Print_Utils.success_message(
                    f"Deleted merchant '{target_merchant.name}'"
                )

            # If an error occurs, catch it and print the message
            except Exception as error:
                Print_Utils.error_message(
                    f"Unable to delete merchant, likely because one or more transactions reference it",
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
            # get a list of merchants from the database
            merchant_list: List[str] = session.query(Merchant).all()

            # Prompt the user to select a merchant and set it as the target account
            target_merchant: Merchant = merchant_list[
                Print_Utils.input_from_options(
                    [merchant.name for merchant in merchant_list], input=name
                )
            ]

            # Prompt the user for a new name
            new_name: str = console.input("New merchant name >>> ")

            # Attempt to commit the rename
            try:
                target_merchant.name = new_name
                session.commit()

                Print_Utils.success_message(
                    f"Renamed merchant '{name}' to '{new_name}'"
                )

            # If an error occurs, catch it and print the message
            except Exception as error:
                Print_Utils.error_message(
                    f"Unable to rename merchant",
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
            # Get the empty table object and populate it
            table: Table = Print_Tables.merchant_table
            for merchant in session.query(Merchant).all():
                table.add_row(
                    str(merchant.id),
                    merchant.name,
                    ", ".join([default.name for default in merchant.default_tags]),
                )

            # Print the table
            console.print(table)

    @app.command()
    def default(
        merchant_name: Annotated[str, typer.Argument(help="Name of merchant")],
        tag_name: Annotated[str, typer.Argument(help="Name of tag to toggle")],
    ) -> None:
        """
        Add or remove a default tag from a merchant.
        """

        with Session(engine) as session:
            # Get a list of merchants from the database
            merchant_list: List[Merchant] = session.query(Merchant).all()

            # Prompt the user to select an account and set it as the target merchant
            target_merchant: Merchant = merchant_list[
                Print_Utils.input_from_options(
                    [merchant.name for merchant in merchant_list], input=merchant_name
                )
            ]

            # Get a list of tags from the database
            tag_list: List[Tag] = session.query(Tag).all()

            # Prompt the user to select a tag and set it as the target tag
            target_tag: Merchant = tag_list[
                Print_Utils.input_from_options(
                    [tag.name for tag in tag_list], input=tag_name
                )
            ]

            # If the merchant already has the tag, remove it
            if target_tag in target_merchant.default_tags:
                target_merchant.default_tags.remove(target_tag)
                Print_Utils.success_message(
                    f"Removed default tag '{target_tag.name}' from merchant '{target_merchant.name}'"
                )

            # if the merchant does not have the tag, add it
            else:
                target_merchant.default_tags.append(target_tag)
                Print_Utils.success_message(
                    f"Added default tag '{target_tag.name}' to merchant '{target_merchant.name}'"
                )

            session.commit()

    @app.callback()
    def callback() -> None:
        """
        Edits merchants, to add or remove locations from each merchant use "exptrack location".
        """
