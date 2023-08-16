# expense_tracker/view/popup/detailed_data_popup

from textual.app import ComposeResult
from textual.widgets import Static, DataTable
from textual.widgets._data_table import RowKey, ColumnKey, CellKey
from textual.containers import Vertical
from textual.coordinate import Coordinate
from textual.screen import ModalScreen
from textual.events import Click

from expense_tracker.view.table.exptrack_data_table import Exptrack_Data_Table

from typing import Optional


class Detailed_Data_Popup(ModalScreen):
    """
    Popup that displays a detailed table row
    """

    DEFAULT_CSS: str = """
        Detailed_Data_Popup {
            align: center middle;
        }

        Detailed_Data_Popup > Vertical {
            width: 60;
            height: auto;
            background: $surface;
            padding: 1;
        }

        Detailed_Data_Popup > Vertical > DataTable {
            margin-top: 1;
        }
    """

    def __init__(
        self,
        object_id: int,
        parent_table: Exptrack_Data_Table,
        title: str = "Details",
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes)
        self.title: str = title
        self.object_id: int = object_id
        self.parent_table: Exptrack_Data_Table = parent_table

    BINDINGS: list[tuple[str, str, str]] = [
        ("escape", "exit_popup", "Dismiss popup"),
    ]

    def compose(self) -> ComposeResult:
        """
        Composes the display
        """
        self._container: Vertical = Vertical()
        self._title_widget: Static = Static(self.title)
        self._data_table_widget: DataTable = DataTable(show_cursor=False)

        with self._container:
            yield self._title_widget
            yield self._data_table_widget

    def on_mount(self) -> None:
        """
        Called when the widget is mounted.

        Adds the rows and columns.
        """
        # Add columns
        self._data_table_widget.add_column("Detail", key="detail")
        self._data_table_widget.add_column("Value", key="value")

        # Get the data list form the specified presenter
        data_list: list[tuple[str, ...]] = self.parent_table.presenter.get_by_id(
            self.object_id
        )

        # Add rows, the rows and columns are flipped so be careful with naming
        for index, column in enumerate(self.parent_table.column_list):
            self._data_table_widget.add_row(
                column.display_name, data_list[index], key=column.key
            )

    def action_exit_popup(self) -> None:
        """
        Called when the escape key is pressed.

        Returns none and dismisses.
        """

        self.dismiss(None)

    def on_click(self, event: Click) -> None:
        """
        Called when the user clicks a cell.

        Gets the details of the cell clicked and mounts a popup.
        """

        # Get the row and column index from event
        meta: dict[str, any] = event.style.meta
        if not meta:
            return
        row_index: int = meta["row"]
        column_index: int = meta["column"]

        # If the cell does not exist then return
        if row_index == -1:
            return

        # Get the data id and database column id
        key: CellKey = self._data_table_widget.coordinate_to_cell_key(
            Coordinate(row_index, column_index)
        )
        row_key: str = key.row_key.value
        column_key: str = key.column_key.value

        # Get the popup for the column
        popup: ModalScreen = self.get_input_popup(row_key, self.object_id)

        # If there is no popup then return
        if not popup:
            return

        def callback(new_value: Optional[str]) -> None:
            """
            Updates the database and the view with the new value
            """

            # If there is no new value then dont do anything
            if new_value is None:
                return

            # Update the database
            updated_value: str = self.parent_table.presenter.set_value(
                int(self.object_id), row_key, new_value
            )

            # Update self
            self._data_table_widget.update_cell(
                RowKey(row_key),
                ColumnKey(column_key),
                updated_value,
                update_width=True,
            )

            # Update parent table
            self.parent_table.update_cell(
                RowKey(self.object_id),
                ColumnKey(row_key),
                updated_value,
                update_width=True,
            )

        self.app.push_screen(popup, callback)

    def get_input_popup(self, column: str, id: int) -> Optional[ModalScreen]:
        """
        Get the input popup based on the column
        """

        return self.parent_table.get_input_popup(column, id)
