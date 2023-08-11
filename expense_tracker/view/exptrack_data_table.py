# expense_tracker/view/exptrack_data_table.py

from __future__ import annotations

from collections import Callable

from typing import Any, Optional
from textual.coordinate import Coordinate
from textual.message import Message
from textual.widgets import DataTable
from textual.widgets._data_table import CellKey
from textual.events import Click
from textual.screen import ModalScreen
from textual.widgets._data_table import RowKey, ColumnKey

from expense_tracker.view.table_constants import Table_Info, Column_Info

from expense_tracker.presenter.presenter import Presenter
from expense_tracker.presenter.transaction import Transaction
from expense_tracker.presenter.merchant import Merchant
from expense_tracker.presenter.account import Account
from expense_tracker.presenter.location import Location
from expense_tracker.presenter.tag import Tag


class Exptrack_Data_Table(DataTable):
    """
    Generates data tables from each of the data types.
    """

    def __init__(
        self,
        table_info_list: Table_Info,
        initial_row_list: list[tuple[int, ...]] = None,
        name: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        self._presenter: Presenter = table_info_list.presenter
        self._column_info_list: list[Column_Info] = table_info_list.column_list

        # Set the initial row list
        self._initial_row_list: list[tuple[int, ...]]
        if not initial_row_list:
            self._initial_row_list = self._presenter.get_all()
        else:
            self._initial_row_list = initial_row_list

        super().__init__(
            show_cursor=False,
            zebra_stripes=True,
            name=name,
            id=table_info_list.name,
            classes=classes,
        )

    def on_mount(self) -> None:
        """
        Called when the widget is mounted.

        Adds the columns and initial rows.
        """
        # Add an id column and other columns
        self.add_column("id", key="id")
        for info in self._column_info_list:
            self.add_column(info.display_name, key=info.column_variable)

        # Add initial rows
        for row in self._initial_row_list:
            if len(self.columns) != len(row):
                raise ValueError(
                    f"Table has {len(self.columns)} columns but was given a row with {len(row)} values."
                )
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
        column: Column_Info
        try:
            column = next(
                (
                    info
                    for info in self._column_info_list
                    if info.column_variable == column_key.value
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

            updated_value: str = self._presenter.set_value(
                int(row_key.value), column_key.value, new_value
            )
            self.update_cell(
                row_key,
                column_key,
                updated_value,
                update_width=True,
            )

        self.app.push_screen(column.popup_factory(row_key.value), update_view_and_model)
