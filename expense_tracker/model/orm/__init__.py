# expense_tracker/orm/__init__.py

from sqlalchemy import Engine
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

from expense_tracker.config_manager import Config_Manager


class Base(DeclarativeBase):
    """
    Shared base object for all mapped classes.
    """


engine: Engine = create_engine(f"sqlite:///{Config_Manager().get_database_path()}")
