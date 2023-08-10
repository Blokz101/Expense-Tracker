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
        popup: any

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
            args: Optional[list[any]] = None,
        ) -> None:
            self.sender: str = sender
            self.row_key: RowKey = row_key
            self.column_key: ColumnKey = column_key
            self.popup: ModalScreen = popup
            self.args: Optional[list[any]] = args
            super().__init__()

    def __init__(self, column_info_list: list[Column_Info], initial_row_list: list[tuple[int, ...]]) -> None:
        self.column_info_list: list[Exptrack_Data_Table.Column_Info] = column_info_list
        self._initial_row_list: list[tuple[int, ...]] = initial_row_list
        super().__init__(show_cursor=False, zebra_stripes=True)

    def on_mount(self) -> None:
        """
        Called when the widget is mounted.
        
        Adds the columns and initial rows.
        """
        
        # Add an id column and other columns
        self.add_column("id", key="id")
        for info in self.column_info_list:
            self.add_column(info.display_name, key=info.column_variable)
            
        # Add initial rows
        for row in self._initial_row_list:
            self.add_row(*row[0:], key=row[0])

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
        popup: Any = None
        try:
            popup = next(
                (
                    info.popup
                    for info in self.column_info_list
                    if info.column_variable == column_key.value
                )
            )
        except:
            pass

        # If there is a popup factory then mount its popup
        if popup:
            self.post_message(
                self.Edit_Request(
                    self,
                    row_key,
                    column_key,
                    popup,
                    self.request_popup_args(column_key.value, int(row_key.value)),
                )
            )

    def request_popup_args(self, popup_column: any, id: int) -> Optional[list[any]]:
        """
        To be implemented by classes that extend this one.

        Returns the arguments that are required to deal with different popup columns.
        """
        return None
