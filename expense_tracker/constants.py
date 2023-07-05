# expense_tracker/constants.py

from dataclasses import dataclass


@dataclass
class GeneralConstants:
    """
    General constants for the program
    """

    SETTINGS_FILE_NAME: str = "settings.ini"

    SETTINGS_FILE_DEAFULTS: list = (
        (
            "files",
            {
                "database_path": "database.db",
            },
        ),
    )
