# expense_tracker/view/table_info.py

from __future__ import annotations

from dataclasses import dataclass
from expense_tracker.presenter.presenter import Presenter


@dataclass
class Table_Info:
    """
    Dataclass that holds all the info needed for a table
    """

    name: str
    presenter: Presenter
    popup_factories: Popup_Factories
    column_list: list[Column_Info]


@dataclass
class Popup_Factories:
    """
    Dataclass that holds the different popups for each table action
    """

    create: any = None
    detailed_data: any = None
    delete: any = None


@dataclass
class Column_Info:
    """
    Dataclass that hold all the info needed to create each column
    """

    display_name: str
    column_variable: int
    popup_factory: any
    hidden: bool = False
