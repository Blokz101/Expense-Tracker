# expense_tracker/view/exptrack_app.py

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, TabbedContent, TabPane, Placeholder
from expense_tracker.constants import Constants

from expense_tracker.view.exptrack_data_table import Exptrack_Data_Table
from expense_tracker.view.transaction_table import Transaction_Table
from expense_tracker.view.merchant_table import Merchant_Table

from expense_tracker.presenter.presenter import Presenter
from expense_tracker.presenter.transaction import Transaction
from expense_tracker.presenter.merchant import Merchant

from typing import Optional


class Exptrack_App(App):
    """
    Main app
    """

    CSS_PATH = Constants.CSS_FILE_PATH

    def compose(self) -> ComposeResult:
        yield Header()
        yield Transaction_Table()
        yield Footer()

    def on_transaction_table_edit_request(
        self, message: Transaction_Table.Edit_Request
    ) -> None:
        """
        Called when a transaction database popup is requested.

        Signals what presenter should be used
        """
        self._edit_value(message, Transaction)
        
    def on_merchant_table_edit_request(
        self, message: Merchant_Table.Edit_Request
    ) -> None:
        """
        Called when a database popup is requested.

        Signals what presenter should be used
        """
        self._edit_value(message, Merchant)

    def _edit_value(self, message: Exptrack_Data_Table.Edit_Request, presenter: Presenter) -> None:
        """
        Mounts a popup to get input from the user and attempts to edit the database.
        """
        
        def check_input(new_value: Optional[str]) -> None:
            """
            Updates the database and the view with the new value
            """

            if new_value is None:
                return

            updated_value: str = presenter.set_value(
                int(message.row_key.value), message.column_key.value, new_value
            )
            message.sender.update_cell(
                message.row_key,
                message.column_key,
                updated_value,
                update_width=True,
            )

        self.push_screen(message.popup(*message.args), check_input)
