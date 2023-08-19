# expense_tracker/view/table/transaction_table.py

from enum import Enum
from typing import Any, Optional
from textual.screen import ModalScreen
from textual.validation import Number
from textual.widgets.selection_list import Selection

from expense_tracker.presenter.transaction import Transaction
from expense_tracker.presenter.merchant import Merchant
from expense_tracker.presenter.tag import Tag
from expense_tracker.presenter.account import Account

from expense_tracker.view.table.exptrack_data_table import Exptrack_Data_Table
from expense_tracker.view.popup.text_input_popup import Text_Input_Popup
from expense_tracker.view.popup.options_input_popup import Options_Input_Popup
from expense_tracker.view.popup.toggle_input_popup import Toggle_Input_Popup
from expense_tracker.view.popup.detailed_data_popup import Detailed_Data_Popup
from expense_tracker.view.selector import Selector
from expense_tracker.view.popup.transaction_create_popup import Transaction_Create_Popup
from expense_tracker.view.popup.photo_import_popup import Photo_Import_Popup
from expense_tracker.view.popup.date_input_popup import Date_Input_Popup
from expense_tracker.view.popup.begin_reconcile_popup import Begin_Reconcile_Popup


class Transaction_Table(Exptrack_Data_Table):
    """
    Table of transactions
    """

    BINDINGS: list[tuple[str, str, str]] = [
        ("i", "import", "Import"),
        ("r", "reconcile", "Reconcile"),
    ]

    COLUMN_LIST: list[tuple[str, Enum, bool]] = [
        ("ID", Transaction.Column.ID),
        ("Status", Transaction.Column.RECONCILED_STATUS),
        ("Account", Transaction.Column.ACCOUNT),
        ("Description", Transaction.Column.DESCRIPTION),
        ("Merchant", Transaction.Column.MERCHANT),
        ("Date", Transaction.Column.DATE),
        ("Tags", Transaction.Column.TAGS),
        ("Amount", Transaction.Column.AMOUNT),
    ]

    def __init__(
        self,
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        super().__init__(Transaction, Transaction_Table.COLUMN_LIST, name, id, classes)

    def action_create(self) -> None:
        """
        Called when c is pressed.
        """

        self.app.push_screen(Transaction_Create_Popup(self))

    def action_import(self) -> None:
        """
        Mount an import popup
        """

        self.app.push_screen(Photo_Import_Popup(self))

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

    def action_reconcile(self) -> None:
        """
        Called when r is pressed, beings a reconcile.
        """

        self.app.push_screen(Begin_Reconcile_Popup())

    def get_input_popup(self, column: str, id: int) -> Optional[ModalScreen]:
        """
        Get the input popup based on the column
        """

        if column == Transaction.Column.ACCOUNT:
            return Options_Input_Popup(
                list(
                    Selector.Option(account[1], account[0])
                    for account in Account.get_all()
                )
            )

        if column == Transaction.Column.DESCRIPTION:
            return Text_Input_Popup(instructions="Input a description")

        if column == Transaction.Column.MERCHANT:
            return Options_Input_Popup(
                list(
                    Selector.Option(merchant[1], merchant[0])
                    for merchant in Merchant.get_all()
                ),
                instructions="Select a merchant",
            )

        if column == Transaction.Column.DATE:
            return Date_Input_Popup()

        if column == Transaction.Column.TAGS:
            selected_tag_list: list[tuple[str, ...]] = (
                Tag.get_tags_for_transaction(id) if id else Tag.get_all()
            )
            selected_tag_id_list: list[int] = list(tag[0] for tag in selected_tag_list)

            tag_list: list[tuple[str, ...]] = []

            for tag in Tag.get_all():
                tag_list.append(
                    Selection(tag[1], tag[0], tag[0] in selected_tag_id_list)
                )

            return Toggle_Input_Popup(tag_list, instructions="Select tags")

        if column == Transaction.Column.AMOUNT:
            return Text_Input_Popup(
                instructions="Input an expense amount",
                validators=[Number(failure_description="Input must be a float")],
            )

        return super().get_input_popup(column, id)
