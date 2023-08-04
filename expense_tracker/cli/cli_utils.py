# expense_tracker/cli/cli_utils.py

from expense_tracker.constants import GeneralConstants
from expense_tracker.config_manager import ConfigManager

from expense_tracker.cli import console

from pathlib import Path

import copy

import re

from typing import Optional, List, Any, Tuple

from difflib import SequenceMatcher

from datetime import datetime, timedelta

from rich import box
from rich.table import Column, Table


class Logic_Utils:
    """
    Logic utility for the command line
    """

    @staticmethod
    def is_something(*obj_list: Any) -> bool:
        """
        Check if an object or list of objects have some value
        """

        for obj in obj_list:
            if obj == None:
                return False

        return True


class Print_Tables:
    """
    Returns predefined tables for each database.
    """

    transaction_table: Table = Table(
        Column("ID", style="bright_black"),
        Column("Reconciled"),
        Column("Description"),
        Column("Merchant"),
        Column("Date"),
        Column("Amount"),
        Column("Tags"),
        box=box.SIMPLE,
    )

    merchant_table: Table = Table(
        Column("ID", style="bright_black"),
        Column("Name"),
        Column("Default Tags"),
        box=box.SIMPLE,
    )

    merchant_location_table: Table = Table(
        Column("ID", style="bright_black"),
        Column("Name"),
        Column("Merchant"),
        Column("X Coord"),
        Column("Y Coord"),
        box=box.SIMPLE,
    )

    tag_table: Table = Table(
        Column("ID", style="bright_black"),
        Column("Name"),
        box=box.SIMPLE,
    )

    account_table: Table = Table(
        Column("ID", style="bright_black"),
        Column("Name"),
        box=box.SIMPLE,
    )


class Print_Utils:
    """
    Shortcut for printing status messages in predefined ways.
    """

    @staticmethod
    def success_message(message: str) -> None:
        """
        Print a message with success formatting.
        """
        console.print(message, style="Green")

    @staticmethod
    def error_message(message: str, error_message: Optional[str] = None) -> None:
        """
        Print a message with error formatting.
        """
        console.print(message, style="Red")

        if error_message:
            console.print(f"Failed with: {str(error_message)}", style="Red")

    @staticmethod
    def extract_message(message: str, extracted: str) -> None:
        """
        Print a extracted message and what was extracted.
        """

        console.print(message)
        console.print(f" + {extracted}", style=GeneralConstants.HIGHLIGHTED_STYLE)

    @staticmethod
    def input_rule(prompt_message, default: str = None) -> str:
        """
        Gets input from the user and prints a rule after it.
        """

        console.print()

        # If the default is set then print it
        if default:
            console.print("Press enter to select default or input another string.\n")
            console.print(
                f"(default) --> {default}\n", style=GeneralConstants.SELECTED_STYLE
            )

        # Get user input
        input: str = console.input(f"{prompt_message} >>> ")
        console.rule(style="white")

        # Return default if default is set and user pressed enter, if not return the user input
        if default and input == "":
            return default
        else:
            return input

    def input_date(
        prompt_message: str,
        default: Optional[datetime] = None,
    ) -> datetime:
        """
        Prompt the user to enter a datetime
        """

        selected_date: datetime

        while True:
            # If the default is set then print it and instructions
            if default:
                console.print(
                    "\nPress enter to select default, input 'today' for today, 'yesterday' for yesterday, or input a date in mm/dd/yyyy format.\n"
                )
                console.print(
                    f"(default) --> {datetime.strftime(default, GeneralConstants.DATE_FORMAT)}",
                    style=GeneralConstants.SELECTED_STYLE,
                )

            # If the default is not set then print the instructions
            else:
                console.print(
                    "\nEnter 'today' for today, 'yesterday' for yesterday, or input a date in mm/dd/yyyy format."
                )

            # Get user input
            user_input: str = Print_Utils.input_rule(prompt_message)

            # Check for special cases
            if default and user_input == "":
                selected_date = default
                break

            if user_input == "today":
                selected_date = datetime.today()
                break

            if user_input == "yesterday":
                selected_date = datetime.today() - timedelta(days=1)
                break

            # Attempt to convert user input to date, print message if it fails
            try:
                selected_date = datetime.strptime(user_input, "%m/%d/%Y")
                break
            except ValueError:
                Print_Utils.error_message(
                    f"Could not convert '{user_input}' into date."
                )

        # Print the selected date and return it
        Print_Utils.success_message(
            f"Selected {datetime.strftime(selected_date, GeneralConstants.DATE_FORMAT)}"
        )
        return selected_date

    @staticmethod
    def input_from_options(
        options_list: List[Any],
        key,
        prompt_message: Optional[str] = "Select an option",
        first_input: Optional[str] = "",
        default: Optional[Any] = None,
    ) -> Any:
        """
        Prompts the user to select an option from a list of options.
        """

        # If there are no options in options list, raise an exception
        if len(options_list) == 0:
            raise ValueError("'options_list' has no options")

        user_input: str = first_input
        selected_option: Any
        prompt_default: bool = not default == None

        while True:
            # Sort the options list based on what the user input
            sorted_options_list: List[Tuple] = Print_Utils._search_options_list(
                options_list, key, user_input
            )

            # Print instructions
            console.print(
                "\nPress enter to select the highlighted option, input a number to select an option choice, or input a string to search for another option."
            )
            console.print()

            # If there is a default, display it the first time
            if prompt_default:
                prompt_default = False
                sorted_options_list = [default] + sorted_options_list

                Print_Utils._print_options(
                    list(key(option) for option in sorted_options_list),
                    limit=ConfigManager().get_number_of_options(),
                    default=True,
                )

            # If there is no default, display the list
            else:
                Print_Utils._print_options(
                    list(key(option) for option in sorted_options_list),
                    limit=ConfigManager().get_number_of_options(),
                )

            # Get the user input
            user_input = Print_Utils.input_rule(prompt_message)

            # If the user pressed enter, return the first option
            if user_input == "":
                selected_option = sorted_options_list[0]
                break

            # If the user entered a number, return their choice
            if (
                user_input.isdigit()
                and int(user_input) > 1
                and int(user_input) <= ConfigManager().get_number_of_options()
            ):
                selected_option = sorted_options_list[int(user_input) - 1]
                break

        # Print confirmation and return
        Print_Utils.success_message(f"Selected {key(selected_option)}.")
        return selected_option

    @staticmethod
    def _print_options(
        option_name_list: List[str], default: bool = False, limit: Optional[int] = None
    ) -> None:
        """
        Prints a list of options in a user friendly format.
        """

        for index, option in enumerate(option_name_list):
            # If the limit has been reached print a footer and exit
            if limit and index >= limit:
                console.print(
                    f"and {len(option_name_list) - limit} more...", style="bright_black"
                )
                break

            # If this is the first option, format it differently
            if index == 0:
                if default:
                    console.print(
                        f"(default) --> {option}", style=GeneralConstants.SELECTED_STYLE
                    )
                    console.print()
                else:
                    console.print(
                        f" -->  {option}", style=GeneralConstants.SELECTED_STYLE
                    )

            # Print the option in standard format
            else:
                option_display: str = f"[{index + 1}]"
                console.print(f"{option_display: <6}{option}")

    @staticmethod
    def _search_options_list(
        options_list: List[Any], key, search_input: str
    ) -> List[Any]:
        """
        Sort a list of options based on how close it is to a given search_input.
        """

        # Create a list with each option and a value that relates the similarity of the option key to the search_input
        compared_options_list: List[Tuple[float, Any]] = []
        for option in options_list:
            compared_option: Tuple[float, Any] = (
                option,
                SequenceMatcher(
                    None, key(option).lower(), search_input.lower()
                ).ratio(),
            )
            compared_options_list.append(compared_option)

        # Sort the list and return
        compared_options_list.sort(key=lambda x: x[1], reverse=True)
        return list(option[0] for option in compared_options_list)

    @staticmethod
    def input_file_path(prompt_message: str, default: Optional[Path] = None) -> Path:
        """
        Get user input and validate it as an existing path.
        """

        selected_path: Path

        while True:
            # If the default is set then print it and the instructions
            if default:
                console.print("\nPress enter to select default or enter a path.")
                console.print(
                    f"(default) --> {str(default)}",
                    style=GeneralConstants.SELECTED_STYLE,
                )

            # If the default is not set then print the instructions
            else:
                console.print("\nEnter a path.")

            # Get the user input and clean it
            user_input: str = Print_Utils.input_rule(prompt_message)
            user_input = re.sub("['\"]", "", user_input)
            if user_input[len(user_input) - 1] == " ":
                user_input = user_input[:-1]

            # Check for special cases
            if default and user_input == "":
                selected_path = default
                break

            # Attempt to convert user input to date, print message if it fails
            try:
                selected_path = Path(user_input)
                break
            except ValueError:
                Print_Utils.error_message(
                    f"Could not convert '{user_input}' into path."
                )

        # Print the selected path and return it
        Print_Utils.success_message(f"Selected {selected_path}.")
        return selected_path

    @staticmethod
    def input_float(prompt_message: str, default: float = None) -> float:
        """
        Get user input and validate it as a float.
        """

        selected_path: Path

        while True:
            # If the default is set then print it and the instructions
            if default:
                console.print("\nPress enter to select default or enter a float.\n")
                console.print(
                    f"(default) --> {str(default)}",
                    style=GeneralConstants.SELECTED_STYLE,
                )

            # If the default is not set then print the instructions
            else:
                console.print("\nEnter a float.")

            # Get the user input
            user_input: str = Print_Utils.input_rule(prompt_message)

            # Check for special cases
            if default and user_input == "":
                selected_path = default
                break

            # Attempt to convert user input to date, print message if it fails
            try:
                selected_path = float(user_input)
                break
            except ValueError:
                Print_Utils.error_message(
                    f"Could not convert '{user_input}' into float."
                )

        # Print the selected path and return it
        Print_Utils.success_message(f"Selected {selected_path}.")
        return selected_path

    @staticmethod
    def input_from_toggle_list(
        options_list: List[Any],
        key,
        prompt_message: str,
        initial_selected_list: List[Any] = [],
    ) -> List[Any]:
        """
        Prompts the user to select options from a toggle list
        """

        selected_options_list: List[Any] = copy.copy(initial_selected_list)

        while True:
            # Print the instructions and options
            console.print(
                "\nToggle the options by entering their corresponding integer or press enter to submit.\n"
            )
            Print_Utils._print_toggle_options(
                list(key(option) for option in options_list),
                list(key(option) for option in selected_options_list),
            )

            # Get the user input
            user_input: str = Print_Utils.input_rule(prompt_message)

            # If the user didn't input anything then break
            if user_input == "":
                break

            # Try to find the target option, if unable print an error and continue
            toggle_option: Any
            try:
                toggle_option = options_list[int(user_input) - 1]
            except:
                Print_Utils.error_message(f"'{user_input}' is not an option.")
                continue

            # Toggle the option
            if toggle_option in selected_options_list:
                selected_options_list.remove(toggle_option)
            else:
                selected_options_list.append(toggle_option)

        # Print confirmation and return
        if len(selected_options_list) == 0:
            Print_Utils.success_message("Selected no options.")
        else:
            Print_Utils.success_message(
                f"Selected {', '.join(list(key(option) for option in selected_options_list))}."
            )
        return selected_options_list

    @staticmethod
    def _print_toggle_options(
        option_name_list: List[str], selected_option_name_list: List[int]
    ) -> None:
        """
        Prints options in a list displaying them differently if they have been selected
        """

        for index, option in enumerate(option_name_list):
            if option in selected_option_name_list:
                option_display: str = f"[{index + 1} X ]"
                console.print(
                    f"{option_display: <8}{option}",
                    style=GeneralConstants.SELECTED_STYLE,
                )

            else:
                option_display: str = f"[{index + 1}   ]"
                console.print(f"{option_display: <8}{option}", style="bright_black")
