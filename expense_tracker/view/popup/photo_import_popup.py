# expense_tracker/view/popup/photo_import_popup.py

from textual.app import ComposeResult
from textual.widgets import Input, Static, DataTable
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.validation import Function
from textual.css.query import NoMatches
from textual.binding import Binding

from pathlib import Path

from expense_tracker.model.photo_manager import Photo_Manager

from expense_tracker.presenter.transaction import Transaction

from expense_tracker.view.popup.transaction_create_popup import Transaction_Create_Popup
from expense_tracker.view.table.exptrack_data_table import Exptrack_Data_Table
from expense_tracker.view.popup.popup_utils import Popup_Utils

from typing import Optional


class Photo_Import_Popup(ModalScreen):
    """
    Popup that takes a path to a directory and imports photos from it
    """

    DEFAULT_CSS: str = """
        Photo_Import_Popup {
            align: center middle;
        }

        Photo_Import_Popup > Vertical {
            width: 60;
            height: auto;
            background: $surface;
            padding: 1;
        }

        Photo_Import_Popup > Vertical > Input,  Photo_Import_Popup > Vertical > DataTable{
            margin-top: 1;
        }
        
        .valid #validation_status {
            color: $primary;
        }

        #validation_status {
            color: $error;
        }
    """

    NON_REQUIRED_COLUMNS: list[Transaction.Column] = [
        Transaction.Column.ID,
        Transaction.Column.RECONCILED_STATUS,
    ]

    BINDINGS: list[Binding] = [
        Binding("escape", "exit_import", "Dismiss all", priority=True),
    ]

    def __init__(
        self,
        parent_table: Exptrack_Data_Table,
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        super().__init__(name, id, classes)
        self.parent_table: Exptrack_Data_Table = parent_table

    def compose(self) -> ComposeResult:
        """
        Composes the display
        """
        self._container: Vertical = Vertical()
        self._instructions_widget: Static = Static(
            "Input the path to the import directory."
        )
        self._validation_status_widget: Static = Static(id="validation_status")
        self._input_widget: Input = Input(
            validators=[
                Function(
                    Popup_Utils._directory_exists,
                    failure_description="Directory does not exist",
                ),
                Function(
                    Popup_Utils._photos_in_directory,
                    failure_description="No photos in directory",
                ),
            ]
        )

        self._data_table_widget: DataTable = DataTable(
            id="photo_table", show_cursor=False
        )
        self._data_table_widget.add_column("Photos")

        with self._container:
            yield self._instructions_widget
            yield self._input_widget

    def on_input_changed(self, event: Input.Changed) -> None:
        """
        Called when the input widget is changed.

        Updates the validation status widget if the input is valid.
        """
        # Mount the validation status widget if it is not mounted
        try:
            self.query_one("#validation_status", Static)
        except NoMatches:
            self._container.mount(
                self._validation_status_widget, after=self._input_widget
            )

        # If validation fails then update the validation status widget and return
        if not event.validation_result.is_valid:
            self._validation_status_widget.update(
                event.validation_result.failure_descriptions[0]
            )
            self.remove_class("valid")
            return

        # Update validation widget and update datatable
        self._validation_status_widget.update("Input is valid")
        self.add_class("valid")

        # Mount the datatable widget if it is not mounted
        try:
            self.query_one("#photo_table", DataTable)
        except NoMatches:
            self._container.mount(self._data_table_widget)

        # Update the data table
        self._data_table_widget.clear()
        path: Path = Path(Popup_Utils._get_path(self._input_widget.value))
        for photo in Photo_Manager.photos_in_directory(path):
            self._data_table_widget.add_row(photo.name)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """
        Called when the input widget is submitted with the enter key.

        Returns the input value if validation is successful and dismisses.
        """

        if not event.validation_result.is_valid:
            return

        self.dismiss()
        path: Path = Path(Popup_Utils._get_path(self._input_widget.value))

        print(
            "\n".join(
                list(
                    str(column)
                    for column in self.parent_table.column_list
                    if not column.key in Photo_Import_Popup.NON_REQUIRED_COLUMNS
                )
            )
        )

        self.app.push_screen(
            Transaction_Create_Popup(
                self.parent_table,
                import_list=Photo_Manager.photos_in_directory(path),
                excluded_column_key_list=Photo_Import_Popup.NON_REQUIRED_COLUMNS,
            )
        )

    def action_exit_import(self) -> None:
        """
        Called when the escape key is pressed.

        Dismisses all popups
        """

        self.dismiss()
