# expense_tracker/view/popup/text_input_popup.py

from textual.app import ComposeResult
from textual.widgets import Input, Static
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.validation import Validator

from expense_tracker.view.validated_input import Validated_Input

from typing import Optional, Union


class Text_Input_Popup(ModalScreen[Optional[str]]):
    """
    Popup that prompts the user for text input.
    """

    DEFAULT_CSS: str = """
        Text_Input_Popup {
            align: center middle;
        }

        Text_Input_Popup > Vertical {
            width: 60;
            height: auto;
            background: $surface;
            padding: 1;
        }

        Text_Input_Popup > Vertical > Input {
            margin: 1 0 0 0;
        }
    """

    BINDINGS: list[tuple[str, str, str]] = [
        ("escape", "exit_popup", "Dismiss popup"),
    ]

    def __init__(
        self,
        instructions: str = "Enter a value",
        validators: list[Validator] = [],
        default: Optional[str] = None,
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        """
        Constructor
        """
        super().__init__(name, id, classes)
        self._instructions_text: str = instructions
        self._default: Optional[str] = default
        self._validators = validators

    def compose(self) -> ComposeResult:
        """
        Composes the display
        """
        self._container: Vertical = Vertical()
        self._instructions_widget: Static = Static(self._instructions_text)
        self._input_widget: Union[Validated_Input, Input] = (
            Validated_Input(validators=self._validators)
            if self._validators
            else Input()
        )

        with self._container:
            yield self._instructions_widget
            yield self._input_widget

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """
        Called when the input widget is submitted with the enter key.

        Returns the input value if validation is successful and dismisses.
        """

        if self._validators and not event.validation_result.is_valid:
            return

        self.dismiss(self._input_widget.value)

    def action_exit_popup(self) -> None:
        """
        Called when the escape key is pressed.

        Returns none and dismisses.
        """

        self.dismiss(None)
