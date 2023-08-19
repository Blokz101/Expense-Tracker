# expense_tracker/view/popup/reconcile_popup.py

from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Static
from textual.containers import Grid
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
    ]

    def __init__(
        self,
        statement_path: Path,
        account_id: int,
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        """
        TODO Fill this in
        """
        super().__init__(name, id, classes)

        Reconcile.new_session(statement_path, account_id)

    def compose(self) -> ComposeResult:
        """
        TODO Fill this in
        """

        self._container: Grid = Grid()
        self._reconcile_table: Reconcile_Table = Reconcile_Table()
        # self._possible_match_table: Possible_Match_Table = Possible_Match_Table()
        # self._orphan_table: Orphan_Table = Orphan_Table()

        with self._container:
            yield self._reconcile_table
            # yield self._possible_match_table
            # yield self._orphan_table

    def action_exit_popup(self) -> None:
        """
        Called when the escape key is pressed.

        Returns none and dismisses.
        """

        self.dismiss(None)
