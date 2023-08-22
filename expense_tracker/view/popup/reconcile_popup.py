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
    TODO Fill this in
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
        Binding("q", "kill_session", "Kill reconcile session"),
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
        TODO Fill this in
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
        TODO Fill this in
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
        TODO Fill this in
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
        TODO Fill this in
        """
        Reconcile.kill_session()
        self.dismiss(None)
        self.app.notify("Killed session")
