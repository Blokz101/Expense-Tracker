# expense_tracker/view/table/exptrack_data_table.py

from __future__ import annotations

from enum import Enum

from typing import Any, Optional
from textual.coordinate import Coordinate
from textual.widgets import DataTable
from textual.widgets._data_table import CellKey
from textual.events import Click
from textual.widgets._data_table import RowKey, ColumnKey
from textual.screen import ModalScreen

from expense_tracker.presenter.presenter import Presenter


class Exptrack_Data_Table(DataTable):
    """
    Generates data tables from each of the data types.
    """

    BINDINGS: list[tuple[str, str, str]] = [
        ("c", "create", "Create"),
        ("d", "delete", "Delete"),
        ("e", "expand", "Expand"),
    ]

    def __init__(
        self,
        presenter: Presenter,
        column_list: list[tuple[str, Enum]],
        initial_row_list: Optional[list[tuple[int, ...]]] = None,
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        self.presenter: Presenter = presenter
        self.column_list: list[tuple[str, Enum]] = column_list

        self._initial_row_list: list[tuple[int, ...]]
        if initial_row_list:
            self._initial_row_list = initial_row_list
        else:
            self._initial_row_list = self.presenter.get_all()

        super().__init__(
            zebra_stripes=True,
            name=name,
            id=id,
            classes=classes,
        )

    def on_mount(self) -> None:
        """
        Called when the widget is mounted.

        Adds the columns and initial rows.
        """
        # Set the cursor type
        self.cursor_type = "row"

        # Add an id column and other columns
        for column in self.column_list:
            self.add_column(column[0], key=column[1])

        # Add initial rows
        for row in self._initial_row_list:
            if len(self.columns) != len(row):
                raise ValueError(
                    f"Table has {len(self.columns)} columns but was given a row with {len(row)} values."
                )
            self.add_row(*row[0:], key=row[0])

    def action_create(self) -> None:
        """
        Called when c is pressed.
        """

        return

    def action_expand(self) -> None:
        """
        Called when e is pressed.
        """

        return

    def action_delete(self) -> None:
        """
        Called when d is pressed.
        """

        return

    def on_click(self, event: Click) -> None:
        """
        Called when the user clicks a cell.
        """

        # If the shift key was not held down then return
        if not event.shift:
            return

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
        row_key: str = key.row_key.value
        column_key: str = key.column_key.value

        # Get the popup if it exists
        popup: ModalScreen = self.get_input_popup(column_key, int(row_key))

        # If there is no popup then return
        if not popup:
            return

        def callback(new_value: Optional[any]) -> None:
            """
            Updates the database and the view with the new value
            """

            # If there is no new value then return
            if new_value is None:
                return

            # Update the database
            updated_value: str = self.presenter.set_value(
                int(row_key), column_key, new_value
            )

            # Update self
            self.update_cell(
                RowKey(row_key),
                ColumnKey(column_key),
                updated_value,
                update_width=True,
            )

        self.app.push_screen(popup, callback)

    def get_input_popup(self, column: str, id: int) -> Optional[ModalScreen]:
        """
        To be extended
        """

        return None
