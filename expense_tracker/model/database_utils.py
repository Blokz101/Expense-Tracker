# expense_tracker/model/database.py

from expense_tracker.exceptions import DatabaseNotFound, DatabaseAlreadyExists
from expense_tracker.constants import GeneralConstants

from pathlib import Path

import sqlite3
import os


class Database_Utils:
    """
    Performs all work that requires interaction with the database
    """

    @staticmethod
    def create_database(path: Path):
        """
        Create a new sql database
        """

        if os.path.exists(path):
            raise DatabaseAlreadyExists(f"File at '{str(path)}' already exists.")

        with open(GeneralConstants.DATABASE_TEMPLATE_PATH, "r") as database_template:
            connection, cursor = Database_Utils._connect_to_database(
                path, ignore_exist_error=True
            )

            sql_script: str = database_template.read()
            cursor.executescript(sql_script)

            connection.commit()
            connection.close()

    @staticmethod
    def connect_to_database(
        path: Path, ignore_exist_error=False
    ) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
        """
        Return connection and cursor object after connecting to the database
        """

        if not os.path.exists(path) and not ignore_exist_error:
            raise DatabaseNotFound(f"Could not lcoate database at '{path}'")

        database_connection: sqlite3.connection = sqlite3.connect(path)
        database_cursor: sqlite3.Cursor = database_connection.cursor()

        return (database_connection, database_cursor)
