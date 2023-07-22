# expense_tracker/cli/cli_utils.py

from expense_tracker.constants import GeneralConstants
from expense_tracker.config_manager import ConfigManager

from expense_tracker.cli import console

from pathlib import Path

import os

import re

from typing import Optional, List, Any, Tuple

from difflib import SequenceMatcher

from datetime import datetime, timedelta

from rich import box
from rich.table import Column, Table


class Print_Tables:
    """
    Returns predefined tables for each database.
    """

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
        console.print(f"\n{message}\n", style="Green")

    @staticmethod
    def error_message(message: str, error_message: Optional[str] = None) -> None:
        """
        Print a message with error formatting.
        """
        console.print(f"\n{message}\n", style="Red")

        if error_message:
            console.print(f"Failed with: {str(error_message)}\n", style="Red")

    @staticmethod
    def input_rule(input_message) -> str:
        """
        Gets input from the user and prints a rule after it.
        """

        console.print()
        input: str = console.input(f"{input_message} >>> ")
        console.rule(style="white")
        return input

    def input_date(
        prompt_message: str = "Enter a date (mm/dd/yyyy)",
        input: Optional[str] = None,
    ) -> datetime:
        """
        Prompt the user to enter a datetime
        """

        # Set the user input based on the initial input option
        user_input: str
        if input:
            user_input = input
        else:
            user_input = Print_Utils.input_rule(prompt_message)

        selected_date: datetime

        while True:
            # If the user input is equal to today return today as a datetime
            if user_input == "today":
                selected_date = datetime.today()
                break

            # If the user input is equal to yesterday return yesterday as a datetime
            if user_input == "yesterday":
                selected_date = datetime.today() - timedelta(days=1)
                break

            # If the user input can be converted to a date then return it as a datetime
            try:
                selected_date = datetime.strptime(user_input, "%m/%d/%Y")
                break
            except ValueError:
                pass

            # Prompt the user to input a new string and restart the process
            Print_Utils.error_message(f"Cannot convert '{user_input}' to a date.")
            user_input = Print_Utils.input_rule(prompt_message)

        # Print the selected date and return
        Print_Utils.success_message(
            f"Selected '{selected_date.strftime('%A %B %-d %Y')}'."
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
                "Press enter to select the highlighted option, input a number to select an option choice, or input a string to search for another option."
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
                    console.print(f"(default) --> {option}", style="cyan")
                    console.print()
                else:
                    console.print(f" -->  {option}", style="cyan")

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
    def input_file_path(prompt_message: str) -> Path:
        """
        Get user input and validate it as an existing path.
        """

        input: str = Print_Utils.input_rule(prompt_message)

        input = re.sub("['\"]", "", input)

        if not os.path.exists(input) or not os.path.isfile(input):
            raise ValueError(f"'{input}' is not a valid path to a file.")

        return Path(input)

    @staticmethod
    def input_float(prompt_message: str) -> float:
        """
        Get user input and validate it as a float.
        """

        input: str = Print_Utils.input_rule(prompt_message)
        return float(input)
