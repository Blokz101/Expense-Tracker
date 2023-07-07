# expense_tracker/model/querys.py

from expense_tracker.model.database_utils import Database_Utils


class Execute_Query:
    """
    Defines a query that can be executed with execute_query
    """

    def __init__(self, database_path: str, query: str, args: tuple) -> None:
        """
        Constructor
        """

        self.database_path = database_path
        self.query = query
        self.args = args

        self._execute()

    def _execute(self) -> None:
        """
        Execute the query
        """

        connection, cursor = Database_Utils.connect_to_database(self.database_path)

        cursor.execute(
            self.query,
            self.args,
        )

        connection.commit()
        connection.close()


class Fetchall_Query:
    def __init__(self, database_path: str, query: str, args: tuple) -> None:
        """
        Constructor
        """

        self.database_path = database_path
        self.query = query
        self.args = args

        self.result = self._fetchall()

    def _fetchall(self) -> tuple:
        """
        Execute the query
        """

        connection, cursor = Database_Utils.connect_to_database(self.database_path)

        cursor.execute(
            self.query,
            self.args,
        )

        result: tuple = cursor.fetchall()

        connection.commit()
        connection.close()

        return result
