# expense_tracker/model/merchant_database.py

from expense_tracker.model.database import Database

from typing import Optional


class Merchant_Database:
    """
    Merchant sub commands
    """

    @staticmethod
    def create(database: Database, name: str) -> None:
        """
        Create a new merchant.
        """

        database.execute_query(
            "INSERT INTO merchants (name) VALUES (?)",
            (name,),
        )

    @staticmethod
    def get_all(database: Database) -> list:
        """
        List all merchants in database
        """

        return database.fetchall_query("SELECT id, name FROM merchants", ())

    @staticmethod
    def get_filterd_by_name(database: Database, filter: str) -> list:
        """
        List merchants in database filtered by name
        """

        return database.fetchall_query(
            "SELECT id, name FROM merchants WHERE name LIKE (?)",
            (f"%{filter}%",),
        )

    @staticmethod
    def get_filterd_by_id(database: Database, filter: str) -> list:
        """
        List merchants in database filtered by id.
        """

        return database.fetchall_query(
            "SELECT id, name FROM merchants WHERE id = (?)",
            (filter,),
        )

    @staticmethod
    def delete(database: Database, id: int) -> list:
        """
        Delete a merchant in database by id.
        """

        database.execute_query(
            "DELETE FROM merchants WHERE id = (?)",
            (id,),
        )
