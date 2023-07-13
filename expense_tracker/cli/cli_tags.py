# expense_tracker/cli/cli_tags.py

import typer

from typing import Optional, List

from typing_extensions import Annotated

from expense_tracker.cli import console

from expense_tracker.cli.cli_utils import Print_Utils

from expense_tracker.model.tag_database import Tag_Database
from expense_tracker.orm.tag import Tag


class CLI_Tags:
    app: typer.Typer = typer.Typer()

    @app.command()
    def create(name: Annotated[str, typer.Argument(help="Name of the tag.")]) -> None:
        """
        Create a new tag.
        """

        try:
            Tag_Database.create(name)

            Print_Utils.success_message(f"Created '{name}' tag.")

        except Exception as error:
            Print_Utils.error_message("Unable to create tag.", error_message=error)

    @app.command()
    def delete(
        name: Annotated[str, typer.Argument(help="Name of tag to be deleted")]
    ) -> None:
        """
        Attempt to delete an existing tag.
        """

        tag_list: List[str] = Tag_Database.get_all()
        target_tag: Tag = tag_list[
            Print_Utils.input_from_options([tag.name for tag in tag_list], input=name)
        ]

        try:
            Tag_Database.delete(target_tag)
            Print_Utils.success_message(f"Deleted tag '{target_tag.name}'")

        except Exception as error:
            Print_Utils.error_message(
                f"Unable to delete tag, likley because one or more transactions reference it.",
                error_message=error,
            )

    @app.command()
    def rename(
        name: Annotated[str, typer.Argument(help="Current name of tag to be renamed")]
    ) -> None:
        """
        Attempt to delete an existing tag.
        """

        tag_list: List[str] = Tag_Database.get_all()
        target_tag: Tag = tag_list[
            Print_Utils.input_from_options([tag.name for tag in tag_list], input=name)
        ]

        new_name: str = console.input("New tag name >>> ")

        try:
            Tag_Database.rename(target_tag, new_name)
            Print_Utils.success_message(f"Renamed tag '{name}' to '{new_name}'")

        except Exception as error:
            Print_Utils.error_message(
                f"Unable to rename tag.",
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

        tags_list: List[Tag]

        if filter:
            tags_list = Tag_Database.get_filterd_by_name(filter)
        else:
            tags_list = Tag_Database.get_all()

        Print_Utils.tag_table(tags_list)

    @app.callback()
    def callback() -> None:
        """
        Edits tags, to add or remove locations from each tag use "exptrack location".
        """
