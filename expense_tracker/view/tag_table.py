# expense_tracker/view/tag_table.py


from enum import Enum
from typing import Any, Optional
from textual.screen import ModalScreen

from expense_tracker.presenter.tag import Tag

from expense_tracker.view.exptrack_data_table import Exptrack_Data_Table
from expense_tracker.view.text_input_popup import Text_Input_Popup
from expense_tracker.view.detailed_data_popup import Detailed_Data_Popup
from expense_tracker.view.switch_input_popup import Switch_Input_Popup
from expense_tracker.view.create_popup import Create_Popup


class Tag_Table(Exptrack_Data_Table):
    """
    Table of tags
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

    def action_create(self) -> None:
        """
        Called when c is pressed.
        """

        self.app.push_screen(Create_Popup(self))

    def action_expand(self) -> None:
        """
        Show a detailed data popup
        """

        self.app.push_screen(
            Detailed_Data_Popup(
                self.coordinate_to_cell_key(self.cursor_coordinate).row_key.value, self
            )
        )

    def action_delete(self) -> None:
        """
        Called when d is pressed.
        """

        return

    def get_input_popup(self, column: str, id: int) -> Optional[ModalScreen]:
        """
        Get the input popup based on the column
        """

        if column == Tag.Column.NAME:
            return Text_Input_Popup(instructions="Input a name")

        if column == Tag.Column.INSTANCE_TAG:
            return Switch_Input_Popup(instructions="Is this tag an instance tag")

        return super().get_input_popup(column, id)
