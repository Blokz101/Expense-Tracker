# expense_tracker/view/exptrack_data_table.py

from typing import NamedTuple

from typing import Any, Optional
from textual.coordinate import Coordinate
from textual.message import Message
from textual.widgets import DataTable
from textual.widgets._data_table import CellKey
from textual.events import Click
from textual.screen import ModalScreen


class Exptrack_Data_Table(DataTable):
    """
    Generates data tables from each of the data types.
    """

    class Column_Info(NamedTuple):
        variable_name: str
        display_name: str
        input_popup_factory: Any

    class Table_Info(NamedTuple):
        table_name: str
        display_name: str

    class Edit_Request(Message):
        """
        TODO Fill this in
        """

        def __init__(
            self, table_name: str, id: int, column_name: str, popup: ModalScreen
        ) -> None:
            self.table_name: str = table_name
            self.id: int = id
            self.column_name: str = column_name
            self.popup: ModalScreen = popup
            super().__init__()

    def __init__(
        self,
        column_info_list: list[Column_Info],
        table_name: Table_Info,
        detailed_data_popup_factory=None,
    ) -> None:
        """
        TODO Fill this out
        """
        super().__init__(show_cursor=False, zebra_stripes=True)

        # Set the instance variables
        self.detailed_data_popup_factory = detailed_data_popup_factory
        self.table_name: str = table_name[0]
        self.display_table_name: str = table_name[1]
        self.column_info_list: list[Exptrack_Data_Table.Column_Info] = column_info_list

    def on_mount(self) -> None:
        super().on_mount()

        # Add an id column
        self.add_column("id", key="id")
        for info in self.column_info_list:
            self.add_column(info[1], key=info[0])

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

        # Get the data id and database column id
        key: CellKey = self.coordinate_to_cell_key(Coordinate(row_index, column_index))
        id: int = int(key.row_key.value)
        column_name: str = key.column_key.value

        # Get the popup factory from column info list by id and column name
        popup_factory: Any = None
        try:
            popup_factory = next(
                (info[2] for info in self.column_info_list if info[0] == column_name)
            )
        except:
            pass

        # If there is a popup factory then mount its popup
        if popup_factory:
            self.post_message(
                self.Edit_Request(self.table_name, id, column_name, popup_factory())
            )
