# expense_tracker/view/popup/date_input_popup.py

from textual.app import ComposeResult
from textual.widgets import Input, Static
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.validation import Regex
from textual.css.query import NoMatches

from expense_tracker.constants import Constants
from datetime import datetime

from typing import Optional


class Date_Input_Popup(ModalScreen[Optional[datetime]]):
    """
    Popup that prompts the user for a date input.
    """

    DEFAULT_CSS: str = """
        Date_Input_Popup {
            align: center middle;
        }

        Date_Input_Popup > Vertical {
            width: 60;
            height: auto;
            background: $surface;
            padding: 1;
        }

        Date_Input_Popup > Vertical > Input {
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
        instructions: str = "Input a date",
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

    def compose(self) -> ComposeResult:
        """
        Composes the display
        """
        self._container: Vertical = Vertical()
        self._instructions_widget: Static = Static(self._instructions_text)
        self._validation_status_widget: Static = Static(id="validation_status")
        self._input_widget: Input = Input(
            validators=[
                Regex(
                    Constants.DATE_REGEX,
                    failure_description="Input must match mm/dd/yyyy format",
                )
            ]
        )

        with self._container:
            yield self._instructions_widget
            yield self._input_widget

    def on_input_changed(self, event: Input.Changed) -> None:
        """
        Called when the input widget is changed.

        Updates the validation status widget if the input is valid.
        """

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

        if not event.validation_result.is_valid:
            return

        self.dismiss(
            datetime.strptime(self._input_widget.value, Constants.DATE_STRPTIME)
        )

    def action_exit_popup(self) -> None:
        """
        Called when the escape key is pressed.

        Returns none and dismisses.
        """

        self.dismiss(None)
