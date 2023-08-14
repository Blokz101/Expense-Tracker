# expense_tracker/view/popup/create_popup.py

from __future__ import annotations

from enum import Enum

from dataclasses import dataclass

from textual.app import ComposeResult
from textual.widgets import Static, DataTable
from textual.widgets._data_table import RowKey, ColumnKey, CellKey
from textual.containers import Vertical
from textual.coordinate import Coordinate
from textual.screen import ModalScreen
from textual.events import Click
from textual.binding import Binding

from expense_tracker.view.table.exptrack_data_table import Exptrack_Data_Table

from typing import Optional


class Input_Method(str, Enum):
    NONE: str = "None"
    MANUAL: str = "Manual"
    DEFAULT: str = "Default"
    PHOTO: str = "Photo"


class Create_Popup(ModalScreen):
    """
    Prompt the user for the info required to create a new object.
    """

    @dataclass
    class Field:
        value: any = None
        input_method: Input_Method = Input_Method.NONE

    def __init__(
        self,
        parent_table: Exptrack_Data_Table,
        instructions: str = "Create",
        modified_column_list: Optional[list[tuple[Enum, any]]] = None,
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes)
        self.instruction_text: str = instructions
        self.parent_table: Exptrack_Data_Table = parent_table

        # Generate the colum list if unless a modified one is provided
        self.column_list: list[tuple[Enum, any]] = self.parent_table.column_list
        if modified_column_list:
            self.column_list = modified_column_list

        # Generate a blank list of values for each column in the parent table, excluding the first or id column
        self.values: dict[Enum, Create_Popup.Field] = {}
        for column in self.column_list[1:]:
            self.values[column[1]] = Create_Popup.Field()

    BINDINGS: list[tuple[str, str, str]] = [
        Binding("escape", "exit_popup", "Dismiss popup"),
        Binding("enter", "submit", "Submit", priority=True),
    ]

    def compose(self) -> ComposeResult:
        """
        Composes the display
        """
        self._container: Vertical = Vertical()
        self._instructions_widget: Static = Static(self.instruction_text)
        self._data_table_widget: DataTable = DataTable(show_cursor=False)
        self._validation_status_widget: Static = Static(id="validation_status")

        with self._container:
            yield self._instructions_widget
            yield self._data_table_widget
            yield self._validation_status_widget

    def on_mount(self) -> None:
        """
        Called when the widget is mounted.

        Adds the rows and columns.
        """

        # Set the validation widget
        self._validation_status_widget.update(f"Missing {self.empty_values()} values.")

        # Add columns
        self._data_table_widget.add_column("Detail", key="detail")
        self._data_table_widget.add_column("Value", key="value")
        self._data_table_widget.add_column("Entry", key="entry")

        # Add rows, the rows and columns are flipped so be careful with naming
        for row_key, value in zip(self.column_list[1:], self.values.values()):
            display_value: str = "None"
            input_method: Input_Method = Input_Method.NONE
            if value.value:
                print(row_key[1])
                display_value = self.parent_table.presenter.get_value(
                    value.value,
                    row_key[1],
                )
                input_method = value.input_method

            self._data_table_widget.add_row(
                row_key[0],
                display_value,
                input_method.value,
                key=row_key[1],
            )

    def set_value(self, key: str, new_value: any, input_method: Input_Method) -> None:
        """
        Sets a value in the value dict and updates the validation widget
        """

        # Get the value
        updated_value: str = self.parent_table.presenter.get_value(
            new_value,
            key,
        )

        # Update stored values
        self.values[key].value = new_value
        self.values[key].input_method = input_method

        # Update self
        self._data_table_widget.update_cell(
            RowKey(key),
            ColumnKey("value"),
            updated_value,
            update_width=True,
        )
        self._data_table_widget.update_cell(
            RowKey(key),
            ColumnKey("entry"),
            self.values[key].input_method.value,
            update_width=True,
        )

        # update validation widget
        self._update_validation_widget()

    def _update_validation_widget(self) -> None:
        """
        Update the validation widget based on if its submittable
        """

        # Update the validation widget's text and self's class
        if self.submittable() == True and not "submittable" in self.classes:
            self.add_class("submittable")
            self._validation_status_widget.update("Submittable")

        if self.submittable() == False:
            self._validation_status_widget.update(
                f"Missing {self.empty_values()} values."
            )

    def submittable(self) -> bool:
        """
        If all the values are filled and the create popup can be submitted
        """
        for value in self.values.values():
            if value.value is None:
                return False
        return True

    def empty_values(self) -> int:
        """
        The number of empty values
        """
        return len(list(value for value in self.values.values() if value.value is None))

    def action_submit(self) -> bool:
        """
        Called when the user attempts to submit the values.

        If there are any blank values then automatically directs the user to fill them out, if not then create the new transaction.
        """

        # If there are still blank values then automatically mount a popup to prompt the user to fill it in
        for key, value in self.values.items():
            if value.value is None:
                self._mount_popup(key)
                return False

        # Strip the entry method from the values dict to create a submittable dict
        submittable_dict: dict[Enum, any] = {}
        for key, value in self.values.items():
            submittable_dict[key] = value.value

        # Add the new row to the database
        new_row: list = self.parent_table.presenter.create(submittable_dict)

        # Update parent table
        self.parent_table.add_row(*new_row[0:], key=new_row[0])

        # Dismiss self
        self.dismiss()
        return True

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

        # Mount the popup
        self._mount_popup(row_key)

    def _mount_popup(self, column_key: str) -> None:
        """
        Mount the input popup, and update self with the return value
        """

        # Get the popup for the column
        popup: ModalScreen = self.get_input_popup(column_key, None)

        # If there is no popup then return
        if not popup:
            return

        def input_popup_callback(new_value: Optional[any]) -> None:
            """
            Updates the database and the view with the new value
            """

            # If there is no new value then dont do anything
            if new_value is None:
                return

            # Update values
            self.set_value(column_key, new_value, Input_Method.MANUAL)

        self.app.push_screen(popup, input_popup_callback)

    def get_input_popup(self, column: str, id: int) -> Optional[ModalScreen]:
        """
        Get the input popup based on the column
        """

        return self.parent_table.get_input_popup(column, id)
