# expense_tracker/view/merchant_table.py

from typing import Optional

from textual.validation import Number, Regex

from textual.widgets.selection_list import Selection

from expense_tracker.view.exptrack_data_table import Exptrack_Data_Table
from expense_tracker.view.text_input_popup import Text_Input_Popup

from expense_tracker.presenter.account import Account


class Account_Table(Exptrack_Data_Table):
    """
    Table that displays and allows editing of transactions.
    """

    class Edit_Request(Exptrack_Data_Table.Edit_Request):
        pass

    def __init__(
        self,
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        column_info_list: list[Exptrack_Data_Table.Column_Info] = [
            Exptrack_Data_Table.Column_Info(
                "Name",
                Account.Column.NAME,
                Text_Input_Popup,
            ),
            Exptrack_Data_Table.Column_Info(
                "Description Index",
                Account.Column.DESCRIPTION_COLUMN_INDEX,
                Text_Input_Popup,
            ),
            Exptrack_Data_Table.Column_Info(
                "Amount Index",
                Account.Column.AMOUNT_COLUMN_INDEX,
                Text_Input_Popup,
            ),
            Exptrack_Data_Table.Column_Info(
                "Date Index",
                Account.Column.DATE_COLUMN_INDEX,
                Text_Input_Popup,
            ),
        ]
        super().__init__(
            column_info_list, Account.get_all(), name=name, id=id, classes=classes
        )

    def request_popup_args(self, popup_column: any, id: int) -> Optional[list[any]]:
        """
        Returns the arguments that are required to deal with different popup columns.
        """

        if popup_column == Account.Column.NAME:
            return ["Input a name"]

        if popup_column == Account.Column.DESCRIPTION_COLUMN_INDEX:
            return [
                "Input an index for the description column on statement",
                Regex("\d+", failure_description="Input must be a positive integer"),
            ]

        if popup_column == Account.Column.AMOUNT_COLUMN_INDEX:
            return [
                "Input an index for the amount column on statement",
                Regex("\d+", failure_description="Input must be a positive integer"),
            ]

        if popup_column == Account.Column.DATE_COLUMN_INDEX:
            return [
                "Input an index for the date column on statement",
                Regex("\d+", failure_description="Input must be a positive integer"),
            ]

        return super().request_popup_args(popup_column)
