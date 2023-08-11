# expense_tracker/view/exptrack_app.py

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, TabbedContent, TabPane, Placeholder
from expense_tracker.constants import Constants

from expense_tracker.view.exptrack_data_table import Exptrack_Data_Table

from expense_tracker.view.field_switcher import Field_Switcher
from expense_tracker.view.table_constants import TRANSACTION

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
                yield Exptrack_Data_Table(TRANSACTION)
            with TabPane("Budgets"):
                yield Placeholder("Budgets coming soon")
            with TabPane("Fields"):
                yield Field_Switcher()
        yield Footer()
