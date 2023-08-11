# expense_tracker/view/location_table.py

from typing import Optional

from textual.validation import Number, Regex

from expense_tracker.view.exptrack_data_table import Exptrack_Data_Table
from expense_tracker.view.text_input_popup import Text_Input_Popup
from expense_tracker.view.options_input_popup import Options_Input_Popup
from expense_tracker.view.selector import Selector

from expense_tracker.presenter.merchant import Merchant
from expense_tracker.presenter.location import Location


class Location_Table(Exptrack_Data_Table):
    """
    Table that displays and allows editing of merchant locations.
    """

    class Edit_Request(Exptrack_Data_Table.Edit_Request):
        pass

    def __init__(
        self,
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        column_info_list: list[Exptrack_Data_Table.Column_Info] = [
            Exptrack_Data_Table.Column_Info(
                "Merchant",
                Location.Column.MERCHANT,
                Options_Input_Popup,
            ),
            Exptrack_Data_Table.Column_Info(
                "Name",
                Location.Column.NAME,
                Text_Input_Popup,
            ),
            Exptrack_Data_Table.Column_Info(
                "Latitude",
                Location.Column.XCOORD,
                Text_Input_Popup,
            ),
            Exptrack_Data_Table.Column_Info(
                "Longitude",
                Location.Column.YCOORD,
                Text_Input_Popup,
            ),
        ]
        super().__init__(
            column_info_list, Location.get_all(), name=name, id=id, classes=classes
        )

    def request_popup_args(self, popup_column: any, id: int) -> Optional[list[any]]:
        """
        Returns the arguments that are required to deal with different popup columns.
        """

        if popup_column == Location.Column.MERCHANT:
            return [
                list(
                    Selector.Option(merchant[1], merchant[0])
                    for merchant in Merchant.get_all()
                ),
                "Select a merchant",
            ]

        if popup_column == Location.Column.NAME:
            return ["Input a name"]

        if popup_column == Location.Column.XCOORD:
            return [
                "Input a latitude",
                Number(failure_description="Input must be a float"),
            ]

        if popup_column == Location.Column.YCOORD:
            return [
                "Input a longitude",
                Number(failure_description="Input must be a float"),
            ]

        return super().request_popup_args(popup_column)
