# expense_tracker/view/table/merchant_table.py


from enum import Enum
from typing import Optional
from textual.screen import ModalScreen
from textual.widgets.selection_list import Selection
from textual.validation import Function

import re

from expense_tracker.presenter.merchant import Merchant
from expense_tracker.presenter.tag import Tag

from expense_tracker.view.table.exptrack_data_table import Exptrack_Data_Table
from expense_tracker.view.popup.text_input_popup import Text_Input_Popup
from expense_tracker.view.popup.detailed_data_popup import Detailed_Data_Popup
from expense_tracker.view.popup.create_popup import Create_Popup
from expense_tracker.view.popup.toggle_input_popup import Toggle_Input_Popup


class Merchant_Table(Exptrack_Data_Table):
    """
    Table of merchants
    """

    COLUMN_LIST: list[tuple[str, Enum]] = [
        ("ID", Merchant.Column.ID),
        ("Name", Merchant.Column.NAME),
        ("Rule", Merchant.Column.NAMING_RULE),
        ("Default Tags", Merchant.Column.DEFAULT_TAGS),
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

        if column == Merchant.Column.NAME:
            return Text_Input_Popup(instructions="Input a name")

        if column == Merchant.Column.NAMING_RULE:
            return Text_Input_Popup(
                instructions="Input a regular expression",
                validators=[
                    Function(
                        Merchant_Table._check_regex,
                        failure_description="Regular expression is not valid",
                    )
                ],
            )

        if column == Merchant.Column.DEFAULT_TAGS:
            default_tag_list: list[tuple[int, ...]] = (
                Tag.get_tags_for_merchant_default(id) if id else Tag.get_all()
            )
            selected_tag_id_list: list[int] = list(tag[0] for tag in default_tag_list)

            tag_list: list[tuple[int, ...]] = []

            for tag in Tag.get_all():
                tag_list.append(
                    Selection(tag[1], tag[0], tag[0] in selected_tag_id_list)
                )

            return Toggle_Input_Popup(tag_list, instructions="Select tags")

        return super().get_input_popup(column, id)

    @staticmethod
    def _check_regex(regex: str) -> bool:
        """
        Checks if a regular expression is valid
        """
        try:
            re.compile(regex)
            return True
        except re.error:
            return False
