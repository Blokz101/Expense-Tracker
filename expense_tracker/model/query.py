# expense_tracker/model/querys.py

from expense_tracker.model.database_utils import Database_Utils


class Query:
    @staticmethod
    def execute(database_path: str, query: str, args: tuple) -> None:
        """
        Execute a query.
        """

        connection, cursor = Database_Utils.connect_to_database(database_path)

        cursor.execute(
            query,
            args,
        )

        connection.commit()
        connection.close()

    @staticmethod
    def fetchall(database_path: str, query: str, args: tuple) -> tuple:
        """
        Execute a query and fetch all the results.
        """

        connection, cursor = Database_Utils.connect_to_database(database_path)

        cursor.execute(
            query,
            args,
        )

        result: tuple = cursor.fetchall()

        connection.commit()
        connection.close()

        return result
