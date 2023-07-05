# expense_tracker/database.py

from expense_tracker.config_manager import ConfigManager


class Database:
    """
    Performs all work that requires interaction with the database
    """

    def __init__(self, config: ConfigManager) -> None:
        """
        Constructor
        """

        self.config: ConfigManager = config
