# expense_tracker/constants.py

from dataclasses import dataclass

from pathlib import Path


@dataclass
class GeneralConstants:
    """
    General constants for the program
    """

    SETTINGS_FILE_NAME: str = "settings.ini"

    SETTINGS_FILE_DEAFULTS: list = (
        (
            "files",
            {"database_path": str(Path().absolute() / "database.db")},
        ),
    )

    NUMBER_OF_DISPLAY_OPTIONS: int = 5
