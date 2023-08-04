# expense_tracker/cli/cli_transaction_utils.py

from pathlib import Path

from typing import Optional, List, Any

from sqlalchemy.orm import Session

from expense_tracker.config_manager import ConfigManager
from expense_tracker.constants import GeneralConstants, Field_Constant

from expense_tracker.orm import engine
from expense_tracker.orm.merchant import Merchant
from expense_tracker.orm.amount import Amount
from expense_tracker.orm.merchant_location import Merchant_Location
from expense_tracker.orm.transaction import Transaction
from expense_tracker.orm.tag import Tag
from expense_tracker.orm.account import Account
from expense_tracker.orm.budget import Budget
from expense_tracker.orm.month_budget import Month_Budget

from expense_tracker.model.photo_manager import Photo_Manager

from expense_tracker.cli import console
from expense_tracker.cli.cli_utils import Print_Utils, Logic_Utils
from expense_tracker.cli.transaction_field import Transaction_Field

from datetime import datetime

from pathlib import Path


class CLI_Transaction_Utils:
    """
    Util functions for the cli_transactions class
    """

    @staticmethod
    def create_batch_transactions(
        dir_path: Path,
        income: bool = False,
    ) -> None:
        """
        Get the photos in a directory and run the create transaction command for each
        """

        # Get a list of files in the target directory
        photo_list: list[Path] = list(Photo_Manager.files_in_directory(dir_path))

        # Print out the photos that were found
        console.print(f"Using photos found in '{dir_path}' for imports:")
        console.print(
            "\n".join(
                [f"{index+1: <5}{photo.name}" for index, photo in enumerate(photo_list)]
            )
        )
        console.print()

        for photo_path in photo_list:
            CLI_Transaction_Utils.create_transaction(photo_path=photo_path)

    @staticmethod
    def create_transaction(photo_path: Optional[Path] = None) -> None:
        """
        Prompt the user for the information needed to create a transaction and submit it to the database.
        """

        # Check if the photo exists in the archive already
        if photo_path and Photo_Manager.photo_exists_in_archive(
            photo_path.name, ConfigManager().get_photo_archive_path()
        ):
            Print_Utils.error_message("Photo already exists in archive.\nAborting.")
            return

        # Initialize all fields as none, these will be filled out later
        account_field: Transaction_Field = Transaction_Field(
            "Account",
            None,
            Field_Constant.NONE,
            key=lambda x: x.name,
            index=1,
        )
        amount_field: Transaction_Field = Transaction_Field(
            "Amount",
            None,
            Field_Constant.NONE,
            key=lambda x: x,
            index=2,
        )
        date_field: Transaction_Field = Transaction_Field(
            "Date",
            None,
            Field_Constant.NONE,
            key=lambda x: datetime.strftime(x, GeneralConstants.DATE_FORMAT),
            index=3,
        )
        description_field: Transaction_Field = Transaction_Field(
            "Description",
            None,
            Field_Constant.NONE,
            index=4,
        )
        merchant_field: Transaction_Field = Transaction_Field(
            "Merchant",
            None,
            Field_Constant.NONE,
            key=lambda x: x.name,
            index=5,
        )
        tag_list_field: Transaction_Field = Transaction_Field(
            "Tags",
            None,
            Field_Constant.NONE,
            key=lambda x: ", ".join([i.name for i in x]),
            index=6,
        )

        # Get standard defaults
        account_field.set_field_object(
            CLI_Transaction_Utils._get_account_default(), Field_Constant.DEFAULT
        )
        date_field.set_field_object(datetime.today(), Field_Constant.DEFAULT)
        tag_list_field.set_field_object(list(), Field_Constant.DEFAULT)

        # Get the defaults that can be filled with the info from the photo
        if photo_path:
            Print_Utils.success_message(
                f"Importing information from photo at '{photo_path}'."
            )

            date_field.set_field_object(
                CLI_Transaction_Utils._get_date_default(photo_path),
                Field_Constant.PHOTO,
            )
            description_field.set_field_object(
                CLI_Transaction_Utils._get_description_default(photo_path),
                Field_Constant.PHOTO,
            )

            # Try to find a matching merchant, if there is one then set the fields
            merchant_default: Optional[
                Merchant
            ] = CLI_Transaction_Utils._get_merchant_default(photo_path)
            if merchant_default:
                merchant_field.set_field_object(
                    merchant_default,
                    Field_Constant.PHOTO,
                )
                with Session(engine) as session:
                    session.add(merchant_field.field_object)
                    tag_list_field.set_field_object(
                        merchant_field.field_object.default_tags,
                        Field_Constant.MERCHANT,
                    )

        while True:
            # Declare if all the fields are satisfied
            all_fields_satisfied: bool = Logic_Utils.is_something(
                account_field.field_object,
                amount_field.field_object,
                date_field.field_object,
                description_field.field_object,
                merchant_field.field_object,
                tag_list_field.field_object,
            )

            # Print instructions and current fields
            console.print("\nTransaction fields")
            console.print(
                "Press enter to jump to next required field or submit, or enter a number to select what field to modify.\n",
                style=GeneralConstants.LOWLIGHT_STYLE,
            )
            console.print(account_field, style=account_field.style)
            console.print(amount_field, style=amount_field.style)
            console.print(date_field, style=date_field.style)
            console.print(description_field, style=description_field.style)
            console.print(merchant_field, style=merchant_field.style)
            console.print(tag_list_field, style=tag_list_field.style)

            # Print a commit status
            console.print("\nCommit status: ", end="")
            if all_fields_satisfied:
                Print_Utils.success_message("Able to commit")
            else:
                Print_Utils.error_message("Information missing")

            # Get the user input
            user_input: str = Print_Utils.input_rule("Select a field")

            # If the user enters nothing and all fields are filled then break out of the loop
            if user_input == "" and all_fields_satisfied:
                break

            # Find the field that the user indicated and get the new value from the user
            if CLI_Transaction_Utils._selected_field(
                user_input, 1, account_field.field_object
            ):
                account_field.set_field_object(
                    CLI_Transaction_Utils._get_account(
                        default=account_field.field_object
                    ),
                    Field_Constant.USER_INPUT,
                )
                continue

            if CLI_Transaction_Utils._selected_field(
                user_input, 2, amount_field.field_object
            ):
                amount_field.set_field_object(
                    CLI_Transaction_Utils._get_amount(), Field_Constant.USER_INPUT
                )
                continue

            if CLI_Transaction_Utils._selected_field(
                user_input, 3, date_field.field_object
            ):
                date_field.set_field_object(
                    CLI_Transaction_Utils._get_date(default=date_field.field_object),
                    Field_Constant.USER_INPUT,
                )
                continue

            if CLI_Transaction_Utils._selected_field(
                user_input, 4, description_field.field_object
            ):
                description_field.set_field_object(
                    CLI_Transaction_Utils._get_description(
                        default=description_field.field_object
                    ),
                    Field_Constant.USER_INPUT,
                )
                continue

            if CLI_Transaction_Utils._selected_field(
                user_input, 5, merchant_field.field_object
            ):
                merchant_field.set_field_object(
                    CLI_Transaction_Utils._get_merchant(
                        default=merchant_field.field_object
                    ),
                    Field_Constant.USER_INPUT,
                )
                continue

            if CLI_Transaction_Utils._selected_field(
                user_input, 6, tag_list_field.field_object
            ):
                tag_list_field.set_field_object(
                    CLI_Transaction_Utils._get_tags(
                        selected_list=tag_list_field.field_object
                    ),
                    Field_Constant.USER_INPUT,
                )
                continue

            # If the user input does not match any of the fields above then print an error
            if user_input == "":
                Print_Utils.error_message(
                    "Information missing, cannot create transaction.\n"
                )
            else:
                Print_Utils.error_message("Invalid Input.\n")

        # Create and commit the new transaction
        new_transaction: Transaction = CLI_Transaction_Utils._commit_transaction(
            account_field.field_object,
            description_field.field_object,
            merchant_field.field_object,
            date_field.field_object,
            amount_field.field_object,
            tag_list_field.field_object,
            photo_path=photo_path,
        )
        Print_Utils.success_message("Created transaction.")

        # Move the photo
        if photo_path:
            with Session(engine) as session:
                session.add(new_transaction)
                new_path: Path = (
                    ConfigManager().get_photo_archive_path() / photo_path.name
                )
                Photo_Manager.archive_photo(photo_path, new_path)

    @staticmethod
    def _selected_field(user_input: str, option_int: int, value: Optional[Any]) -> bool:
        """
        Helper function for _create_transaction, checks if the user has selected this option
        """
        if user_input.isdigit() and int(user_input) == option_int:
            return True

        if user_input == "" and value == None:
            return True

        return False

    @staticmethod
    def _commit_transaction(
        account: Account,
        description: str,
        merchant: Merchant,
        date: datetime,
        amount: float,
        tag_list: List[Tag],
        photo_path: Optional[Path] = None
    ) -> Transaction:
        """
        Commit a transaction
        """

        with Session(engine) as session:
            # Add the new transaction
            new_transaction: Transaction = Transaction(
                account_id=account.id,
                description=description,
                merchant_id=merchant.id,
                date=date,
                reconciled_status=False,
                receipt_photo_path=(photo_path.name if photo_path else None),
            )
            session.add(new_transaction)
            session.flush()

            # Add the new amount and its tags
            new_amount: Amount = Amount(
                transaction_id=new_transaction.id, amount=amount
            )
            new_amount.tags = tag_list
            session.add(new_amount)

            session.commit()

            return new_transaction

    @staticmethod
    def _get_account_default() -> Account:
        """
        Return the default account specified by the user in the settings
        """

        with Session(engine) as session:
            return session.query(Account).all()[
                ConfigManager().get_default_account_id()
            ]

    @staticmethod
    def _get_account(default: Optional[Account] = None) -> Account:
        """
        Get the account from the user
        """

        with Session(engine) as session:
            return Print_Utils.input_from_options(
                session.query(Account).all(),
                lambda x: x.name,
                "Enter a transaction account",
                default=default,
            )

    @staticmethod
    def _get_date_default(photo_path: Path) -> Optional[datetime]:
        """
        Get the date default from a given photo
        """

        try:
            return Photo_Manager.get_date(photo_path)
        except AttributeError:
            return None

    @staticmethod
    def _get_date(default: Optional[datetime] = None) -> datetime:
        """
        Get the date from the user
        """

        # Set the default as today if one was not provided
        date_default: datetime = default
        if not date_default:
            date_default = datetime.today()

        # Return the the date
        return Print_Utils.input_date(
            "Enter a transaction date",
            default=date_default,
        )

    @staticmethod
    def _get_amount(income=False) -> float:
        """
        Get the amount from the user
        """

        # TODO Add default option here

        if income:
            return Print_Utils.input_float(
                "Enter an [bold]income[/bold] amount",
            )
        else:
            return -1 * Print_Utils.input_float(
                "Enter an [bold]expense[/bold] amount",
            )

    @staticmethod
    def _get_description_default(photo_path: Path) -> Optional[str]:
        """
        Get the description default from a given photo
        """

        try:
            return Photo_Manager.get_description(photo_path)
        except AttributeError:
            return None

    @staticmethod
    def _get_description(default: Optional[str] = None) -> str:
        """
        Get the description from the user
        """

        return Print_Utils.input_rule(
            "Enter a description",
            default=default,
        )

    @staticmethod
    def _get_merchant_default(photo_path: Path) -> Optional[Merchant]:
        """
        Get the merchant default from a given photo
        """

        # Get the photo coords if possible
        photo_coords: tuple[float, float]
        try:
            photo_coords = Photo_Manager.get_coords(photo_path)
        except AttributeError:
            return None

        with Session(engine) as session:
            # Find possible locations, if there is one, return it
            possible_location: Optional[
                Merchant_Location
            ] = Merchant_Location.possible_location(
                photo_coords,
                session.query(Merchant_Location).all(),
                same_location__mile_radius=ConfigManager().get_same_merchant_mile_radius(),
            )
            if possible_location:
                return possible_location.merchant

        return None

    @staticmethod
    def _get_merchant(default: Optional[Merchant] = None) -> Merchant:
        """
        Get the merchant from the user
        """

        with Session(engine) as session:
            return Print_Utils.input_from_options(
                session.query(Merchant).all(),
                lambda x: x.name,
                "Enter a transaction merchant",
                default=default,
            )

    @staticmethod
    def _get_tags(selected_list: List[Tag] = []) -> List[Tag]:
        """
        Get the list of tags from the user
        """

        with Session(engine) as session:
            session.add_all(selected_list)
            return Print_Utils.input_from_toggle_list(
                session.query(Tag).all(),
                lambda x: x.name,
                "Select a tag",
                initial_selected_list=selected_list,
            )
