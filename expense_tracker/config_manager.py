# expense_tracker/config_manager.py

import os

from configparser import ConfigParser

from expense_tracker.constants import GeneralConstants


class ConfigManager(ConfigParser):
    """
    Handels setting and getting config settings from settings file
    """

    def _create_configs(self, deafults: list) -> None:
        """
        Create a new configs file with deafults defined in constants.py
        """

        for (
            section_name,
            section_deafults,
        ) in deafults:
            self[section_name] = section_deafults

        self.write(open(GeneralConstants.SETTINGS_FILE_NAME, "w"))

    def __init__(self):
        """
        Init ConfigParser and verify that the database exists
        """

        super().__init__()

        if not os.path.exists(GeneralConstants.SETTINGS_FILE_NAME):
            self._create_configs(GeneralConstants.SETTINGS_FILE_DEAFULTS)

        self.read(GeneralConstants.SETTINGS_FILE_NAME)
