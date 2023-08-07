# expense_tracker/config_manager.py

import os

from typing import Optional

from configparser import ConfigParser

from expense_tracker.constants import Constants

from pathlib import Path


class Config_Manager(ConfigParser):
    """
    Handles setting and getting config settings from settings file
    """

    def __new__(cls):
        """
        Define the class as a singleton.
        """
        if not hasattr(cls, "instance"):
            cls.instance = super(Config_Manager, cls).__new__(cls)

        return cls.instance

    def __init__(self):
        """
        Init ConfigParser and verify that the database exists.
        """

        super().__init__()

        if not os.path.exists(Constants.SETTINGS_FILE_PATH):
            self._create_configs(Constants.SETTINGS_FILE_DEFAULTS)

        self.read(Constants.SETTINGS_FILE_PATH)

    def _create_configs(self, defaults: list) -> None:
        """
        Create a new configs file with defaults defined in constants.py
        """

        for (
            section_name,
            section_defaults,
        ) in defaults:
            self[section_name] = section_defaults

        self.write(open(Constants.SETTINGS_FILE_PATH, "w"))

    def get_database_path(self) -> Path:
        return Path(self.get("general", "database_path"))

    def get_photo_archive_path(self) -> Path:
        return Path(self.get("general", "photo_archive_path"))

    def get_number_of_options(self) -> int:
        return int(self.get("general", "number_of_options"))

    def get_same_merchant_mile_radius(self) -> float:
        return float(self.get("general", "same_merchant_mile_radius"))

    def get_default_account_id(self) -> int:
        return int(self.get("general", "default_account_id"))
