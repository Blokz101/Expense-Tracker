# expense_tracker/__init__.py

__app_name__ = "exptrack"
__version__ = "0.0.0"



(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
    ID_ERROR
) = range(6)

ERRORS = {
    DIR_ERROR: "Config directory error",
    FILE_ERROR: "Config file error",
    DB_READ_ERROR: "Database read error",
    DB_WRITE_ERROR: "Database write error"
}
