# expense_tracker/cli/cli_tags.py

import typer

from typing import Optional, List

from typing_extensions import Annotated

from sqlalchemy.orm import Session

from expense_tracker.orm import engine
from expense_tracker.orm.merchant import Merchant
from expense_tracker.orm.amount import Amount
from expense_tracker.orm.merchant_location import Merchant_Location
from expense_tracker.orm.transaction import Transaction
from expense_tracker.orm.tag import Tag
from expense_tracker.orm.account import Account

from expense_tracker.cli import console
from expense_tracker.cli.cli_utils import Print_Utils, Print_Tables

from rich.table import Table


class CLI_Tags:
    """
    Commands for interacting with the tags database.
    """

    app: typer.Typer = typer.Typer()

    @app.command()
    def create(name: Annotated[str, typer.Argument(help="Name of the tag")]) -> None:
        """
        Create a new tag.
        """

        # Attempt to create the tag
        try:
            with Session(engine) as session:
                session.add(Tag(name=name))
                session.commit()

            Print_Utils.success_message(f"Created '{name}' tag")

        # If an error occurs, catch and print it
        except Exception as error:
            Print_Utils.error_message("Unable to create tag", error_message=error)

    @app.command()
    def delete(
        name: Annotated[str, typer.Argument(help="Name of tag to be deleted")]
    ) -> None:
        """
        Attempt to delete an existing tag.
        """

        with Session(engine) as session:
            # Get a list of tags from the database
            tag_list: List[str] = session.query(Tag).all()

            # Prompt the user to select a tag and set it as the target tag
            target_tag: Tag = Print_Utils.input_from_options(
                tag_list,
                lambda x: x.name,
                prompt_message="Select a tag",
                first_input=name,
            )

            # Attempt to delete the tag
            try:
                session.delete(target_tag)
                session.commit()

                Print_Utils.success_message(f"Deleted tag '{target_tag.name}'")

            # If an error occurred, catch it and print the message
            except Exception as error:
                Print_Utils.error_message(
                    f"Unable to delete tag, likely because one or more transactions reference it",
                    error_message=error,
                )

    @app.command()
    def rename(
        name: Annotated[str, typer.Argument(help="Current name of tag to be renamed")]
    ) -> None:
        """
        Attempt to delete an existing tag.
        """

        with Session(engine) as session:
            # Get a list of tags from the database
            tag_list: List[str] = session.query(Tag).all()

            # Prompt the user to select a tag and set it as the target tag
            target_tag: Tag = Print_Utils.input_from_options(
                tag_list,
                lambda x: x.name,
                prompt_message="Select a tag",
                first_input=name,
            )

            # Prompt the user for a new name
            new_name: str = console.input("New tag name >>> ")

            # Attempt to commit the rename
            try:
                target_tag.name = new_name
                session.commit()

                Print_Utils.success_message(f"Renamed tag '{name}' to '{new_name}'")

            # If an error occurs, catch it and print the message
            except Exception as error:
                Print_Utils.error_message(
                    f"Unable to rename tag",
                    error_message=error,
                )

    @app.command()
    def list(
        filter: Annotated[
            Optional[str],
            typer.Argument(help="Filter by string found in tag names"),
        ] = None
    ) -> None:
        """
        List all tags, filter by name if needed
        """

        with Session(engine) as session:
            # Get the empty table object and populate it
            table: Table = Print_Tables.tag_table
            for tag in session.query(Tag).all():
                table.add_row(str(tag.id), tag.name)

            # Print the table
            console.print(table)

    @app.callback()
    def callback() -> None:
        """
        Edits tags, to add or remove locations from each tag use "exptrack location".
        """
