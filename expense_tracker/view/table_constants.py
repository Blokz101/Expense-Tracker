# expense_tracker/view/table_constants.py

from __future__ import annotations

from textual.validation import Number, Regex
from textual.widgets.selection_list import Selection

from expense_tracker.constants import Constants

from expense_tracker.view.text_input_popup import Text_Input_Popup
from expense_tracker.view.options_input_popup import Options_Input_Popup
from expense_tracker.view.toggle_input_popup import Toggle_Input_Popup
from expense_tracker.view.selector import Selector
from expense_tracker.view.detailed_data_popup import Detailed_Data_Popup
from expense_tracker.view.table_info import Table_Info, Column_Info, Popup_Factories

from expense_tracker.presenter.transaction import Transaction
from expense_tracker.presenter.merchant import Merchant
from expense_tracker.presenter.account import Account
from expense_tracker.presenter.location import Location
from expense_tracker.presenter.tag import Tag


def _get_tag_selections(row_id: int) -> list[any]:
    """
    Get the tag selections for a transaction
    """

    selected_tag_list: list[tuple[int, ...]] = Tag.get_tags_from_transaction(row_id)
    selected_tag_id_list: list[int] = list(tag[0] for tag in selected_tag_list)

    tag_list: list[tuple[int, ...]] = []

    for tag in Tag.get_all():
        tag_list.append(Selection(tag[1], tag[0], tag[0] in selected_tag_id_list))

    return tag_list


TRANSACTION: Table_Info = Table_Info(
    "transaction",
    Transaction,
    Popup_Factories(None, lambda id: Detailed_Data_Popup(id, TRANSACTION), None),
    [
        Column_Info("ID", Transaction.Column.ID, None),
        Column_Info("Status", Transaction.Column.RECONCILED_STATUS, None),
        Column_Info(
            "Description",
            Transaction.Column.DESCRIPTION,
            lambda id: Text_Input_Popup(instructions="Input a description"),
        ),
        Column_Info(
            "Merchant",
            Transaction.Column.MERCHANT,
            lambda id: Options_Input_Popup(
                list(
                    Selector.Option(merchant[1], merchant[0])
                    for merchant in Merchant.get_all()
                ),
                instructions="Select a merchant",
            ),
        ),
        Column_Info(
            "Date",
            Transaction.Column.DATE,
            lambda id: Text_Input_Popup(
                instructions="Input a date",
                validators=[
                    Regex(
                        Constants.DATE_REGEX,
                        failure_description="Input must match mm/dd/yyyy format",
                    )
                ],
            ),
        ),
        Column_Info(
            "Tags",
            Transaction.Column.TAGS,
            lambda id: Toggle_Input_Popup(
                _get_tag_selections(id), instructions="Select tags"
            ),
        ),
        Column_Info(
            "Amount",
            Transaction.Column.AMOUNT,
            lambda id: Text_Input_Popup(
                instructions="Input an expense amount",
                validators=[Number(failure_description="Input must be a float")],
            ),
        ),
    ],
)

ACCOUNT: Table_Info = Table_Info(
    "account",
    Account,
    None,
    [
        Column_Info("ID", Transaction.Column.ID, None),
        Column_Info(
            "Name",
            Account.Column.NAME,
            lambda id: Text_Input_Popup(instructions="Input a name"),
        ),
        Column_Info(
            "Description Index",
            Account.Column.DESCRIPTION_COLUMN_INDEX,
            lambda id: Text_Input_Popup(
                instructions="Input an index for the description column on statement",
                validators=[
                    Regex("\d+", failure_description="Input must be a positive integer")
                ],
            ),
        ),
        Column_Info(
            "Amount Index",
            Account.Column.AMOUNT_COLUMN_INDEX,
            lambda id: Text_Input_Popup(
                instructions="Input an index for the amount column on statement",
                validators=[
                    Regex("\d+", failure_description="Input must be a positive integer")
                ],
            ),
        ),
        Column_Info(
            "Date Index",
            Account.Column.DATE_COLUMN_INDEX,
            lambda id: Text_Input_Popup(
                instructions="Input an index for the date column on statement",
                validators=[
                    Regex("\d+", failure_description="Input must be a positive integer")
                ],
            ),
        ),
    ],
)

LOCATION: Table_Info = Table_Info(
    "location",
    Location,
    None,
    [
        Column_Info("ID", Transaction.Column.ID, None),
        Column_Info(
            "Merchant",
            Location.Column.MERCHANT,
            lambda id: Options_Input_Popup(
                list(
                    Selector.Option(merchant[1], merchant[0])
                    for merchant in Merchant.get_all()
                ),
                instructions="Select a merchant",
            ),
        ),
        Column_Info(
            "Name",
            Location.Column.NAME,
            lambda id: Text_Input_Popup(instructions="Input a name"),
        ),
        Column_Info(
            "Latitude",
            Location.Column.XCOORD,
            lambda id: Text_Input_Popup(
                instructions="Input a latitude",
                validators=[Number(failure_description="Input must be a float")],
            ),
        ),
        Column_Info(
            "Longitude",
            Location.Column.YCOORD,
            lambda id: Text_Input_Popup(
                instructions="Input a longitude",
                validators=[Number(failure_description="Input must be a float")],
            ),
        ),
    ],
)

MERCHANT: Table_Info = Table_Info(
    "merchant",
    Merchant,
    None,
    [
        Column_Info("ID", Transaction.Column.ID, None),
        Column_Info(
            "Name",
            Merchant.Column.NAME,
            lambda id: Text_Input_Popup(instructions="Input a name"),
        ),
        Column_Info(
            "Rule",
            Merchant.Column.NAMING_RULE,
            lambda id: Text_Input_Popup(instructions="Input a regular expression"),
        ),
    ],
)

TAG: Table_Info = Table_Info(
    "tag",
    Tag,
    None,
    [
        Column_Info("ID", Transaction.Column.ID, None),
        Column_Info(
            "Name",
            Tag.Column.NAME,
            lambda id: Text_Input_Popup(instructions="Input a name"),
        ),
        Column_Info(
            "Instance Tag",
            Tag.Column.INSTANCE_TAG,
            None,
        ),
    ],
)
