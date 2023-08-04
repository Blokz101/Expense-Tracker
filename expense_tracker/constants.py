# expense_tracker/constants.py

from dataclasses import dataclass, field

from typing import Literal

from pathlib import Path


@dataclass
class GeneralConstants:
    """
    General constants for the program
    """

    DATE_FORMAT: str = "%A, %B %-d %Y"

    SELECTED_STYLE: str = "cyan"
    HIGHLIGHTED_STYLE: str = "purple4"
    LOWLIGHT_STYLE: str = "bright_black"
    ERROR_STYLE = "red"
    SUCCESS_STYLE: str = "green"
    WARNING_STYLE: str = "dark_goldenrod"

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
    USER_INPUT: tuple = ("User Input", GeneralConstants.SUCCESS_STYLE)
    DEFAULT: dict[str, str] = ("Default", GeneralConstants.WARNING_STYLE)
    PHOTO: dict[str, str] = ("Photo", GeneralConstants.SUCCESS_STYLE)
    MERCHANT: dict[str, str] = ("Merchant", GeneralConstants.WARNING_STYLE)
    NONE: dict[str, str] = ("None", GeneralConstants.ERROR_STYLE)
