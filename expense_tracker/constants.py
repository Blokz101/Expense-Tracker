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

    DATABASE_TEMPLATE_PATH: Path = (
        Path().absolute() / "expense_tracker" / "model" / "database_template.sql"
    )
