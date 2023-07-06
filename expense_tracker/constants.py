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
            {
                "database_path": str(Path().absolute() / "database.db"),
            },
        ),
    )

    DATABASE_TEMPLATE_PATH: Path = (
        Path().absolute() / "expense_tracker" / "model" / "database_template.sql"
    )
    
@dataclass
class StatusMessage:
    """
    Provides status messages for the user
    """
    
    DATABASE_CREATION_SUCCESS: str = "Database successfully created!"
    SETTING_OPTION_NOT_FOUND: str = "Unable to locate setting option."
    DATABASE_NOT_FOUND: str = "Could not locate the database\nCheck the path in settings.ini?"
    DATABASE_ALREADY_ESISTS: str = "Database already exists."
    CANNOT_OPEN_DATABASE: str = "Failed to open database\nCheck the path in settings.ini?"
    