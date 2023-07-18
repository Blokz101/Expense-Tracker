# expense_tracker/orm/__init__.py

from sqlalchemy import Engine
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

from expense_tracker.config_manager import ConfigManager


engine: Engine = create_engine(f"sqlite:///{ConfigManager().get_database_path()}")


class Base(DeclarativeBase):
    """
    Shared base object for all mapped classes.
    """
