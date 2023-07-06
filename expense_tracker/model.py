# expense_tracker/database.py

from expense_tracker.config_manager import ConfigManager
from expense_tracker.exceptions import DatabaseNotFound, DatabaseAlreadyExists
from expense_tracker.constants import GeneralConstants

from pathlib import Path

import sqlite3
import os


class Database:
    """
    Performs all work that requires interaction with the database
    """

    @staticmethod
    def create_database(path: Path):
        """
        Create a new sql database
        """

        if os.path.exists(path):
            raise DatabaseAlreadyExists(f"Database at '{str(path)}' already exists.")

        with open(GeneralConstants.DATABASE_TEMPLATE_PATH, "r") as database_template:

            database, cursor = Database._connect_to_database(path)

            sql_script: str = database_template.read()
            cursor.executescript(sql_script)

            database.commit()
            database.close()

    def _connect_to_database(path: Path) -> tuple[sqlite3.Connection, sqlite3.Cursor]:

        if not os.path.exists(path):
            raise DatabaseNotFound(
                f"Could not lcoate database at '{path}'\n\tCreate a new database with 'exptrack --init'"
            )

        database_connection: sqlite3.connection = sqlite3.connect(path)
        database_cursor: sqlite3.Cursor = database_connection.cursor()

        return (database_connection, database_cursor)
