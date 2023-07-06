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
        console.print(f"\n\t{StatusPrint._indent_message(message)}\n", style="Green")

    @staticmethod
    def error(message: str, error_message: Optional[str] = None) -> None:
        """
        Print a message with error formating
        """
        console.print(f"\n\t{StatusPrint._indent_message(message)}\n", style="Red")
        
        if error_message:
            console.print(f"\tFailed with: {str(error_message)}\n", style = "Red")
        
    @staticmethod
    def _indent_message(message: str) -> str:
        """
        Edit a message so it will display as indented in the terminal
        """

        return re.sub("\n", "\n\t", str(message))