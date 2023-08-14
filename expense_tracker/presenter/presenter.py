# expense_tracker/presenter/presenter.py

from enum import Enum

from typing import Union

from datetime import datetime


class Presenter:
    """
    Base class that should be extended for specific sql tables. Formats data from the sql database into a displayable format and makes edits to the database for the view.
    """

    class Column(Enum):
        ID: int = 0

    @staticmethod
    def _format(database_object: any) -> tuple[int, ...]:
        """
        Formats the raw database objects into a tuple that the view can parse. Should be extended.

        Args:
            database_object: Sqlalchmey objects to be formatted into a list of strings.

        Returns: Tuple beginning with the object id.
        """

        return []

    @staticmethod
    def get_all() -> list[tuple[int, ...]]:
        """
        Gets all the rows in the sql table. Should be extended.

        Returns: Formatted list of all rows in the sql table

        Throws:
            RuntimeError: If the presenter classes does not implement this method.
        """

        raise RuntimeError("Presenter class does not implement get_all.")

    @staticmethod
    def get_by_id(id: int) -> tuple[int, ...]:
        """
        Returns a single object with the requested id. Should be extended.

        Args:
            id: Row id and id of the database object.

        Throws:
            RuntimeError: If the presenter classes does not implement this method.
        """

        raise RuntimeError("Presenter class does not implement get_by_id.")

    @staticmethod
    def create(values: dict[Enum, Union[int, str, datetime]]) -> None:
        """
        Creates a new row in the database. Should be extended.

        Args:
            values:

        Throws:
            RuntimeError: If the presenter classes does not implement this method.
        """

        raise RuntimeError("Presenter class does not implement create.")

    @staticmethod
    def delete(object_id: int) -> None:
        """
        Deletes a row in the database. Should be extended.

        Throws:
            RuntimeError: If the presenter classes does not implement this method.
        """

        raise RuntimeError("Presenter class does not implement delete.")

    @staticmethod
    def set_value(id: int, column: Column, new_value: Union[int, str, datetime]) -> str:
        """
        Updates a cell in the database. Should be extended.

        When extended, this function should contain many if clauses with code to deal with the specific column and then exit the function.

        Return: The new value in a displayable format.

        Throws:
            TypeError: If new value is None.
            ValueError: If a column is passed in and no statements handel it.
        """

        if new_value == None:
            raise TypeError("new_value must have a value")

        raise ValueError(f"Unable to handel an edit of database column '{column}'.")

    @staticmethod
    def get_value(value: Union[int, str, datetime], column: Column) -> str:
        """
        Format or get a value based on the column it was requested for.

        When extended, this function should contain many if clauses with code to deal with the specific column and then exit the function.

        Return: The value in a displayable format.

        Throws:
            TypeError: If new value is None.
            ValueError: If a column is passed in and no statements handel it.
        """

        if value == None:
            raise TypeError("value must have a value")

        raise ValueError(f"Unable to a request for database column '{column}'.")
