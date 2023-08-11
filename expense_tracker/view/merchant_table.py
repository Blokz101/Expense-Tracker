# expense_tracker/view/merchant_table.py

from typing import Optional

from textual.validation import Number, Regex

from textual.widgets.selection_list import Selection

from expense_tracker.view.exptrack_data_table import Exptrack_Data_Table
from expense_tracker.view.text_input_popup import Text_Input_Popup
from expense_tracker.view.options_input_popup import Options_Input_Popup
from expense_tracker.view.toggle_input_popup import Toggle_Input_Popup
from expense_tracker.view.selector import Selector

from expense_tracker.constants import Constants

from expense_tracker.presenter.merchant import Merchant


class Merchant_Table(Exptrack_Data_Table):
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
                Merchant.Column.NAME,
                Text_Input_Popup,
            ),
            Exptrack_Data_Table.Column_Info(
                "Rule",
                Merchant.Column.NAMING_RULE,
                Text_Input_Popup,
            ),
        ]
        super().__init__(
            column_info_list, Merchant.get_all(), name=name, id=id, classes=classes
        )

    def request_popup_args(self, popup_column: any, id: int) -> Optional[list[any]]:
        """
        Returns the arguments that are required to deal with different popup columns.
        """

        if popup_column == Merchant.Column.NAME:
            return ["Input a name"]

        if popup_column == Merchant.Column.NAMING_RULE:
            return ["Input a regular expression"]

        return super().request_popup_args(popup_column)
