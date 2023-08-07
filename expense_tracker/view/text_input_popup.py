# expense_tracker/view/text_input_popup.py

from textual.app import ComposeResult
from textual.widgets import Input, Static
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.validation import Validator
from textual.css.query import NoMatches

from typing import Optional


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

        .valid #validation_status {
            color: $primary;
        }

        #validation_status {
            color: $error;
        }
    """

    BINDINGS: list[tuple[str, str, str]] = [
        ("escape", "exit_popup", "Dismiss popup"),
    ]

    def __init__(
        self,
        instructions: str = "Enter a value",
        placeholder: str = "",
        validators: list[Validator] = [],
        default: Optional[str] = None,
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        self._instructions_text: str = instructions
        self._placeholder: str = placeholder
        self._default: Optional[str] = default
        self._validators = validators
        super().__init__(name, id, classes)

    def compose(self) -> ComposeResult:
        self._container: Vertical = Vertical()
        self._instructions_widget: Static = Static(self._instructions_text)
        self._validation_status_widget: Static = Static(id="validation_status")
        self._input_widget: Input = Input(
            placeholder=self._placeholder, validators=self._validators
        )

        with self._container:
            yield self._instructions_widget
            yield self._input_widget

    def on_input_changed(self, event: Input.Changed) -> None:
        """
        Called when the input widget is changed.

        Updates the validation status widget if the input is valid.
        """

        if self._validators:
            # If the validation status widget is not mounted mount it
            try:
                self.query_one("#validation_status", Static)
            except NoMatches:
                self._container.mount(self._validation_status_widget)

            # Update the validation status widget
            if not event.validation_result.is_valid:
                self._validation_status_widget.update(
                    event.validation_result.failure_descriptions[0]
                )
                self.remove_class("valid")
            else:
                self._validation_status_widget.update("Input is valid")
                self.add_class("valid")

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
