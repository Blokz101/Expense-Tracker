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

    SETTINGS_FILE_NAME: str = "settings.ini"

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


@dataclass
class Field_Constant:
    USER_INPUT: tuple = ("User Input", Constants.SUCCESS_STYLE)
    DEFAULT: dict[str, str] = ("Default", Constants.WARNING_STYLE)
    PHOTO: dict[str, str] = ("Photo", Constants.SUCCESS_STYLE)
    MERCHANT: dict[str, str] = ("Merchant", Constants.WARNING_STYLE)
    NONE: dict[str, str] = ("None", Constants.ERROR_STYLE)
