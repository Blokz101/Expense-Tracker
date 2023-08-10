# expense_tracker/view/transaction_table.py

from enum import Enum
from typing import Optional

from textual.validation import Number, Regex

from textual.widgets.selection_list import Selection

from expense_tracker.view.exptrack_data_table import Exptrack_Data_Table
from expense_tracker.view.text_input_popup import Text_Input_Popup
from expense_tracker.view.options_input_popup import Options_Input_Popup
from expense_tracker.view.toggle_input_popup import Toggle_Input_Popup
from expense_tracker.view.selector import Selector

from expense_tracker.constants import Constants

from expense_tracker.presenter.transaction import Transaction
from expense_tracker.presenter.merchant import Merchant
from expense_tracker.presenter.tag import Tag


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
            Exptrack_Data_Table.Column_Info(
                "Tags",
                Transaction.Column.TAGS,
                Toggle_Input_Popup,
            ),
            Exptrack_Data_Table.Column_Info(
                "Amount",
                Transaction.Column.AMOUNT,
                Text_Input_Popup,
            ),
        ]
        super().__init__(column_info_list)

    def request_popup_args(self, popup_column: any, id: int) -> Optional[list[any]]:
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
                    for merchant in Merchant.get_all()
                ),
                "Select a merchant",
            ]

        if popup_column == Transaction.Column.TAGS:
            selected_tag_list: list[tuple[int, ...]] = Tag.get_tags_from_transaction(id)
            selected_tag_id_list: list[int] = list(tag[0] for tag in selected_tag_list)

            tag_list: list[tuple[int, ...]] = []

            for tag in Tag.get_all():
                tag_list.append(
                    Selection(tag[1], tag[0], tag[0] in selected_tag_id_list)
                )

            return [
                tag_list,
                "Select tags",
            ]

        return super().request_popup_args(popup_column)
