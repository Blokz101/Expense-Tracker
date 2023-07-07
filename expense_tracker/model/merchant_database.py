# expense_tracker/model/merchant_database.py

from expense_tracker.model.database_utils import Database_Utils
from expense_tracker.model.querys import Execute_Query, Fetchall_Query

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

        Execute_Query(
            database_path,
            "INSERT INTO merchants (name) VALUES (?)",
            (name,),
        )

    @staticmethod
    def get_all(database_path: str) -> list:
        """
        List all merchants in database
        """

        return Fetchall_Query(
            database_path, "SELECT id, name FROM merchants", ()
        ).result

    @staticmethod
    def get_filterd_by_name(database_path: str, filter: str) -> list:
        """
        List all merchants in database
        """

        return Fetchall_Query(
            database_path,
            "SELECT id, name FROM merchants WHERE name LIKE (?)",
            (f"%{filter}%",),
        ).result
