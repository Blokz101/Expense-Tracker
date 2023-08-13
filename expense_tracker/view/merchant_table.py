# expense_tracker/view/merchant_table.py


from enum import Enum
from typing import Any, Optional
from textual.screen import ModalScreen

from expense_tracker.presenter.merchant import Merchant

from expense_tracker.view.exptrack_data_table import Exptrack_Data_Table
from expense_tracker.view.text_input_popup import Text_Input_Popup


class Merchant_Table(Exptrack_Data_Table):
    """
    TODO Fill this in
    """

    COLUMN_LIST: list[tuple[str, Enum]] = [
        ("ID", Merchant.Column.ID),
        ("Name", Merchant.Column.NAME),
        ("Rule", Merchant.Column.NAMING_RULE),
    ]

    def __init__(
        self,
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        super().__init__(
            Merchant, Merchant_Table.COLUMN_LIST, name=name, id=id, classes=classes
        )

    def get_input_popup(self, column: str, id: int) -> Optional[ModalScreen]:
        """
        TODO Fill this in
        """

        if column == Merchant.Column.NAME:
            return Text_Input_Popup(instructions="Input a name")

        if column == Merchant.Column.NAMING_RULE:
            return Text_Input_Popup(instructions="Input a regular expression")

        return super().get_input_popup(column, id)
