# expense_tracker/model/database.py

import sqlite3

import os


class Database:
    """
    Handels all direct interaction with sql database.
    """

    def __init__(self, database_path: str) -> None:
        """
        Constructor
        """

        if not type(database_path) == str:
            raise ValueError(f"database_path cannot be of type {type(database_path)}")

        self.database_path = database_path

    def create_database(self, database_template_path: str):
        """
        Create a new sql database.
        """

        if os.path.exists(self.database_path):
            raise DatabaseAlreadyExists(
                f"File at '{str(self.database_path)}' already exists."
            )

        with open(database_template_path, "r") as database_template:
            connection, cursor = self._connect_to_database(ignore_exist_error=True)

            sql_script: str = database_template.read()
            cursor.executescript(sql_script)

            connection.commit()
            connection.close()

    def _connect_to_database(
        self, ignore_exist_error=False
    ) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
        """
        Return connection and cursor object after connecting to the database.
        """

        if not os.path.exists(self.database_path) and not ignore_exist_error:
            raise DatabaseNotFound(
                f"Could not lcoate database at '{self.database_path}'"
            )

        database_connection: sqlite3.connection = sqlite3.connect(self.database_path)
        database_cursor: sqlite3.Cursor = database_connection.cursor()

        return (database_connection, database_cursor)

    def execute_query(self, query: str, args: tuple) -> None:
        """
        Execute a query.
        """

        connection, cursor = self._connect_to_database()

        cursor.execute(
            query,
            args,
        )

        connection.commit()
        connection.close()

    def fetchall_query(self, query: str, args: tuple) -> tuple:
        """
        Execute a query and fetch all the results.
        """

        connection, cursor = self._connect_to_database()

        cursor.execute(
            query,
            args,
        )

        result: tuple = cursor.fetchall()

        connection.commit()
        connection.close()

        return result


class DatabaseNotFound(Exception):
    """
    Database was not found.
    """


class DatabaseAlreadyExists(Exception):
    """
    User ordered creation of database but it already exists.
    """
