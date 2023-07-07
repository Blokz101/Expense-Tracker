# expense_tracker/model/merchant_database.py

from expense_tracker.model.database_utils import Database_Utils
from expense_tracker.model.query import Query

from typing import Optional


class Merchant_Database:
    """
    Merchant sub commands
    """

    @staticmethod
    def create(database_path: str, name: str) -> None:
        """
        Create a new merchant.
        """

        Query.execute(
            database_path,
            "INSERT INTO merchants (name) VALUES (?)",
            (name,),
        )

    @staticmethod
    def get_all(database_path: str) -> list:
        """
        List all merchants in database
        """

        return Query.fetchall(database_path, "SELECT id, name FROM merchants", ())

    @staticmethod
    def get_filterd_by_name(database_path: str, filter: str) -> list:
        """
        List merchants in database filtered by name
        """

        return Query.fetchall(
            database_path,
            "SELECT id, name FROM merchants WHERE name LIKE (?)",
            (f"%{filter}%",),
        )

    @staticmethod
    def get_filterd_by_id(database_path: str, filter: str) -> list:
        """
        List merchants in database filtered by id.
        """

        return Query.fetchall(
            database_path,
            "SELECT id, name FROM merchants WHERE id = (?)",
            (filter,),
        )

    @staticmethod
    def delete(database_path: str, id: int) -> list:
        """
        Delete a merchant in database by id.
        """

        Query.execute(
            database_path,
            "DELETE FROM merchants WHERE id = (?)",
            (id,),
        )
