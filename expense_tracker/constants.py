# expense_tracker/constants.py

from dataclasses import dataclass

from typing import Tuple

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


@dataclass
class Field_Constant:
    USER_INPUT: Tuple = ("User Input", GeneralConstants.SUCCESS_STYLE)
    DEFAULT: dict = ("Default", GeneralConstants.WARNING_STYLE)
    PHOTO: dict = ("Photo", GeneralConstants.SUCCESS_STYLE)
    MERCHANT: dict = ("Merchant", GeneralConstants.WARNING_STYLE)
    NONE: dict = ("None", GeneralConstants.ERROR_STYLE)
