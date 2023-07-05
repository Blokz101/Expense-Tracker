# expense_tracker/config_manager.py

import os

from configparser import ConfigParser

from expense_tracker.constants import GeneralConstants
from expense_tracker.exceptions import SettingsFormatException


class ConfigManager(ConfigParser):
    """
    Handels setting and getting config settings from settings file
    """

    def __init__(self):
        """
        Init ConfigParser and verify that the database exists
        """

        super().__init__()

        if not os.path.exists(GeneralConstants.SETTINGS_FILE_NAME):
            self._create_database()

        self.read(GeneralConstants.SETTINGS_FILE_NAME)

        self._verify_database()

    def _create_database(self) -> None:
        """
        Create a new database with deafults defined in constants.py
        """

        for (
            section_name,
            section_deafults,
        ) in GeneralConstants.SETTINGS_FILE_DEAFULTS:
            self[section_name] = section_deafults

        self.write(open(GeneralConstants.SETTINGS_FILE_NAME, "w"))

    def _verify_database(self) -> None:
        """
        Verify that the settings file has all the sections and options that the application requires
        """

        for (
            section_name,
            section_deafults,
        ) in GeneralConstants.SETTINGS_FILE_DEAFULTS:

            for key in section_deafults.keys():

                if not self.has_option(section_name, key):

                    raise SettingsFormatException(
                        f'Settings file is missing section "{section_name}" option "{key}"'
                    )
