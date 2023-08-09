# expense_tracker/view/selector.py

from __future__ import annotations

from textual.app import ComposeResult
from textual.widget import Widget
from textual.geometry import Size
from textual.widgets import Input, ListView, ListItem, Static, OptionList
from textual.widgets.option_list import Option, Separator
from textual.containers import Vertical
from textual.message import Message

from typing import Optional, NamedTuple

from difflib import SequenceMatcher

from typing import Optional

from expense_tracker.config_manager import Config_Manager


class Selector(Widget):
    """
    TODO Fill this in
    """

    class Option(NamedTuple):
        display_name: str
        option_id: int

    class Submitted(Message):
        """
        TODO Fill this in
        """

        def __init__(self, option: Selector.Option) -> None:
            self.display_name = option.display_name
            self.option_id = option.option_id
            super().__init__()

    def __init__(
        self,
        option_list: list[tuple[str, int]] = [],
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        self._option_list: list[tuple[str, int]] = option_list
        super().__init__(name=name, id=id, classes=classes)

    def compose(self) -> ComposeResult:
        """
        TODO Fill this in
        """

        self._option_widget_list: list[Static] = list(
            Static("") for _ in self._option_list
        )

        self._container: Vertical = Vertical()
        self._input_widget: Input = Input()
        self._list_view: ListView = ListView(
            *(ListItem(static) for static in self._option_widget_list)
        )

        with self._container:
            yield self._input_widget
            yield self._list_view

    def on_mount(self) -> None:
        """
        TODO Fill this in
        """
        self.update_options_list()
        
    # def get_content_height(self, container: Size, viewport: Size) -> int:
    #     """
    #     TODO Fill this in
    #     """
    #     return 5 + Config_Manager().get_number_of_options()

    def on_input_changed(self, event: Input.Changed) -> None:
        """
        TODO Fill this in
        """

        self.update_options_list(search_input=event.value)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """
        TODO Fill this in
        """
        self.post_message(self.Submitted(self._option_list[0]))

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """
        TODO Fill this in
        """
        self.post_message(
            self.Submitted(
                self._option_list[list(self.query(ListItem)).index(event.item)]
            )
        )

    def update_options_list(self, search_input: Optional[str] = None) -> None:
        """
        TODO Fill this in
        """

        if search_input:
            self._search_options_list(search_input)

        for index, widget in enumerate(self._option_widget_list):
            if len(self._option_list) > index:
                widget.update(self._option_list[index][0])
            else:
                widget.update("")

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
