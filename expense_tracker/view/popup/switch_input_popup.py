# expense_tracker/view/popup/switch_input_popup.py

from textual.app import ComposeResult
from textual.widgets import Input, Static, Switch
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.validation import Validator
from textual.css.query import NoMatches
from textual.binding import Binding

from typing import Optional


class Switch_Input_Popup(ModalScreen[Optional[bool]]):
    """
    Popup that prompts the user to select true or false
    """

    DEFAULT_CSS: str = """
        Switch_Input_Popup {
            align: center middle;
        }

        Switch_Input_Popup > Vertical {
            width: 60;
            height: auto;
            background: $surface;
            padding: 1;
        }

        Switch_Input_Popup > Vertical > Switch {
            margin: 1 0 0 0;
        }
    """

    BINDINGS: list[tuple[str, str, str]] = [
        Binding("escape", "exit_popup", "Dismiss popup"),
        Binding("enter", "submit", "Submit", priority=True),
    ]

    def __init__(
        self,
        instructions: str = "Select true or false",
        default: Optional[bool] = None,
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        """
        Constructor
        """
        super().__init__(name, id, classes)
        self._instructions_text: str = instructions
        self._default: Optional[bool] = default

    def compose(self) -> ComposeResult:
        """
        Composes the display
        """
        self._container: Vertical = Vertical()
        self._instructions_widget: Static = Static(self._instructions_text)
        self._switch_widget: Switch = Switch()

        with self._container:
            yield self._instructions_widget
            yield self._switch_widget

    def action_submit(self) -> None:
        """
        Called when the popup is submitted
        """
        self.dismiss(self._switch_widget.value)

    def action_exit_popup(self) -> None:
        """
        Called when the escape key is pressed.

        Returns none and dismisses.
        """

        self.dismiss(None)
