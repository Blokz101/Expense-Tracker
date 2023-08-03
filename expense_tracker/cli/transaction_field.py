# expense_tracker/cli/transaction_field.py

from __future__ import annotations

from expense_tracker.constants import Field_Constant

from typing import Optional, Any, Tuple


class Transaction_Field:
    def __init__(
        self,
        name: str,
        field_object: Optional[Any],
        input_location_pair: Tuple[str, str],
        key=None,
        index: Optional[int] = None,
    ) -> None:
        """
        Constructor
        """
        self.name: str = name
        self.field_object: Optional[Any] = field_object
        self.key = key
        self.input_location: str = input_location_pair[0]
        self.style = input_location_pair[1]
        self.index = index

    def set_field_object(
        self, new_object: Any, new_input_location_pair: Tuple[str, str]
    ) -> None:
        """
        Set a new field object and input location
        """

        if new_object == None:
            return

        self.field_object = new_object
        self.input_location: str = new_input_location_pair[0]
        self.style = new_input_location_pair[1]

    def __str__(self) -> str:
        """
        Return a string version
        """

        index_str: str = ""
        if self.index:
            index_str = f"[{self.index}] "

        input_location_str: str = "(None)"
        if self.input_location:
            input_location_str = f"({self.input_location}) --> "

        value_str: str = "None"
        if self.field_object:
            if self.key:
                value_str = self.key(self.field_object)
            else:
                value_str = self.field_object

        return f"{index_str}{self.name: <15}{input_location_str}{value_str}"
