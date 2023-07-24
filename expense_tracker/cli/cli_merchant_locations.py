# expense_tracker/cli/cli_merchant_locations.py

import typer

from typing import Optional, List, Tuple

from typing_extensions import Annotated

from sqlalchemy.orm import Session

from expense_tracker.config_manager import ConfigManager

from expense_tracker.orm import engine
from expense_tracker.orm.merchant import Merchant
from expense_tracker.orm.amount import Amount
from expense_tracker.orm.merchant_location import Merchant_Location
from expense_tracker.orm.transaction import Transaction
from expense_tracker.orm.tag import Tag
from expense_tracker.orm.account import Account

from expense_tracker.model.photo_manager import Photo_Manager

from expense_tracker.cli import console
from expense_tracker.cli.cli_utils import Print_Utils, Print_Tables

from rich.table import Table


class CLI_Merchant_Locations:
    """
    Commands to edit the merchant locations database.
    """

    app: typer.Typer = typer.Typer()

    @app.command()
    def create(
        merchant: Annotated[
            str,
            typer.Argument(help="Merchant to add the default location to."),
        ],
        photo: Annotated[
            bool,
            typer.Option("--photo", help="Set to get coords from a photo."),
        ] = True,
        manual: Annotated[
            bool,
            typer.Option("--manual", help="Set to manually enter the coords"),
        ] = False,
    ) -> None:
        """
        Create a new merchant location and assign it to a merchant
        """

        # Check that there is some coord input option selected
        if not (photo or manual):
            Print_Utils.error_message("You must use either '--photo' or '--manual'")
            raise typer.Exit()

        with Session(engine) as session:
            # Get a list of merchants from the database
            merchant_list: List[Merchant] = session.query(Merchant).all()

            # Prompt the user to select a merchant and set it as the target merchant
            target_merchant: Merchant = Print_Utils.input_from_options(
                merchant_list,
                lambda x: x.name,
                prompt_message="Select a merchant",
                first_input=merchant,
            )

            new_coords: tuple[float, float]

            # If photo is set then try to get the coords from a photo
            if photo:
                try:
                    path: str = Print_Utils.input_file_path("Enter the path to photo")

                    new_coords = Photo_Manager.get_coords(path)

                    Print_Utils.success_message(
                        f"Found coordinates from photo: ( {new_coords[0]}, {new_coords[1]} )"
                    )

                # If an error occurs, catch it and print
                except AttributeError as error:
                    Print_Utils.error_message(
                        f"Cannot get coordinates from photo at '{path}'.",
                        error_message=error,
                    )
                    raise typer.Exit()

            # If the manual tag is set then get the coords manually
            elif manual:
                # Get and validate the x coord
                x_coord: str = Print_Utils.input_rule("Enter the x coordinate")
                if not x_coord.isdecimal():
                    Print_Utils.error_message("Invalid x coordinate.")

                # Get and validate the y coord
                y_coord: str = Print_Utils.input_rule("Enter the y coordinate")
                if not y_coord.isdecimal():
                    Print_Utils.error_message("Invalid y coordinate.")

                new_coords = (x_coord, y_coord)

            # Get any locations that the new coords might be close to.
            possible_location: Optional[
                Merchant_Location
            ] = Merchant_Location.possible_location(
                new_coords,
                session.query(Merchant_Location)
                .where(Merchant_Location.merchant == target_merchant)
                .all(),
                ConfigManager().get_same_merchant_mile_radius(),
            )

            # If the location might already be in the database, print an error and exit
            if possible_location:
                Print_Utils.error_message(
                    f"The new coordinate ({new_coords[0]}, {new_coords[1]}) is close enough to existing location ({possible_location.x_coord}, {possible_location.y_coord}) to be the same location."
                )
                raise typer.Exit()

            # Get the name of the new location
            location_name: str = Print_Utils.input_rule("Enter a location name")

            # Commit the new merchant location
            session.add(
                Merchant_Location(
                    merchant_id=target_merchant.id,
                    name=location_name,
                    x_coord=new_coords[0],
                    y_coord=new_coords[1],
                )
            )
            session.commit()

            # Print success message
            Print_Utils.success_message(f"Created '{location_name}'.")

    @app.command()
    def delete(
        merchant_name: Annotated[
            str, typer.Argument(help="Name of merchant that the location belongs to.")
        ],
        merchant_location_name: Annotated[
            str, typer.Argument(help="Current name of location.")
        ],
    ) -> None:
        """
        Attempt to rename an existing merchant location.
        """

        with Session(engine) as session:
            # Get a list of merchants from the database
            merchant_list: List[str] = session.query(Merchant).all()

            # Prompt the user to select a merchant and set it as the target merchant
            target_merchant: Merchant = Print_Utils.input_from_options(
                merchant_list,
                lambda x: x.name,
                prompt_message="Select a merchant",
                first_input=merchant_name,
            )

            # Get a list of merchants from the database
            location_list: List[str] = (
                session.query(Merchant_Location)
                .where(Merchant_Location.merchant_id == target_merchant.id)
                .all()
            )

            # Prompt the user to select a merchant location and set it as the target location
            target_merchant_location: Merchant = Print_Utils.input_from_options(
                location_list,
                lambda x: x.name,
                prompt_message="Select a location",
                first_input=merchant_location_name,
            )

            # Attempt to commit the rename
            try:
                session.delete(target_merchant_location)
                session.commit()

                Print_Utils.success_message(
                    f"Deleted location '{merchant_location_name}'."
                )

            # If an error occurs, catch it and print the message
            except Exception as error:
                Print_Utils.error_message(
                    f"Unable to delete location.",
                    error_message=error,
                )

    @app.command()
    def rename(
        merchant_name: Annotated[
            str, typer.Argument(help="Name of merchant that the location belongs to.")
        ],
        merchant_location_name: Annotated[
            str, typer.Argument(help="Current name of location.")
        ],
    ) -> None:
        """
        Attempt to rename an existing merchant location.
        """

        with Session(engine) as session:
            # Get a list of merchants from the database
            merchant_list: List[str] = session.query(Merchant).all()

            # Prompt the user to select a merchant and set it as the target account
            target_merchant: Merchant = Print_Utils.input_from_options(
                merchant_list,
                lambda x: x.name,
                prompt_message="Select a merchant",
                first_input=merchant_name,
            )

            # Get a list of merchants from the database
            location_list: List[str] = (
                session.query(Merchant_Location)
                .where(Merchant_Location.merchant_id == target_merchant.id)
                .all()
            )

            # Prompt the user to select a merchant and set it as the target account
            target_merchant_location: Merchant = Print_Utils.input_from_options(
                location_list,
                lambda x: x.name,
                prompt_message="Select a location",
                first_input=merchant_location_name,
            )

            # Prompt the user for a new name
            new_name: str = console.input("New location name >>> ")

            # Attempt to commit the rename
            try:
                target_merchant_location.name = new_name
                session.commit()

                Print_Utils.success_message(
                    f"Renamed location '{merchant_location_name}' to '{new_name}'"
                )

            # If an error occurs, catch it and print the message
            except Exception as error:
                Print_Utils.error_message(
                    f"Unable to rename location",
                    error_message=error,
                )

    @app.command()
    def list() -> None:
        """
        List all merchant locations
        """

        with Session(engine) as session:
            # Get the empty table object and populate it
            table: Table = Print_Tables.merchant_location_table
            merchant_list: List[Merchant_Location] = (
                session.query(Merchant_Location)
                .order_by(Merchant_Location.merchant_id)
                .all()
            )
            for merchant_location in merchant_list:
                table.add_row(
                    str(merchant_location.id),
                    merchant_location.name,
                    merchant_location.merchant.name,
                    str(merchant_location.x_coord),
                    str(merchant_location.y_coord),
                )

            # Print the table
            console.print(table)
