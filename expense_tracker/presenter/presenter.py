# expense_tracker/presenter/presenter.py

from enum import Enum


class Presenter:
    class Column(Enum):
        ID: int = 0

    @staticmethod
    def _format(object_list: any) -> tuple[int, ...]:
        """
        Formats the raw database objects into a tuple
        """

        return []

    @staticmethod
    def get_all() -> list[tuple[int, ...]]:
        """
        Returns a list of all objects in a table
        """

        raise RuntimeError("Presenter class does not implement get_all.")

    @staticmethod
    def get_by_id(id: int) -> tuple[int, ...]:
        """
        Returns a single object with the requested id
        """

        raise RuntimeError("Presenter class does not implement get_by_id.")

    @staticmethod
    def create(values: dict[Enum, any]) -> None:
        """
        Creates a new row in the database
        """

        raise RuntimeError("Presenter class does not implement create.")

    @staticmethod
    def delete(object_id: int) -> None:
        """
        Deletes a row in the database
        """

        raise RuntimeError("Presenter class does not implement delete.")

    @staticmethod
    def set_value(id: int, column: Column, new_value: any) -> any:
        """
        Updates a cell in the database
        """

        if new_value == None:
            raise TypeError("new_value must have a value")

        raise ValueError(f"Unable to handel an edit of database column '{column}'.")

    @staticmethod
    def get_value(value: any, column: Column) -> any:
        """
        Format or get a value based on the column it was requested for
        """

        if value == None:
            raise TypeError("value must have a value")

        raise ValueError(f"Unable to a request for database column '{column}'.")
