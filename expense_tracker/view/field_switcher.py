# expense_tracker/view/field_switcher.py

from enum import Enum

from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import ContentSwitcher, OptionList, Placeholder
from textual.containers import Horizontal
from textual.widgets.option_list import Option

from expense_tracker.view.merchant_table import Merchant_Table


class Field_Switcher(Widget):
    """
    TODO Fill this in
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
        Placeholder("Account", id="account"),
        Placeholder("Budget", id="budget"),
        Placeholder("Location", id="location"),
        Merchant_Table(id="merchant"),
        Placeholder("Tag", id="tag"),
    ]

    def compose(self) -> ComposeResult:
        """
        TODO Fill this in
        """

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
        TODO Fill this in
        """
        self._content_switcher.current = event.option_id
