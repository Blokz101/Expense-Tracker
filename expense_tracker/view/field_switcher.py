# expense_tracker/view/field_switcher.py

from enum import Enum

from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import ContentSwitcher, OptionList, Placeholder
from textual.containers import Horizontal
from textual.widgets.option_list import Option

from expense_tracker.view.exptrack_data_table import Exptrack_Data_Table
from expense_tracker.view.table_constants import Table_Constants

from expense_tracker.presenter.transaction import Transaction
from expense_tracker.presenter.merchant import Merchant
from expense_tracker.presenter.account import Account
from expense_tracker.presenter.location import Location
from expense_tracker.presenter.tag import Tag

class Field_Switcher(Widget):
    """
    Switches field tables based on what the user selects
    """

    CSS: str = """
    
    """

    class Fields(Enum):
        ACCOUNT: int = 0
        BUDGET: int = 1
        LOCATION: int = 2
        MERCHANT: int = 3
        TAG: int = 4

    _OPTION_LIST_OPTIONS: list[Option] = [
        Option("Account", id="account"),
        Option("Budget", id="budget"),
        Option("Location", id="location"),
        Option("Merchant", id="merchant"),
        Option("Tag", id="tag"),
    ]

    _TABLE_WIDGETS: list[Widget] = [
        Exptrack_Data_Table(
            Table_Constants.account_column_list,
            Account.get_all(),
            Table_Constants.account_popup_args,
            id=Table_Constants.Tables.ACCOUNT,
        ),
        Placeholder("Budget", id="budget"),
        Exptrack_Data_Table(
            Table_Constants.location_column_list,
            Location.get_all(),
            Table_Constants.location_popup_args,
            id=Table_Constants.Tables.LOCATION,
        ),
        Exptrack_Data_Table(
            Table_Constants.merchant_column_list,
            Merchant.get_all(),
            Table_Constants.merchant_popup_args,
            id=Table_Constants.Tables.MERCHANT,
        ),
        Exptrack_Data_Table(
            Table_Constants.tag_column_list,
            Tag.get_all(),
            Table_Constants.tag_popup_args,
            id=Table_Constants.Tables.TAG,
        ),
    ]

    def compose(self) -> ComposeResult:
        self._container: Horizontal = Horizontal()
        self._field_list_widget: OptionList = OptionList(
            *Field_Switcher._OPTION_LIST_OPTIONS
        )
        self._content_switcher: ContentSwitcher = ContentSwitcher(initial="account")

        with self._container:
            yield self._field_list_widget
            with self._content_switcher:
                for widget in Field_Switcher._TABLE_WIDGETS:
                    yield widget

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """
        Called when a new option is selected.
        
        Switches the content switcher.
        """
        self._content_switcher.current = event.option_id
