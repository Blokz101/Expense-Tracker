# expense_tracker/model.py


class Database:
    """
    Performs all work that requires interaction with the database
    """

    def __init__(self, database_path: str) -> None:
        """
        Constructor
        """

        self.database_path: str = database_path
