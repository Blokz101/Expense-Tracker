# expense_tracker/view/exptrack_app.py

from textual.app import App, ComposeResult
from textual.validation import Regex

from expense_tracker.constants import Constants

from expense_tracker.view.text_input_popup import Text_Input_Popup
from expense_tracker.view.transaction_table import Transaction_Table

from expense_tracker.presenter.transaction import Transaction


class Exptrack_App(App):
    """
    Main app
    """

    CSS_PATH = Constants.CSS_FILE_PATH

    def compose(self) -> ComposeResult:
        yield Transaction_Table()

    def on_mount(self) -> None:
        table = self.query_one(Transaction_Table)

        for row in Transaction.get_display():
            table.add_row(*row[0:], key=row[0])

        print(table.cursor_coordinate)

    def on_exptrack_data_table_edit_request(
        self, message: Transaction_Table.Edit_Request
    ) -> None:
        def check_input(new_value: str) -> None:
            print(new_value)

        self.push_screen(message.popup, check_input)
