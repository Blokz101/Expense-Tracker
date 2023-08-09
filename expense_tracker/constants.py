# expense_tracker/constants.py

from dataclasses import dataclass, field

from typing import Literal

from pathlib import Path


@dataclass
class Constants:
    """
    General constants for the program
    """

    DATE_FORMAT: str = "%A, %B %-d %Y"

    DATE_REGEX: str = "(0[1-9]|1[0-2])\/(^0[1-9]|[12][0-9]|3[01])\/(\d{4}$)"
    DATE_STRPTIME: str = "%m/%d/%Y"

    SETTINGS_FILE_PATH: str = "settings.ini"

    CSS_FILE_PATH: str = "stylesheet.css"

    SUPPORTED_IMAGE_EXTENSIONS: tuple[str, ...] = (".png", ".jpg", ".jpeg")

    SETTINGS_FILE_DEFAULTS: tuple[tuple[str, dict[str, str]], ...] = (
        (
            "general",
            {
                "number_of_options": "5",
                "database_path": str(Path().absolute() / "database.db"),
                "photo_archive_path": str(Path().absolute() / "photos"),
                "same_merchant_mile_radius": "0.2",
                "default_account_id": "0",
            },
        ),
    )
