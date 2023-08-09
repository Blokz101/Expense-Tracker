# expense_tracker/view/transaction_table.py

from enum import Enum
from typing import Optional

from textual.validation import Number, Regex

from expense_tracker.view.exptrack_data_table import Exptrack_Data_Table
from expense_tracker.view.text_input_popup import Text_Input_Popup
from expense_tracker.view.options_input_popup import Options_Input_Popup
from expense_tracker.view.selector import Selector

from expense_tracker.constants import Constants

from expense_tracker.presenter.transaction import Transaction
from expense_tracker.presenter.merchant import Merchant


class Transaction_Table(Exptrack_Data_Table):
    """
    Table that displays and allows editing of transactions.
    """

    def __init__(self) -> None:
        column_info_list: list[Exptrack_Data_Table.Column_Info] = [
            Exptrack_Data_Table.Column_Info(
                "Status", Transaction.Column.RECONCILED_STATUS, None
            ),
            Exptrack_Data_Table.Column_Info(
                "Description",
                Transaction.Column.DESCRIPTION,
                Text_Input_Popup,
            ),
            Exptrack_Data_Table.Column_Info(
                "Merchant",
                Transaction.Column.MERCHANT,
                Options_Input_Popup,
            ),
            Exptrack_Data_Table.Column_Info(
                "Date",
                Transaction.Column.DATE,
                Text_Input_Popup,
            ),
            Exptrack_Data_Table.Column_Info("Tags", Transaction.Column.TAGS, None),
            Exptrack_Data_Table.Column_Info(
                "Amount",
                Transaction.Column.AMOUNT,
                Text_Input_Popup,
            ),
        ]
        super().__init__(column_info_list)

    def request_popup_args(self, popup_column: any) -> Optional[list[any]]:
        """
        Returns the arguments that are required to deal with different popup columns.
        """

        if popup_column == Transaction.Column.DESCRIPTION:
            return ["Input a description"]

        if popup_column == Transaction.Column.DATE:
            return [
                "Input a date",
                Regex(
                    Constants.DATE_REGEX,
                    failure_description="Input must match mm/dd/yyyy format",
                ),
            ]

        if popup_column == Transaction.Column.AMOUNT:
            return [
                "Input an expense amount",
                Number(failure_description="Input must be a float"),
            ]

        if popup_column == Transaction.Column.MERCHANT:
            return [
                list(
                    Selector.Option(merchant[1], merchant[0])
                    for merchant in Merchant.get_display_list()
                ),
                "Select a merchant",
            ]

        return super().request_popup_args(popup_column)
