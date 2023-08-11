# expense_tracker/view/tag_table.py

from typing import Optional

from textual.validation import Number, Regex

from expense_tracker.view.exptrack_data_table import Exptrack_Data_Table
from expense_tracker.view.text_input_popup import Text_Input_Popup

from expense_tracker.presenter.tag import Tag


class Tag_Table(Exptrack_Data_Table):
    """
    Table that displays and allows editing of tags.
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
                Tag.Column.NAME,
                Text_Input_Popup,
            ),
            Exptrack_Data_Table.Column_Info(
                "Instance Tag",
                Tag.Column.INSTANCE_TAG,
                None,
            ),
        ]
        super().__init__(
            column_info_list, Tag.get_all(), name=name, id=id, classes=classes
        )

    def request_popup_args(self, popup_column: any, id: int) -> Optional[list[any]]:
        """
        Returns the arguments that are required to deal with different popup columns.
        """

        if popup_column == Tag.Column.NAME:
            return ["Input a name"]

        return super().request_popup_args(popup_column)
