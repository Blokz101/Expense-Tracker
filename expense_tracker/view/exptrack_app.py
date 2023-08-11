# expense_tracker/view/exptrack_app.py

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, TabbedContent, TabPane, Placeholder
from expense_tracker.constants import Constants

from expense_tracker.view.exptrack_data_table import Exptrack_Data_Table
from expense_tracker.view.field_switcher import Field_Switcher
from expense_tracker.view.table_constants import Table_Constants

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
                yield Exptrack_Data_Table(
                    Table_Constants.transaction_column_list,
                    Transaction.get_all(),
                    Table_Constants.transaction_popup_args,
                    id=Table_Constants.Tables.TRANSACTION,
                )
            with TabPane("Budgets"):
                yield Placeholder("Budgets coming soon")
            with TabPane("Fields"):
                yield Field_Switcher()
        yield Footer()

    def on_exptrack_data_table_edit_request(self, message: Exptrack_Data_Table.Edit_Request):
        """
        Called when a table cell is clicked.
        
        Mounts a popup to get user input and edits the database with the users input.
        """

        def check_input(new_value: Optional[str]) -> None:
            """
            Updates the database and the view with the new value
            """
            presenter: Presenter = self._get_presenter(message.sender.id)
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
        
    def _get_presenter(self, id: str) -> Presenter:
        """
        Gets the presenter to use based on the table
        """
        
        if id == Table_Constants.Tables.TRANSACTION:
            return Transaction
            
        if id == Table_Constants.Tables.MERCHANT:
            return Merchant
        
        if id == Table_Constants.Tables.TAG:
            return Tag
        
        if id == Table_Constants.Tables.LOCATION:
            return Location
        
        if id == Table_Constants.Tables.ACCOUNT:
            return Account
        
        raise ValueError(f"No presenter found for table id {id}")
