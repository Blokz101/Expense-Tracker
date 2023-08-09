# expense_tracker/view/selector.py

from __future__ import annotations

from textual.app import ComposeResult
from textual.widget import Widget
from textual.geometry import Size
from textual.widgets import Input, OptionList
from textual.widgets.option_list import Option as ListOption
from textual.widgets.option_list import Separator
from textual.containers import Vertical
from textual.message import Message

from typing import Optional, NamedTuple

from difflib import SequenceMatcher

from typing import Optional

from expense_tracker.config_manager import Config_Manager


class Selector(Widget):
    """
    Select an option from a list of options
    """

    DEFAULT_CSS: str = """
        Selector {
            height: auto;
        }

        Selector > Vertical {
            height: auto;
        }

        Selector > Vertical > OptionList {
            height: 7;
        }
    """

    class Option(NamedTuple):
        display_name: str
        option_id: int

    class Submitted(Message):
        """
        Message to indicate that the selector was submitted and to contain the id of the selected option.
        """

        def __init__(self, option_id: int) -> None:
            self.option_id = option_id
            super().__init__()

    def __init__(
        self,
        option_list: list[Option] = [],
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        """
        Constructor
        """
        self._option_list: list[Selector.Option] = option_list
        super().__init__(name=name, id=id, classes=classes)

    def compose(self) -> ComposeResult:
        """
        Composes the display
        """

        self._container: Vertical = Vertical()
        self._input_widget: Input = Input(placeholder="Search and select")
        self._list_view: OptionList = OptionList()

        with self._container:
            yield self._input_widget
            yield self._list_view

        self.update_options_list()

    def on_input_changed(self, event: Input.Changed) -> None:
        """
        Called when the input is changed.

        Updates the options list.
        """
        self.update_options_list(search_input=event.value)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """
        Called when the input is submitted.

        Sends the submitted message with the first option id.
        """
        self.post_message(self.Submitted(self._option_list[0].option_id))

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """
        Called when an option is selected.

        Sends the submitted message with the id of the selected option.
        """
        self.post_message(self.Submitted(event.option_id))

    def update_options_list(self, search_input: Optional[str] = None) -> None:
        """
        Sorts and re draws the option list
        """
        if search_input:
            self._search_options_list(search_input)

        self._list_view.clear_options()
        self._list_view.add_options(
            ListOption(option.display_name, id=option.option_id)
            for option in self._option_list
        )

    def _search_options_list(self, search_input: str) -> list[tuple[str, int]]:
        """
        Sort a list of options based on how close it is to a given search_input.
        """

        # Create a list with each option and a value that relates the similarity of the option key to the search_input
        compared_options_list: list[tuple[float, any]] = []
        for option in self._option_list:
            compared_option: tuple[float, any] = (
                option,
                SequenceMatcher(None, option[0].lower(), search_input.lower()).ratio(),
            )
            compared_options_list.append(compared_option)

        # Sort the list and return
        compared_options_list.sort(key=lambda x: x[1], reverse=True)
        self._option_list = list(option[0] for option in compared_options_list)
