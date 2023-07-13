# expense_tracker/cli/cli_utils.py

from expense_tracker.constants import GeneralConstants

from expense_tracker.cli import console

from expense_tracker.model.merchant import Merchant

from typing import Optional, List

from difflib import SequenceMatcher

from rich import box
from rich.table import Column, Table


class Print_Utils:
    """
    Shortcut for printing status messages in predefined ways.
    """

    @staticmethod
    def success_message(message: str) -> None:
        """
        Print a message with success formating.
        """
        console.print(f"\n{message}\n", style="Green")

    @staticmethod
    def error_message(message: str, error_message: Optional[str] = None) -> None:
        """
        Print a message with error formating.
        """
        console.print(f"\n{message}\n", style="Red")

        if error_message:
            console.print(f"Failed with: {str(error_message)}\n", style="Red")

    @staticmethod
    def merchant_table(merchat_list: List[Merchant]) -> None:
        """
        Print a merchant table.
        """

        table: Table = Table(
            Column("ID", style="bright_black"),
            Column("Name"),
            box=box.SIMPLE,
        )

        for merchant in merchat_list:
            table.add_row(str(merchant.id), merchant.name)

        console.print(table)

    @staticmethod
    def input_from_options(
        options_list: List[str],
        prompt_message: Optional[str] = None,
        input: Optional[str] = None,
    ) -> int:
        """
        Prompts the user to pick an option from a list of options. Returns the index of the option picked
        """

        if not (prompt_message or input):
            raise ValueError("Argument 'prompt_message' or 'input' must be given.")

        user_input: str

        if prompt_message:
            user_input = console.input(f"{prompt_message} >>> ")

        elif input:
            user_input = input

        while True:
            sorted_options: List[tuple] = Print_Utils._similar_strings(
                user_input, options_list
            )

            # Print the options
            console.rule()
            console.print(f"Options sorted by '{user_input}':\n")
            for index, option in enumerate(
                sorted_options[: GeneralConstants.NUMBER_OF_DISPLAY_OPTIONS]
            ):
                console.print(f"{index: <4}{option[1]}")
            console.print()

            user_input = console.input("Please select an option >>> ")

            if not user_input:
                return sorted_options[0][2]

            if str.isdigit(user_input):
                index: int = int(user_input)
                if index >= 0 and index <= len(sorted_options) - 1:
                    return sorted_options[index][2]

    @staticmethod
    def _similar_strings(main_string: str, str_list: List[str]) -> List[tuple]:
        """
        Compare a string to a list of strings and return tuples with floats that describe how similar the two strings are and contain the origional index.
        """

        result_list: List[tuple] = []

        for index, string in enumerate(str_list):
            result_list.append(
                (SequenceMatcher(None, main_string, string).ratio(), string, index)
            )

        return sorted(result_list, reverse=True)
