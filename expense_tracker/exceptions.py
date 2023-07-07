# expense_tracker/exceptions.py


class DatabaseNotFound(Exception):
    """
    Database was not found.
    """


class DatabaseAlreadyExists(Exception):
    """
    User ordered creation of database but it already exists.
    """
