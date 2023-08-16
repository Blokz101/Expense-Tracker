# expense_tracker/view/table/exptrack_data_table.py

from __future__ import annotations

from enum import Enum

from typing import Union, Iterable

from datetime import datetime

from typing import Any, Optional

from rich.text import Text

from textual.coordinate import Coordinate
from textual.widgets import DataTable
from textual.widgets._data_table import CellKey
from textual.events import Click
from textual.widgets._data_table import RowKey, ColumnKey
from textual.screen import ModalScreen

from expense_tracker.presenter.presenter import Presenter


class Exptrack_Data_Table(DataTable):
    """
    Generates interactive data tables from each of the data types.

    Should be extended to create specific table classes.
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
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        """
        Initializes the widget.

        Args:
            presenter: The presenter that is used to get data for the table.
            column_list: List of columns for the table containing the column display name and an presenter Column.
            name: The name of the widget.
            id: The ID of the widget in the DOM.
            classes: The CSS classes for the widget.
        """
        self.presenter: Presenter = presenter
        self.column_list: list[tuple[str, Enum]] = column_list

        super().__init__(
            zebra_stripes=True,
            name=name,
            id=id,
            classes=classes,
        )

    def on_mount(self) -> None:
        """
        Called when the widget is mounted, adds the columns and initial rows.
        """
        # Set the cursor type
        self.cursor_type = "row"

        # Add an id column and other columns
        for column in self.column_list:
            self.add_column(column[0], key=column[1])

        self.refresh_data()

    def refresh_data(self) -> None:
        """
        Clears and refreshes data from the database.
        """

        self.clear()

        for row in self._get_row_data():
            # Check that the row is of correct length
            if len(self.columns) != len(row):
                raise ValueError(
                    f"Table has {len(self.columns)} columns but was given a row with {len(row)} values."
                )
            # Check that the row is of correct type
            if not all(type(cell) == str for cell in row):
                raise ValueError(f"Row {row} must only contain strings.")

            # line_counts = [cell.count("\n") + 1 for cell in formatted_cells]
            # height = max(line_counts)

            cell_height_list: list[int] = (cell.count("\n") + 1 for cell in row)
            row_height: int = max(cell_height_list)

            # Style and add the row
            self.add_row(
                *(Text(cell, style=self.get_row_style(row)) for cell in row),
                key=row[0],
                height=row_height,
            )

    def get_row_style(self, row: tuple[str, ...]) -> str:
        """
        Gets the style for a row. Should be extended if the table requires custom row styles.

        Args:
            row: Row in display format

        Return: Style as a string
        """

        return ""

    def _get_row_data(self) -> list[tuple[str, ...]]:
        """
        Gets the rows for the table, should be extended if table requires filtered data.

        Return: List of rows in display format.
        """

        return self.presenter.get_all()

    def action_create(self) -> None:
        """
        Called when c is pressed, should be extended and implemented.
        """

        return

    def action_expand(self) -> None:
        """
        Called when e is pressed, should be extended and implemented to allow for an expand feature.
        """

        return

    def action_delete(self) -> None:
        """
        Called when d is pressed, should be extended and implemented.
        """

        return

    def on_click(self, event: Click) -> None:
        """
        Called when the user clicks a cell, if this shift key is held down then mount a
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

        def callback(new_value: Optional[Union[int, str, datetime]]) -> None:
            """
            Updates the database and the view with the new value.

            Args:
                new_value: The value that the user inputted. Should be handled and converted into a displayable string by the presenter.
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

    def get_input_popup(self, column: Enum, id: int) -> Optional[ModalScreen]:
        """
        Gets the popup required to obtain user input for a column data type.

        Columns in each exptrack_data_table can display different data types. This function finds the popup required to deal with the column data type and returns it so it can be mounted. Should be extended to handel the specific presenters columns.

        Args:
            column: Column enum provided by the presenter class.
            id: The id of the row that was clicked.

        Return: A popup in the form of a ModalScreen if one is found.
        """

        return None
