# expense_tracker/view/exptrack_app.py

from textual.app import App, ComposeResult
from textual.validation import Regex

from expense_tracker.constants import Constants

from expense_tracker.view.transaction_table import Transaction_Table

from expense_tracker.presenter.transaction import Transaction

from typing import Optional


class Exptrack_App(App):
    """
    Main app
    """

    CSS_PATH = Constants.CSS_FILE_PATH

    def compose(self) -> ComposeResult:
        yield Transaction_Table()

    def on_mount(self) -> None:
        table = self.query_one(Transaction_Table)

        for row in Transaction.get_display_list():
            table.add_row(*row[0:], key=row[0])

    def on_exptrack_data_table_edit_request(
        self, message: Transaction_Table.Edit_Request
    ) -> None:
        """
        Called when a database popup is requested.

        Mounts a popup to get input from the user and attempts to edit the database.
        """

        def check_input(new_value: Optional[str]) -> None:
            """
            Updates the database and the view with the new value
            """

            if not new_value:
                return

            updated_value: str = Transaction.set_value(
                int(message.row_key.value), message.column_key.value, new_value
            )
            message.sender.update_cell(
                message.row_key, message.column_key, updated_value
            )

        self.push_screen(message.popup(*message.args), check_input)
