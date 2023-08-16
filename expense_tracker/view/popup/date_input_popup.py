# expense_tracker/view/popup/date_input_popup.py

from textual.app import ComposeResult
from textual.widgets import Static, Input
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.validation import Function
from textual.css.query import NoMatches

from expense_tracker.view.validated_input import Validated_Input

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
        self._input_widget: Validated_Input = Validated_Input(
            validators=[
                Function(
                    Date_Input_Popup._validate_date,
                    failure_description="Input must match mm/dd/yyyy format and be a valid date",
                )
            ]
        )

        with self._container:
            yield self._instructions_widget
            yield self._input_widget

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """
        Called when the input widget is submitted with the enter key.

        Returns the input value if validation is successful and dismisses.
        """

        if not event.validation_result.is_valid:
            return

        self.dismiss(
            datetime.strptime(
                self._input_widget.value, Constants.USER_INPUT_DATE_FORMAT
            )
        )

    def action_exit_popup(self) -> None:
        """
        Called when the escape key is pressed.

        Returns none and dismisses.
        """

        self.dismiss(None)

    @staticmethod
    def _validate_date(date: str) -> bool:
        """
        Returns true if date is readable and false if not.

        Args:
            date: String to be parsed

        Return: Boolean status of validation
        """

        try:
            datetime.strptime(date, Constants.USER_INPUT_DATE_FORMAT)
            return True
        except ValueError:
            return False
