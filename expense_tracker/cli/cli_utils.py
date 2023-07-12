# expense_tracker/cli/cli_utils.py

from expense_tracker.cli import console

from expense_tracker.model.merchant import Merchant

from typing import Optional, List, Any, Callable

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
