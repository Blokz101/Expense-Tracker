# expense_tracker/model.py


class database:
    def __init__(self, database_path: str) -> None:
        """
        Constructor
        """

        self.database_path: str = database_path
