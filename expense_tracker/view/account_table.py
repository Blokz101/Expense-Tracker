# expense_tracker/view/account_table.py

from enum import Enum
from typing import Optional
from textual.screen import ModalScreen
from textual.validation import Regex

from expense_tracker.presenter.account import Account

from expense_tracker.view.exptrack_data_table import Exptrack_Data_Table
from expense_tracker.view.text_input_popup import Text_Input_Popup


class Account_Table(Exptrack_Data_Table):
    """
    TODO Fill this in
    """

    COLUMN_LIST: list[tuple[str, Enum]] = [
        ("ID", Account.Column.ID),
        ("Name", Account.Column.NAME),
        ("Description Index", Account.Column.DESCRIPTION_COLUMN_INDEX),
        ("Amount Index", Account.Column.AMOUNT_COLUMN_INDEX),
        ("Date Index", Account.Column.DATE_COLUMN_INDEX),
    ]

    def __init__(
        self,
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        super().__init__(
            Account, Account_Table.COLUMN_LIST, name=name, id=id, classes=classes
        )

    def get_input_popup(self, column: str, id: int) -> Optional[ModalScreen]:
        """
        TODO Fill this in
        """

        if column == Account.Column.NAME:
            return Text_Input_Popup(instructions="Input a name")

        if column == Account.Column.DESCRIPTION_COLUMN_INDEX:
            return Text_Input_Popup(
                instructions="Input an index for the description column on statement",
                validators=[
                    Regex("\d+", failure_description="Input must be a positive integer")
                ],
            )

        if column == Account.Column.AMOUNT_COLUMN_INDEX:
            return Text_Input_Popup(
                instructions="Input an index for the amount column on statement",
                validators=[
                    Regex("\d+", failure_description="Input must be a positive integer")
                ],
            )

        if column == Account.Column.DATE_COLUMN_INDEX:
            return Text_Input_Popup(
                instructions="Input an index for the date column on statement",
                validators=[
                    Regex("\d+", failure_description="Input must be a positive integer")
                ],
            )

        return super().get_input_popup(column, id)
