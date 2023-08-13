# expense_tracker/view/popup/toggle_input_popup.py

from textual.app import ComposeResult
from textual.widgets import Static, SelectionList
from textual.widgets.selection_list import Selection
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.binding import Binding

from typing import Optional, NamedTuple


class Toggle_Input_Popup(ModalScreen[Optional[int]]):
    """
    Popup that prompts the user to select an option from many
    """

    DEFAULT_CSS: str = """
        Toggle_Input_Popup {
            align: center middle;
        }

        Toggle_Input_Popup > Vertical {
            width: 60;
            height: auto;
            background: $surface;
            padding: 1;
        }

        Toggle_Input_Popup > Vertical > SelectionList {
            margin-top: 1;
        }
    """

    BINDINGS: list[Binding] = [
        Binding("escape", "exit_popup", "Dismiss popup"),
        Binding("enter", "submit", "Submit", priority=True),
    ]

    def __init__(
        self,
        option_list: list[Selection] = [],
        instructions: str = "Enter a value",
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        self._option_list: list[Selection] = sorted(
            option_list, key=lambda x: str(x.prompt)
        )
        self._instructions_text: str = instructions
        super().__init__(name, id, classes)

    def compose(self) -> ComposeResult:
        self._container: Vertical = Vertical()
        self._instructions_widget: Static = Static(self._instructions_text)
        self._selector_widget: SelectionList = SelectionList(*self._option_list)

        with self._container:
            yield self._instructions_widget
            yield self._selector_widget

    def action_submit(self) -> None:
        """
        Called when the popup is submitted
        """
        self.dismiss(self._selector_widget.selected)

    def action_exit_popup(self) -> None:
        """
        Called when the escape key is pressed.

        Returns none and dismisses.
        """
        self.dismiss(None)
