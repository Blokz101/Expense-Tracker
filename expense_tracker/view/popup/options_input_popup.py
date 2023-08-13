# expense_tracker/view/popup/options_input_popup.py

from textual.app import ComposeResult
from textual.widgets import Static
from textual.containers import Vertical
from textual.screen import ModalScreen

from expense_tracker.view.selector import Selector

from typing import Optional, NamedTuple


class Options_Input_Popup(ModalScreen[Optional[int]]):
    """
    Popup that prompts the user to select an option from many
    """

    DEFAULT_CSS: str = """
        Options_Input_Popup {
            align: center middle;
        }

        Options_Input_Popup > Vertical {
            width: 60;
            height: auto;
            background: $surface;
            padding: 1;
        }

        Options_Input_Popup > Vertical > Selector {
            margin-top: 1;
        }
    """

    BINDINGS: list[tuple[str, str, str]] = [
        ("escape", "exit_popup", "Dismiss popup"),
    ]

    def __init__(
        self,
        option_list: list[Selector.Option] = [],
        instructions: str = "Enter a value",
        default: Optional[str] = None,
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        self._option_list: list[Selector.Option] = option_list
        self._instructions_text: str = instructions
        self._default: Optional[str] = default
        super().__init__(name, id, classes)

    def compose(self) -> ComposeResult:
        self._container: Vertical = Vertical()
        self._instructions_widget: Static = Static(self._instructions_text)
        self._selector_widget: Selector = Selector(self._option_list)

        with self._container:
            yield self._instructions_widget
            yield self._selector_widget

    def action_exit_popup(self) -> None:
        """
        Called when the escape key is pressed.

        Returns none and dismisses.
        """

        self.dismiss(None)

    def on_selector_submitted(self, event: Selector.Submitted) -> None:
        """
        Called when the selector is submitted.

        Dismisses popup and returns the id of the chosen option.
        """
        self.dismiss(event.option_id)
