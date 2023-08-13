# expense_tracker/view/table/location_table.py

from enum import Enum
from typing import Optional
from textual.screen import ModalScreen
from textual.validation import Number

from expense_tracker.presenter.location import Location
from expense_tracker.presenter.merchant import Merchant

from expense_tracker.view.table.exptrack_data_table import Exptrack_Data_Table
from expense_tracker.view.popup.text_input_popup import Text_Input_Popup
from expense_tracker.view.popup.options_input_popup import Options_Input_Popup
from expense_tracker.view.popup.detailed_data_popup import Detailed_Data_Popup
from expense_tracker.view.selector import Selector
from expense_tracker.view.popup.create_popup import Create_Popup


class Location_Table(Exptrack_Data_Table):
    """
    Table of locations
    """

    COLUMN_LIST: list[tuple[str, Enum]] = [
        ("ID", Location.Column.ID),
        ("Merchant", Location.Column.MERCHANT),
        ("Name", Location.Column.NAME),
        ("Latitude", Location.Column.XCOORD),
        ("Longitude", Location.Column.YCOORD),
    ]

    def __init__(
        self,
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        super().__init__(
            Location, Location_Table.COLUMN_LIST, name=name, id=id, classes=classes
        )

    def action_create(self) -> None:
        """
        Called when c is pressed.
        """

        self.app.push_screen(Create_Popup(self))

    def action_expand(self) -> None:
        """
        Show a detailed data popup
        """

        self.app.push_screen(
            Detailed_Data_Popup(
                self.coordinate_to_cell_key(self.cursor_coordinate).row_key.value, self
            )
        )

    def action_delete(self) -> None:
        """
        Called when d is pressed.
        """

        return

    def get_input_popup(self, column: str, id: int) -> Optional[ModalScreen]:
        """
        Get the input popup based on the column
        """

        if column == Location.Column.MERCHANT:
            return Options_Input_Popup(
                list(
                    Selector.Option(merchant[1], merchant[0])
                    for merchant in Merchant.get_all()
                ),
                instructions="Select a merchant",
            )

        if column == Location.Column.NAME:
            return Text_Input_Popup(instructions="Input a name")

        if column == Location.Column.XCOORD:
            return Text_Input_Popup(
                instructions="Input a latitude",
                validators=[Number(failure_description="Input must be a float")],
            )

        if column == Location.Column.YCOORD:
            return Text_Input_Popup(
                instructions="Input a longitude",
                validators=[Number(failure_description="Input must be a float")],
            )

        return super().get_input_popup(column, id)
