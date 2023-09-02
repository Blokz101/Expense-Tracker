# expense_tracker/view/popup/merchant_create_popup.py

from typing import Optional

from textual.screen import ModalScreen
from textual.widgets.selection_list import Selection

from expense_tracker.presenter.merchant import Merchant
from expense_tracker.presenter.tag import Tag

from expense_tracker.view.popup.create_popup import Create_Popup
from expense_tracker.view.popup.toggle_input_popup import Toggle_Input_Popup


class Merchant_Create_Popup(Create_Popup):
    """
    TODO Fill this in later
    """

    def get_input_popup(self, column: str, id: int) -> Optional[ModalScreen]:
        """
        Gets the input popup to use for each column
        """
        if column == Merchant.Column.DEFAULT_TAGS:
            # If the tags are at None or their default value, then convert them to an empty list for ease of processing
            selected_tag_id_list: list[int] = self.values[
                Merchant.Column.DEFAULT_TAGS
            ].value
            if not selected_tag_id_list:
                selected_tag_id_list = []

            # Convert tags into selection objects for the selector widget in Toggle_Input_Popup
            tag_list: list[tuple[str, ...]] = []
            for tag in Tag.get_all():
                tag_list.append(
                    Selection(tag[1], tag[0], tag[0] in selected_tag_id_list)
                )

            return Toggle_Input_Popup(tag_list, instructions="Select tags")

        return super().get_input_popup(column, id)
