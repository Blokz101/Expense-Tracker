# expense_tracker/config_manager.py

import os

from typing import Optional

from configparser import ConfigParser

from expense_tracker.constants import GeneralConstants


class ConfigManager(ConfigParser):
    """
    Handles setting and getting config settings from settings file
    """

    def __new__(cls):
        """
        Define the class as a singleton.
        """
        if not hasattr(cls, "instance"):
            cls.instance = super(ConfigManager, cls).__new__(cls)

        return cls.instance

    def __init__(self):
        """
        Init ConfigParser and verify that the database exists.
        """

        super().__init__()

        if not os.path.exists(GeneralConstants.SETTINGS_FILE_NAME):
            self._create_configs(GeneralConstants.SETTINGS_FILE_DEFAULTS)

        self.read(GeneralConstants.SETTINGS_FILE_NAME)

    def _create_configs(self, defaults: list) -> None:
        """
        Create a new configs file with defaults defined in constants.py
        """

        for (
            section_name,
            section_defaults,
        ) in defaults:
            self[section_name] = section_defaults

        self.write(open(GeneralConstants.SETTINGS_FILE_NAME, "w"))

    def get_database_path(self) -> str:
        return self.get("general", "database_path")

    def get_number_of_options(self) -> Optional[str]:
        return int(self.get("general", "number_of_options"))

    def get_same_merchant_mile_radius(self) -> Optional[str]:
        return float(self.get("general", "same_merchant_mile_radius"))

    def get_default_account_id(self) -> int:
        return int(self.get("general", "default_account_id"))
