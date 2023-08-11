# expense_tracker/view/field_switcher.py

from enum import Enum

from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import ContentSwitcher, OptionList, Placeholder
from textual.containers import Horizontal
from textual.widgets.option_list import Option

from expense_tracker.view.merchant_table import Merchant_Table
from expense_tracker.view.account_table import Account_Table
from expense_tracker.view.location_table import Location_Table
from expense_tracker.view.tag_table import Tag_Table


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
        Account_Table(id="account"),
        Placeholder("Budget", id="budget"),
        Location_Table(id="location"),
        Merchant_Table(id="merchant"),
        Tag_Table(id="tag"),
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
