# expense_tracker/view/exptrack_data_table.py

from typing import NamedTuple

from typing import Any, Optional
from textual.coordinate import Coordinate
from textual.message import Message
from textual.widgets import DataTable
from textual.widgets._data_table import CellKey
from textual.events import Click
from textual.screen import ModalScreen
from textual.widgets._data_table import RowKey, ColumnKey


class Exptrack_Data_Table(DataTable):
    """
    Generates data tables from each of the data types.
    """

    class Column_Info(NamedTuple):
        display_name: str
        column_variable: int
        input_popup_factory: Any

    class Edit_Request(Message):
        """
        Message to request a database edit
        """

        def __init__(
            self,
            sender: DataTable,
            row_key: RowKey,
            column_key: ColumnKey,
            popup: ModalScreen,
        ) -> None:
            self.sender: str = sender
            self.row_key: RowKey = row_key
            self.column_key: ColumnKey = column_key
            self.popup: ModalScreen = popup
            super().__init__()

    def __init__(
        self,
        column_info_list: list[Column_Info],
        detailed_data_popup_factory=None,
    ) -> None:
        # Set the instance variables
        self.detailed_data_popup_factory = detailed_data_popup_factory
        self.column_info_list: list[Exptrack_Data_Table.Column_Info] = column_info_list

        super().__init__(show_cursor=False, zebra_stripes=True)

    def on_mount(self) -> None:
        super().on_mount()

        # Add an id column
        self.add_column("id", key="id")
        for info in self.column_info_list:
            self.add_column(info.display_name, key=info.column_variable)

    def on_click(self, event: Click) -> None:
        """
        Called when the user clicks a cell.

        Gets the details of the cell clicked and mounts a popup.
        """

        # Get the row and column index from event
        meta: dict[str, Any] = event.style.meta
        if not meta:
            return
        row_index: int = meta["row"]
        column_index: int = meta["column"]

        # If the cell does not exist then return
        if row_index == -1:
            return

        # Get the data id and database column id
        key: CellKey = self.coordinate_to_cell_key(Coordinate(row_index, column_index))
        row_key: RowKey = key.row_key
        column_key: ColumnKey = key.column_key

        # Get the popup factory from column info list by id and column name
        popup_factory: Any = None
        try:
            popup_factory = next(
                (
                    info.input_popup_factory
                    for info in self.column_info_list
                    if info.column_variable == column_key.value
                )
            )
        except:
            pass

        # If there is a popup factory then mount its popup
        if popup_factory:
            self.post_message(
                self.Edit_Request(self, row_key, column_key, popup_factory())
            )
