# expense_tracker/view/popup/reconcile_popup.py

from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Static, Footer
from textual.containers import VerticalScroll
from textual.binding import Binding

from typing import Optional

from expense_tracker.presenter.reconcile import Reconcile

from pathlib import Path

from expense_tracker.view.table.exptrack_data_table import Exptrack_Data_Table
from expense_tracker.view.table.reconcile_tables import (
    Reconcile_Table,
    Possible_Match_Table,
    Orphan_Table,
)


class Reconcile_Popup(ModalScreen):
    """
    Popup that allows the user to reconcile database transactions with a statement.
    """

    DEFAULT_CSS: str = """
        Reconcile_Popup {
            align: center middle;
        }

        Reconcile_Popup > Grid {
            width: 80%;
            height: auto;
            background: $surface;
            padding: 1;
        }
    """

    BINDINGS: list[Binding] = [
        Binding("escape", "exit_popup", "Dismiss popup"),
        Binding("Q", "kill_session", "Kill reconcile session"),
        Binding("S", "commit_reconcile", "Submit reconcile"),
    ]

    def __init__(
        self,
        statement_path: Optional[Path] = None,
        account_id: Optional[int] = None,
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        """
        Constructor

        Args:
            statement_path: Path to the statement csv.
            account_id: ID of the account that the statement belongs to.
            name: The name of the screen.
            id: The ID of the screen in the DOM.
            classes: The CSS classes for the screen.
        """
        super().__init__(name, id, classes)

        if statement_path and account_id:
            Reconcile.new_session(statement_path, account_id)
            return

        if Reconcile.ongoing_session():
            return

        raise RuntimeError(
            "No reconcile session is running and either statement_path or account_id were not provided to the constructor."
        )

    def compose(self) -> ComposeResult:
        """
        Composes the display.
        """

        self._container: VerticalScroll = VerticalScroll()
        self._reconcile_table: Reconcile_Table = Reconcile_Table()
        self._possible_match_table: Possible_Match_Table = Possible_Match_Table()
        self._orphan_table: Orphan_Table = Orphan_Table()

        with self._container:
            yield Static("Statement")
            yield self._reconcile_table
            yield Static("Possible Matches")
            yield self._possible_match_table
            yield Static("Orphan Table")
            yield self._orphan_table
            yield Footer()

    def refresh_data(self) -> None:
        """
        Refreshes the data in each of the tables.
        """

        self._reconcile_table.refresh_data()
        self._possible_match_table.refresh_data()
        self._orphan_table.refresh_data()

    def action_exit_popup(self) -> None:
        """
        Called when the escape key is pressed.

        Returns none and dismisses.
        """

        self.dismiss(None)

    def action_kill_session(self) -> None:
        """
        Called when capital Q is pressed.

        Kills the current session and dismisses popup.
        """
        Reconcile.kill_session()
        self.dismiss(None)
        self.app.notify("Killed session")

    def action_commit_reconcile(self) -> None:
        """
        Attempts to commit the reconcile session.
        """

        if not Reconcile.committable():
            self.notify(
                "Reconcile failed, one or more statements is not matched.",
                severity="error",
            )
            return

        Reconcile.commit()
        Reconcile.kill_session()
        self.dismiss(None)
        self.app.notify("Committed session")
