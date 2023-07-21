# expense_tracker/constants.py

from dataclasses import dataclass

from pathlib import Path


@dataclass
class GeneralConstants:
    """
    General constants for the program
    """

    SETTINGS_FILE_NAME: str = "settings.ini"

    SETTINGS_FILE_DEFAULTS: list = (
        (
            "general",
            {
                "number_of_options": "5",
                "database_path": str(Path().absolute() / "database.db"),
                "same_merchant_mile_radius": "0.2",
                "default_account_id": "1",
            },
        ),
    )
