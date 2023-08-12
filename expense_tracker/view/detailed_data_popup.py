# expense_tracker/view/detailed_data_popup

from textual.app import ComposeResult
from textual.widgets import Static, DataTable
from textual.widgets._data_table import RowKey, ColumnKey, CellKey
from textual.containers import VerticalScroll
from textual.coordinate import Coordinate
from textual.screen import ModalScreen
from textual.events import Click

from expense_tracker.view.table_info import Table_Info, Column_Info

from typing import Optional


class Detailed_Data_Popup(ModalScreen):
    """
    Popup that displays a detailed table row
    """

    def __init__(
        self,
        object_id: int,
        table_info: Table_Info,
        title: str = "Details",
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes)
        self._title = title
        self._object_id: int = object_id
        self._table_info: Table_Info = table_info

    BINDINGS: list[tuple[str, str, str]] = [
        ("escape", "exit_popup", "Dismiss popup"),
    ]

    def compose(self) -> ComposeResult:
        """
        Composes the display
        """
        self._container: VerticalScroll = VerticalScroll()
        self._instructions_widget: Static = Static(self._title)
        self._data_table_widget: DataTable = DataTable(show_cursor=False)

        with self._container:
            yield self._instructions_widget
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
        data_list: list[tuple[int, ...]] = self._table_info.presenter.get_by_id(
            self._object_id
        )

        # Add rows, the rows and columns are flipped so be careful with naming
        for index, column in enumerate(self._table_info.column_list):
            self._data_table_widget.add_row(
                column.display_name, data_list[index], key=column.column_variable
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
        row_key: RowKey = key.row_key
        column_key: ColumnKey = key.column_key

        # Get the popup factory from column info list by id and column name
        column: Column_Info
        try:
            column = next(
                (
                    info
                    for info in self._table_info.column_list
                    if info.column_variable == row_key.value
                )
            )
        except:
            return

        if column.popup_factory is None:
            return

        def update_view_and_model(new_value: Optional[str]) -> None:
            """
            Updates the database and the view with the new value
            """

            if new_value is None:
                return

            updated_value: str = self._table_info.presenter.set_value(
                int(self._object_id), row_key.value, new_value
            )
            self._data_table_widget.update_cell(
                row_key,
                column_key,
                updated_value,
                update_width=True,
            )

        self.app.push_screen(
            column.popup_factory(self._object_id), update_view_and_model
        )
