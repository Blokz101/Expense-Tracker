# expense_tracker/constants.py

from pathlib import Path


class Constants:
    """
    General constants for the program
    """
    
    # Textual
    VALIDATION_TEXT_ID: str = "validation_text"
    VALIDATION_BUTTON_ID: str = "validation_button"
    
    VALIDATED_CLASS: str = "validated"

    # Date formats
    DATE_FORMAT: str = "%a, %b %-d %Y"
    STATEMENT_DATE_FORMAT: str = "%m/%d/%Y"
    USER_INPUT_DATE_FORMAT: str = "%m/%d/%Y"

    # File Paths
    SETTINGS_FILE_PATH: str = "settings.ini"
    CSS_FILE_PATH: str = "stylesheet.css"

    SUPPORTED_IMAGE_EXTENSIONS: tuple[str, ...] = (".png", ".jpg", ".jpeg")

    SETTINGS_FILE_DEFAULTS: list[tuple[str, dict[str, str]]] = [
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
    ]
