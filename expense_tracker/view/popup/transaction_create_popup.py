# expense_tracker/view/popup/transaction_create_popup.py


from pathlib import Path

from datetime import datetime

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
        excluded_column_key_list: Optional[list[Transaction.Column]] = None,
        import_list: Optional[list[Path]] = None,
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        self.import_photo: Optional[Path] = import_list[0] if import_list else None

        super().__init__(
            parent_table,
            excluded_column_key_list=excluded_column_key_list,
            instructions=f"Import create for {self.import_photo.name}"
            if self.import_photo
            else "Manual create",
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
        
        # Get the possible locations and set them as defaults
        possible_location_id: Optional[int] = Location.possible_location(
            coords, Config_Manager().get_same_merchant_mile_radius()
        )
        if not possible_location_id:
            return

        self.values[Transaction.Column.MERCHANT].value = possible_location_id
        self.values[Transaction.Column.MERCHANT].input_method = Input_Method.PHOTO

        # If a merchant was found then get the default tags if there are any and set them
        default_tag_id_list: list[int] = list(
            tag[0]
            for tag in Tag.get_tags_for_merchant_default(
                self.values[Transaction.Column.MERCHANT].value
            )
        )
        
        # If there are no default tags then done set the value
        if not default_tag_id_list:
            return
        
        self.values[Transaction.Column.TAGS].value = default_tag_id_list
        self.values[Transaction.Column.TAGS].input_method = Input_Method.PHOTO

    def action_submit(self) -> None:
        """
        Called when the user presses enter

        Submits the popup or jumps to the next empty field if there is one
        """

        submit_succeeded: bool = super().action_submit()

        if submit_succeeded and self.import_photo:
            Photo_Manager.archive_photo(
                self.import_photo,
                Config_Manager().get_photo_archive_path() / self.import_photo.name,
            )

        if submit_succeeded and len(self.import_list) > 1:
            self.app.push_screen(
                Transaction_Create_Popup(
                    self.parent_table,
                    excluded_column_key_list=self.excluded_column_key_list,
                    import_list=self.import_list[1:],
                )
            )

    def get_input_popup(self, column: str, id: int) -> Optional[ModalScreen]:
        """
        Gets the input popup to use for each column
        """
        if column == Transaction.Column.TAGS:
            
            # If the tags are at None or their default value, then convert them to an empty list for ease of processing
            selected_tag_id_list: list[int] = self.values[Transaction.Column.TAGS].value
            if not selected_tag_id_list:
                selected_tag_id_list = []

            # Convert tags into selection objects for the selector widget in Toggle_Input_Popup
            tag_list: list[tuple[str, ...]] = []
            for tag in Tag.get_all():
                tag_list.append(
                    Selection(tag[1], tag[0], tag[0] in selected_tag_id_list)
                )

            return Toggle_Input_Popup(tag_list, instructions="Select tags")

        return super().get_input_popup(column, id)
