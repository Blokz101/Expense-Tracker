# expense_tracker/view/validated_input.py

from textual.app import ComposeResult

from typing import Iterable, Union, Optional

from textual.widget import Widget
from textual.widgets import Static, Input
from textual.containers import Vertical
from textual.validation import Validator
from textual.css.query import NoMatches

from typing import Optional


class Validated_Input(Widget):
    """
    Input with a validation status below it.
    """

    DEFAULT_CSS = """
        Validated_Input, Validated_Input > Vertical{
            height: auto;
        }
    """

    def __init__(
        self,
        placeholder: str = "",
        validators: Optional[Union[Validator, Iterable[Validator]]] = None,
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        """
        Initializes the widget.

        Args:
            placeholder: Placeholder text.
            validators: Validators that validate the widget.
            name: The name of the widget.
            id: The ID of the widget in the DOM.
            classes: The CSS classes for the widget.
        """

        self._validation_status_widget: Static = Static(id="validation_status")
        self._input_widget: Input = Input(
            placeholder=placeholder, validators=validators
        )
        self._container: Vertical = Vertical()

        super().__init__(name=name, id=id, classes=classes)

    def compose(self) -> ComposeResult:
        """
        Composes the widget.

        Return: Result of the compose.
        """

        with self._container:
            yield self._input_widget
            yield self._validation_status_widget

    def on_input_changed(self, event: Input.Changed) -> None:
        """
        Called when the input widget is changed, updates the validation status widget if the input is valid.

        Args:
            event: Event that this function is being called in response to.
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
            self._container.remove_class("valid")
        else:
            self._validation_status_widget.update("Input is valid")
            self._container.add_class("valid")
