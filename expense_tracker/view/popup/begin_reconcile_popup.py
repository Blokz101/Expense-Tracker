# expense_tracker/view/popup/begin_reconcile_popup.py

from textual.app import ComposeResult

from textual.binding import Binding

from expense_tracker.view.popup.popup_utils import Popup_Utils

from expense_tracker.view.selector import Selector
from expense_tracker.view.validated_input import Validated_Input

from expense_tracker.presenter.account import Account
from expense_tracker.presenter.reconcile import Reconcile

from expense_tracker.view.popup.reconcile_popup import Reconcile_Popup

from textual.screen import ModalScreen
from textual.widgets import Static, Input, Button
from textual.containers import Vertical
from textual.validation import Function

from typing import Optional


class Begin_Reconcile_Popup(ModalScreen):
    """
    ! TODO Fix this class, it is a work around solution and does not really fit the style of the rest of the program
    """

    DEFAULT_CSS: str = """
        Begin_Reconcile_Popup {
            align: center middle;
        }

        Begin_Reconcile_Popup > Vertical {
            width: 60;
            height: auto;
            background: $surface;
            padding: 1;
        }

        Begin_Reconcile_Popup > Vertical > * {
            margin-top: 1;
        }

        Begin_Reconcile_Popup > Vertical {
            border: $error;
        }

        .valid > Vertical {
            border: $primary;
        }
    """

    BINDINGS: list[Binding] = [
        Binding("escape", "exit_popup", "Dismiss popup"),
    ]

    def __init__(
        self,
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        """
        Constructor
        """

        self.statement_path: Optional[str] = None
        self.account_id: Optional[int] = None

        super().__init__(name, id, classes)

    def compose(self) -> ComposeResult:
        """
        Composes the display
        """
        self._container: Vertical = Vertical()
        self._statement_text: Static = Static("Input a statement path")
        self._account_text: Static = Static("Select an account")
        self._input_widget: Validated_Input = Validated_Input(
            [
                Function(Popup_Utils._file_exists, "File does not exist"),
                Function(Popup_Utils._file_is_csv, "File must be in csv format"),
            ]
        )
        self._selector: Selector = Selector(
            list(
                Selector.Option(account[1], account[0]) for account in Account.get_all()
            )
        )
        self._button: Button = Button("Submit")

        with self._container:
            yield self._statement_text
            yield self._input_widget
            yield self._account_text
            yield self._selector
            yield self._button

    def on_mount(self) -> None:
        """
        TODO Fill this in
        """
        if Reconcile.ongoing_session():
            self.dismiss()
            self.app.push_screen(Reconcile_Popup())

    def action_exit_popup(self) -> None:
        """
        Called when the escape key is pressed.

        Returns none and dismisses.
        """

        self.dismiss(None)

    def submittable(self) -> bool:
        """
        If all the values are filled and the create popup can be submitted.

        Return: If all the values have some value.
        """
        return self.account_id and self.statement_path

    def on_input_changed(self, event: Input.Changed) -> None:
        """
        TODO Fill this out
        """

        if event.validation_result and event.validation_result.is_valid:
            self.statement_path = event.value
        else:
            self.statement_path = None
        self._update_valid_class()

    def on_selector_submitted(self, event: Selector.Submitted) -> None:
        """
        TODO Fill this in
        """
        self.account_id = event.option_id
        self._update_valid_class()

    def _update_valid_class(self) -> None:
        """
        TODO Fill this in
        """

        if self.submittable():
            self.add_class("valid")
        else:
            self.remove_class("valid")

    def on_button_pressed(self) -> None:
        """
        TODO Fill this in
        """

        if self.submittable():
            self.dismiss()
            self.app.push_screen(
                Reconcile_Popup(
                    Popup_Utils._get_path(self.statement_path), self.account_id
                )
            )
