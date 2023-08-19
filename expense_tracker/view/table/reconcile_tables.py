# expense_tracker/view/table/reconcile_tables.py

from enum import Enum
from typing import Optional, Union
from expense_tracker.presenter.presenter import Presenter

from expense_tracker.view.table.exptrack_data_table import Exptrack_Data_Table
from expense_tracker.presenter.reconcile import Reconcile


class Reconcile_Table(Exptrack_Data_Table):
    """
    TODO Fill this in
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
        super().__init__(Reconcile, Reconcile_Table.COLUMN_LIST, name, id, classes)

    def _get_row_data(self) -> list[tuple[str, ...]]:
        return self.presenter.get_statement_list()


class Possible_Match_Table(Exptrack_Data_Table):
    """
    TODO Fill this in
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
        return self.presenter.get_error_list()


class Orphan_Table(Exptrack_Data_Table):
    """
    TODO Fill this in
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
