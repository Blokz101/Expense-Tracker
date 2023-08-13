# expense_tracker/view/tag_table.py


from enum import Enum
from typing import Any, Optional
from textual.screen import ModalScreen

from expense_tracker.presenter.tag import Tag

from expense_tracker.view.exptrack_data_table import Exptrack_Data_Table
from expense_tracker.view.text_input_popup import Text_Input_Popup


class Tag_Table(Exptrack_Data_Table):
    """
    TODO Fill this in
    """

    COLUMN_LIST: list[tuple[str, Enum]] = [
        ("ID", Tag.Column.ID),
        ("Name", Tag.Column.NAME),
        ("Instance", Tag.Column.INSTANCE_TAG),
    ]

    def __init__(
        self,
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        super().__init__(Tag, Tag_Table.COLUMN_LIST, name=name, id=id, classes=classes)

    def get_input_popup(self, column: str, id: int) -> Optional[ModalScreen]:
        """
        TODO Fill this in
        """

        if column == Tag.Column.NAME:
            return Text_Input_Popup(instructions="Input a name")

        return super().get_input_popup(column, id)
