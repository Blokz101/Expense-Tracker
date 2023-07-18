# expense_tracker/cli/cli_utils.py

from expense_tracker.config_manager import ConfigManager

from expense_tracker.cli import console

from pathlib import Path

import os

import re

from typing import Optional, List

from difflib import SequenceMatcher

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
        console.rule()
        return input

    @staticmethod
    def input_from_options(
        options_list: List[str],
        prompt_message: Optional[str] = None,
        input: Optional[str] = None,
    ) -> int:
        """
        Prompts the user to pick an option from a list of options. Returns the index of the option picked
        """

        # Raise an exception if there is no initial input option
        if not (prompt_message or input):
            raise ValueError("Argument 'prompt_message' or 'input' must be given")

        # If there are no options in options list, raise an exception
        if len(options_list) == 0:
            raise ValueError("'options_list' has no options")

        # Set the user input based on the initial input option
        user_input: str
        if prompt_message:
            user_input = Print_Utils.input_rule(prompt_message)
        elif input:
            user_input = input

        selected_option: tuple

        while True:
            # Sort the list of strings by similarity to the user input
            sorted_options: List[tuple] = Print_Utils.similar_strings(
                user_input, options_list
            )

            # Print the help and first five sorted options
            console.print(
                f"\nPress enter to select the first option, enter a number to select another option, or type a phrase to search for another option. Options sorted by '{user_input}':\n"
            )
            for index, option in enumerate(
                sorted_options[: ConfigManager().get_number_of_options()]
            ):
                if index == 0:
                    console.print(f"{' -->': <7}{option[1]}", style="cyan")
                else:
                    console.print(f"{f'[{index}]': <6}{option[1]}")

            # Prompt the user to select an option
            user_input = Print_Utils.input_rule("Please select an option")

            # If the user selects 0, return the set of the selected option and break
            if not user_input:
                selected_option = sorted_options[0]
                break

            # If the user selects another number, set the index of the selected option and break
            if str.isdigit(user_input):
                index: int = int(user_input)
                if index >= 0 and index <= len(sorted_options) - 1:
                    selected_option = sorted_options[index]
                    break

        # Print the selected option and return
        console.print(f"Selected '{selected_option[1]}'\n")
        return selected_option[2]

    @staticmethod
    def similar_strings(target_string: str, str_list: List[str]) -> List[tuple]:
        """
        Compare a string to a list of strings and return tuples with floats that describe how similar the two strings are and contain the original index.
        """

        result_list: List[tuple] = []

        # Calculate the similarity to the target string, save the original list index as well
        for index, string in enumerate(str_list):
            result_list.append(
                (SequenceMatcher(None, target_string, string).ratio(), string, index)
            )

        # Sort the list by similarity and return
        return sorted(result_list, reverse=True)

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
