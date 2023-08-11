# expense_tracker/view/table_constants.py

from typing import Optional

from enum import Enum

from textual.validation import Number, Regex
from textual.widgets.selection_list import Selection

from expense_tracker.constants import Constants

from expense_tracker.view.exptrack_data_table import Exptrack_Data_Table
from expense_tracker.view.text_input_popup import Text_Input_Popup
from expense_tracker.view.options_input_popup import Options_Input_Popup
from expense_tracker.view.toggle_input_popup import Toggle_Input_Popup
from expense_tracker.view.selector import Selector

from expense_tracker.presenter.transaction import Transaction
from expense_tracker.presenter.merchant import Merchant
from expense_tracker.presenter.account import Account
from expense_tracker.presenter.location import Location
from expense_tracker.presenter.tag import Tag

class Table_Constants:
    """
    Constants class that contains all the table info for each table
    """
    
    class Tables(str, Enum):
        TRANSACTION: str = "transaction"
        MERCHANT: str = "merchant"
        TAG: str = "tag"
        LOCATION: str = "location"
        ACCOUNT: str = "account"
    
    transaction_column_list: list[Exptrack_Data_Table.Column_Info] = [
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
    
    @staticmethod
    def transaction_popup_args(popup_column: any, id: int) -> Optional[list[any]]:
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
            
    account_column_list: list[Exptrack_Data_Table.Column_Info] = [
        Exptrack_Data_Table.Column_Info(
            "Name",
            Account.Column.NAME,
            Text_Input_Popup,
        ),
        Exptrack_Data_Table.Column_Info(
            "Description Index",
            Account.Column.DESCRIPTION_COLUMN_INDEX,
            Text_Input_Popup,
        ),
        Exptrack_Data_Table.Column_Info(
            "Amount Index",
            Account.Column.AMOUNT_COLUMN_INDEX,
            Text_Input_Popup,
        ),
        Exptrack_Data_Table.Column_Info(
            "Date Index",
            Account.Column.DATE_COLUMN_INDEX,
            Text_Input_Popup,
        ),
    ]
    
    @staticmethod
    def account_popup_args(popup_column: any, id: int) -> Optional[list[any]]:
        """
        Returns the arguments that are required to deal with different popup columns.
        """

        if popup_column == Account.Column.NAME:
            return ["Input a name"]

        if popup_column == Account.Column.DESCRIPTION_COLUMN_INDEX:
            return [
                "Input an index for the description column on statement",
                Regex("\d+", failure_description="Input must be a positive integer"),
            ]

        if popup_column == Account.Column.AMOUNT_COLUMN_INDEX:
            return [
                "Input an index for the amount column on statement",
                Regex("\d+", failure_description="Input must be a positive integer"),
            ]

        if popup_column == Account.Column.DATE_COLUMN_INDEX:
            return [
                "Input an index for the date column on statement",
                Regex("\d+", failure_description="Input must be a positive integer"),
            ]
            
    location_column_list: list[Exptrack_Data_Table.Column_Info] = [
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
    
    @staticmethod
    def location_popup_args(popup_column: any, id: int) -> Optional[list[any]]:
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
            
    merchant_column_list: list[Exptrack_Data_Table.Column_Info] = [
            Exptrack_Data_Table.Column_Info(
                "Name",
                Merchant.Column.NAME,
                Text_Input_Popup,
            ),
            Exptrack_Data_Table.Column_Info(
                "Rule",
                Merchant.Column.NAMING_RULE,
                Text_Input_Popup,
            ),
        ]
    
    @staticmethod
    def merchant_popup_args(popup_column: any, id: int) -> Optional[list[any]]:
        """
        Returns the arguments that are required to deal with different popup columns.
        """

        if popup_column == Merchant.Column.NAME:
            return ["Input a name"]

        if popup_column == Merchant.Column.NAMING_RULE:
            return ["Input a regular expression"]
        
    tag_column_list: list[Exptrack_Data_Table.Column_Info] = [
            Exptrack_Data_Table.Column_Info(
                "Name",
                Tag.Column.NAME,
                Text_Input_Popup,
            ),
            Exptrack_Data_Table.Column_Info(
                "Instance Tag",
                Tag.Column.INSTANCE_TAG,
                None,
            ),
        ]
    
    @staticmethod
    def tag_popup_args(popup_column: any, id: int) -> Optional[list[any]]:
        """
        Returns the arguments that are required to deal with different popup columns.
        """

        if popup_column == Tag.Column.NAME:
            return ["Input a name"]