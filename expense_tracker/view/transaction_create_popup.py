# expense_tracker/view/transaction_create_popup.py


from enum import Enum

from copy import copy

from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets.selection_list import Selection

from expense_tracker.presenter.transaction import Transaction
from expense_tracker.presenter.tag import Tag

from expense_tracker.view.toggle_input_popup import Toggle_Input_Popup
from expense_tracker.view.create_popup import Create_Popup
from expense_tracker.view.exptrack_data_table import Exptrack_Data_Table

from typing import Optional


class Transaction_Create_Popup(Create_Popup):
    """
    Transaction specific create popup
    """

    def __init__(
        self,
        parent_table: Exptrack_Data_Table,
        instructions: str = "Create",
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        parent_column_list: list[tuple[Enum, any]] = copy(parent_table.column_list)
        parent_column_list.pop(1)

        super().__init__(
            parent_table,
            instructions,
            modified_column_list=parent_column_list,
            name=name,
            id=id,
            classes=classes,
        )

    def get_input_popup(self, column: str, id: int) -> Optional[ModalScreen]:
        if column == Transaction.Column.TAGS:
            return Toggle_Input_Popup(
                (Selection(tag[1], tag[0], False) for tag in Tag.get_all()),
                instructions="Select tags",
            )

        return super().get_input_popup(column, id)
