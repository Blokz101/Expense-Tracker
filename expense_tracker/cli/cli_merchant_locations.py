# expense_tracker/cli/cli_merchant_locations.py

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

            # Prompt the user to select a merchant and set it as the target account
            target_merchant: Merchant = merchant_list[
                Print_Utils.input_from_options(
                    [mernt.name for mernt in merchant_list],
                    input=merchant,
                )
            ]

            coords: tuple[float, float]

            # If photo is set then try to get the coords from a photo
            if photo:
                try:
                    path: str = Print_Utils.input_file_path("Enter the path to photo")

                    coords = Photo_Manager.get_coords(path)

                    Print_Utils.success_message(
                        f"Found coordinates from photo: ( {coords[0]}, {coords[1]} )"
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

                coords = (x_coord, y_coord)

            # TODO Check if the coordinates are near an existing location

            # Get the name of the new location
            location_name: str = Print_Utils.input_rule("Enter a location name")

            # Commit the new merchant location
            session.add(
                Merchant_Location(
                    merchant_id=target_merchant.id,
                    name=location_name,
                    x_coord=coords[0],
                    y_coord=coords[1],
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

            # Prompt the user to select a merchant and set it as the target account
            target_merchant: Merchant = merchant_list[
                Print_Utils.input_from_options(
                    [merchant.name for merchant in merchant_list], input=merchant_name
                )
            ]

            # Get a list of merchants from the database
            location_list: List[str] = session.query(Merchant_Location).where(
                Merchant_Location.merchant_id == target_merchant.id
            )

            # Prompt the user to select a merchant and set it as the target account
            target_merchant_location: Merchant = location_list[
                Print_Utils.input_from_options(
                    [merchant_location.name for merchant_location in location_list],
                    input=merchant_location_name,
                )
            ]

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
            target_merchant: Merchant = merchant_list[
                Print_Utils.input_from_options(
                    [merchant.name for merchant in merchant_list], input=merchant_name
                )
            ]

            # Get a list of merchants from the database
            location_list: List[str] = session.query(Merchant_Location).where(
                Merchant_Location.merchant_id == target_merchant.id
            )

            # Prompt the user to select a merchant and set it as the target account
            target_merchant_location: Merchant = location_list[
                Print_Utils.input_from_options(
                    [merchant_location.name for merchant_location in location_list],
                    input=merchant_location_name,
                )
            ]

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
