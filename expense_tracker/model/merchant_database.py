# expense_tracker/model/merchant_database.py

from expense_tracker.model.database_utils import Database_Utils


class Merchant_Database:
    """
    Merchant sub commands
    """

    @staticmethod
    def create_merchant(path: str, name: str) -> None:
        """
        Create a new merchant
        """

        connection, cursor = Database_Utils._connect_to_database(path)

        cursor.execute(
            "INSERT INTO merchants (name) values (?)",
            (name,),
        )

        connection.commit()
        connection.close()
