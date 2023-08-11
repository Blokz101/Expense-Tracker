# expense_tracker/view/exptrack_app.py

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, TabbedContent, TabPane, Placeholder
from expense_tracker.constants import Constants

from expense_tracker.view.exptrack_data_table import Exptrack_Data_Table
from expense_tracker.view.transaction_table import Transaction_Table
from expense_tracker.view.merchant_table import Merchant_Table
from expense_tracker.view.field_switcher import Field_Switcher

from expense_tracker.presenter.presenter import Presenter
from expense_tracker.presenter.transaction import Transaction
from expense_tracker.presenter.merchant import Merchant
from expense_tracker.presenter.account import Account
from expense_tracker.presenter.location import Location
from expense_tracker.presenter.tag import Tag

from typing import Optional


class Exptrack_App(App):
    """
    Main app
    """

    CSS_PATH = Constants.CSS_FILE_PATH

    def compose(self) -> ComposeResult:
        yield Header()
        with TabbedContent():
            with TabPane("Accounts"):
                yield Transaction_Table()
            with TabPane("Budgets"):
                yield Placeholder("Budgets coming soon")
            with TabPane("Fields"):
                yield Field_Switcher()
        yield Footer()

    # The next many functions are all request edit handlers which just call _edit_value
    def on_transaction_table_edit_request(
        self, message: Transaction_Table.Edit_Request
    ) -> None:
        self._edit_value(message, Transaction)

    def on_merchant_table_edit_request(
        self, message: Merchant_Table.Edit_Request
    ) -> None:
        self._edit_value(message, Merchant)

    def on_account_table_edit_request(
        self, message: Merchant_Table.Edit_Request
    ) -> None:
        self._edit_value(message, Account)
        
    def on_location_table_edit_request(
        self, message: Merchant_Table.Edit_Request
    ) -> None:
        self._edit_value(message, Location)
        
    def on_tag_table_edit_request(
        self, message: Merchant_Table.Edit_Request
    ) -> None:
        self._edit_value(message, Tag)

    def _edit_value(
        self, message: Exptrack_Data_Table.Edit_Request, presenter: Presenter
    ) -> None:
        """
        Called whenever a database popup is requested.
        
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
