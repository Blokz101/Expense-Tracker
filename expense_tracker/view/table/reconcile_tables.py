# expense_tracker/view/table/reconcile_tables.py

from enum import Enum
from typing import Optional

from textual.screen import ModalScreen
from textual.events import Click

from expense_tracker.view.selector import Selector
from expense_tracker.presenter.merchant import Merchant
from expense_tracker.view.table.exptrack_data_table import Exptrack_Data_Table
from expense_tracker.presenter.reconcile import Reconcile
from expense_tracker.view.popup.options_input_popup import Options_Input_Popup


class Reconcile_Table(Exptrack_Data_Table):
    """
    Table that shows the statement and matched database transactions.
    """

    COLUMN_LIST: list[tuple[str, Enum]] = [
        ("ST ID", Reconcile.Full_Column.ST_ID),
        ("ST Description", Reconcile.Full_Column.ST_DESCRIPTION),
        ("ST Merchant", Reconcile.Full_Column.ST_MERCHANT),
        ("ST Date", Reconcile.Full_Column.ST_DATE),
        ("ST Amount", Reconcile.Full_Column.ST_AMOUNT),
        ("DB ID", Reconcile.Full_Column.DB_ID),
        ("DB Description", Reconcile.Full_Column.DB_DESCRIPTION),
        ("DB Merchant", Reconcile.Full_Column.DB_MERCHANT),
        ("DB Date", Reconcile.Full_Column.DB_DATE),
        ("DB Amount", Reconcile.Full_Column.DB_AMOUNT),
    ]

    def __init__(
        self,
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        """
        Constructor

        Args:
            name: The name of the screen.
            id: The ID of the screen in the DOM.
            classes: The CSS classes for the screen.
        """

        super().__init__(Reconcile, Reconcile_Table.COLUMN_LIST, name, id, classes)

    def _get_row_data(self) -> list[tuple[str, str, str, str, str, str, str, str]]:
        """
        Gets the row data from presenter.

        Return: List of row data in displayable format.
        """

        return self.presenter.get_statement_list()

    def get_input_popup(self, column: str, id: int) -> Optional[ModalScreen]:
        """
        Get the input popup based on the column.

        Args:
            column: Column that the popup should be able to respond to.
            id: ID of the row that was clicked.

        Return: Popup in the form of a ModalScreen if one exists for the column. If there is no popup, then the column cannot be edited by the user.
        """

        if column == Reconcile.Full_Column.ST_MERCHANT:
            return Options_Input_Popup(
                list(
                    Selector.Option(merchant[1], merchant[0])
                    for merchant in Merchant.get_all()
                ),
                instructions="Select a merchant",
            )

        return super().get_input_popup(column, id)

    def on_exptrack_data_table_data_edited(
        self, message: Exptrack_Data_Table.Data_Edited
    ) -> None:
        """
        Called when table data is edited.

        Refreshes the view with the new data.
        """
        self.parent.parent.refresh_data()


class Possible_Match_Table(Exptrack_Data_Table):
    """
    Table that shows the possible matches of statement transactions that are not yet matched.
    """

    COLUMN_LIST: list[tuple[str, Enum]] = [
        ("ST ID", Reconcile.Full_Column.ST_ID),
        ("ST Description", Reconcile.Full_Column.ST_DESCRIPTION),
        ("ST Merchant", Reconcile.Full_Column.ST_MERCHANT),
        ("ST Date", Reconcile.Full_Column.ST_DATE),
        ("ST Amount", Reconcile.Full_Column.ST_AMOUNT),
        ("DB ID", Reconcile.Full_Column.DB_ID),
        ("DB Description", Reconcile.Full_Column.DB_DESCRIPTION),
        ("DB Merchant", Reconcile.Full_Column.DB_MERCHANT),
        ("DB Date", Reconcile.Full_Column.DB_DATE),
        ("DB Amount", Reconcile.Full_Column.DB_AMOUNT),
    ]

    def __init__(
        self,
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        super().__init__(Reconcile, Possible_Match_Table.COLUMN_LIST, name, id, classes)

    def _get_row_data(self) -> list[tuple[str, ...]]:
        return self.presenter.get_possible_match_list()

    def get_input_popup(self, column: str, id: int) -> Optional[ModalScreen]:
        """
        Get the input popup based on the column
        """

        if column == Reconcile.Full_Column.ST_MERCHANT:
            return Options_Input_Popup(
                list(
                    Selector.Option(merchant[1], merchant[0])
                    for merchant in Merchant.get_all()
                ),
                instructions="Select a merchant",
            )

        return super().get_input_popup(column, id)

    def on_exptrack_data_table_data_edited(
        self, message: Exptrack_Data_Table.Data_Edited
    ) -> None:
        """
        Called when table data is edited.

        Refreshes the view with the new data.
        """
        self.parent.parent.refresh_data()


class Orphan_Table(Exptrack_Data_Table):
    """
    Table that displays the orphans of the reconcile session.
    """

    COLUMN_LIST: list[tuple[str, Enum]] = [
        ("ST ID", Reconcile.Full_Column.ST_ID),
        ("ST Description", Reconcile.Full_Column.ST_DESCRIPTION),
        ("ST Merchant", Reconcile.Full_Column.ST_MERCHANT),
        ("ST Date", Reconcile.Full_Column.ST_DATE),
        ("ST Amount", Reconcile.Full_Column.ST_AMOUNT),
    ]

    def __init__(
        self,
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        super().__init__(Reconcile, Orphan_Table.COLUMN_LIST, name, id, classes)

    def _get_row_data(self) -> list[tuple[str, ...]]:
        return self.presenter.get_orphan_list()
