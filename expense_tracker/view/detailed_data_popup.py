# expense_tracker/view/detailed_data_popup

from textual.app import ComposeResult
from textual.widgets import Static, DataTable
from textual.containers import VerticalScroll
from textual.screen import ModalScreen

from expense_tracker.view.table_info import Table_Info

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
        self._data_table_widget: DataTable = DataTable()

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
            self._data_table_widget.add_row(column.display_name, data_list[index])

    def action_exit_popup(self) -> None:
        """
        Called when the escape key is pressed.

        Returns none and dismisses.
        """

        self.dismiss(None)
