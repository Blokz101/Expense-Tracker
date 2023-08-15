# expense_tracker/view/popup/transaction_create_popup.py


from enum import Enum

from copy import copy

from pathlib import Path

from datetime import datetime

from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets.selection_list import Selection

from expense_tracker.presenter.transaction import Transaction
from expense_tracker.presenter.tag import Tag
from expense_tracker.presenter.location import Location

from expense_tracker.view.popup.toggle_input_popup import Toggle_Input_Popup
from expense_tracker.view.popup.create_popup import Create_Popup, Input_Method
from expense_tracker.view.table.exptrack_data_table import Exptrack_Data_Table

from expense_tracker.model.photo_manager import Photo_Manager

from expense_tracker.config_manager import Config_Manager

from typing import Optional


class Transaction_Create_Popup(Create_Popup):
    """
    Transaction specific create popup
    """

    def __init__(
        self,
        parent_table: Exptrack_Data_Table,
        import_list: Optional[list[Path]] = None,
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        parent_column_list: list[tuple[Enum, any]] = copy(parent_table.column_list)
        parent_column_list.pop(1)

        self.import_photo: Optional[Path] = import_list[0] if import_list else None

        super().__init__(
            parent_table,
            f"Import create for {self.import_photo.name}"
            if self.import_photo
            else "Manual create",
            modified_column_list=parent_column_list,
            name=name,
            id=id,
            classes=classes,
        )

        self.import_list: list[Path] = []
        if import_list:
            self.import_list = import_list

        if self.import_photo:
            self._set_defaults()

    def _set_defaults(self) -> None:
        """
        Finds and sets defaults for each column.
        """

        self.values[
            Transaction.Column.ACCOUNT
        ].value = Config_Manager().get_default_account_id()
        self.values[Transaction.Column.ACCOUNT].input_method = Input_Method.DEFAULT

        description: Optional[str] = Photo_Manager.get_description(self.import_photo)
        if description:
            self.values[Transaction.Column.DESCRIPTION].value = description
            self.values[
                Transaction.Column.DESCRIPTION
            ].input_method = Input_Method.PHOTO

        date: Optional[datetime] = Photo_Manager.get_date(self.import_photo)
        if date:
            self.values[Transaction.Column.DATE].value = date
            self.values[Transaction.Column.DATE].input_method = Input_Method.PHOTO

        # The rest of the conditions from here on out require both coords and a possible location id
        coords: Optional[tuple[float, float]] = Photo_Manager.get_coords(
            self.import_photo
        )
        if not coords:
            return
        possible_location_id: Optional[int] = Location.possible_location(
            coords, Config_Manager().get_same_merchant_mile_radius()
        )
        if not possible_location_id:
            return

        self.values[Transaction.Column.MERCHANT].value = possible_location_id
        self.values[Transaction.Column.MERCHANT].input_method = Input_Method.PHOTO

        default_tag_id_list: list[int] = list(
            tag[0]
            for tag in Tag.get_tags_for_transaction(
                self.values[Transaction.Column.MERCHANT].value
            )
        )
        self.values[Transaction.Column.TAGS].value = default_tag_id_list
        self.values[Transaction.Column.TAGS].input_method = Input_Method.PHOTO

    def action_submit(self) -> None:
        """
        Called when the user presses enter

        Submits the popup or jumps to the next empty field if there is one
        """
        if super().action_submit() and len(self.import_list) > 1:
            self.app.push_screen(
                Transaction_Create_Popup(
                    self.parent_table, import_list=self.import_list[1:]
                )
            )

    def get_input_popup(self, column: str, id: int) -> Optional[ModalScreen]:
        """
        Gets the input popup to use for each column
        """
        if column == Transaction.Column.TAGS:
            selected_tag_list: list[tuple[str, ...]] = Tag.get_tags_for_transaction(
                self.values[Transaction.Column.MERCHANT].value
            )

            selected_tag_id_list: list[int] = list(tag[0] for tag in selected_tag_list)

            tag_list: list[tuple[str, ...]] = []

            for tag in Tag.get_all():
                tag_list.append(
                    Selection(tag[1], tag[0], tag[0] in selected_tag_id_list)
                )

            return Toggle_Input_Popup(tag_list, instructions="Select tags")

        return super().get_input_popup(column, id)
