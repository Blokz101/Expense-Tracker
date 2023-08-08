# expense_tracker/view/transaction_table.py

from typing_extensions import Literal
from expense_tracker.view.exptrack_data_table import Exptrack_Data_Table


class Transaction_Table(Exptrack_Data_Table):
    def __init__(self) -> None:
        """
        TODO Fill this out
        """

        column_info_list: list[Exptrack_Data_Table.Column_Info] = [
            Exptrack_Data_Table.Column_Info("reconciled_status", "Status", None),
            Exptrack_Data_Table.Column_Info("description", "Description", None),
            Exptrack_Data_Table.Column_Info("merchant", "Merchant", None),
            Exptrack_Data_Table.Column_Info("date", "Date", None),
            Exptrack_Data_Table.Column_Info("No Clue", "Tags", None),
            Exptrack_Data_Table.Column_Info("amount", "Amount", None),
        ]

        table_name: Exptrack_Data_Table.Table_Info = Exptrack_Data_Table.Table_Info(
            "transactions", "Transactions"
        )
        super().__init__(column_info_list, table_name)
