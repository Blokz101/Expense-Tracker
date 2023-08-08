# expense_tracker/view/transaction_table.py

from enum import Enum

from textual.validation import Number

from expense_tracker.view.exptrack_data_table import Exptrack_Data_Table
from expense_tracker.view.text_input_popup import Text_Input_Popup

from expense_tracker.presenter.transaction import Transaction


class Transaction_Table(Exptrack_Data_Table):
    """
    TODO Fill this in
    """

    def __init__(self) -> None:
        column_info_list: list[Exptrack_Data_Table.Column_Info] = [
            Exptrack_Data_Table.Column_Info(
                "Status", Transaction.Column.RECONCILED_STATUS, None
            ),
            Exptrack_Data_Table.Column_Info(
                "Description",
                Transaction.Column.DESCRIPTION,
                lambda: Text_Input_Popup("Input a description"),
            ),
            Exptrack_Data_Table.Column_Info(
                "Merchant", Transaction.Column.MERCHANT, None
            ),
            Exptrack_Data_Table.Column_Info("Date", Transaction.Column.DATE, None),
            Exptrack_Data_Table.Column_Info("Tags", Transaction.Column.TAGS, None),
            Exptrack_Data_Table.Column_Info(
                "Amount",
                Transaction.Column.AMOUNT,
                lambda: Text_Input_Popup(
                    "Input an expense amount",
                    validators=Number(failure_description="Input must be a float"),
                ),
            ),
        ]
        super().__init__(column_info_list)
