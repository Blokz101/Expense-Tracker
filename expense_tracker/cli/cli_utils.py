# expense_tracker/cli/cli_utils.py

from expense_tracker.cli import console

from typing import Optional

import re


class StatusPrint:
    """
    Utility printing functions
    """

    @staticmethod
    def success(message: str) -> None:
        """
        Print a message with success formating
        """
        console.print(f"\n{message}\n", style="Green")

    @staticmethod
    def error(message: str, error_message: Optional[str] = None) -> None:
        """
        Print a message with error formating
        """
        console.print(f"\n{message}\n", style="Red")

        if error_message:
            console.print(f"Failed with: {str(error_message)}\n", style="Red")
