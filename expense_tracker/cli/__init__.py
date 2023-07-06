# expense_tracker/cli/__init__.py

import typer

from rich.console import Console

from expense_tracker.config_manager import ConfigManager
from expense_tracker.model.database import Database

console: Console = Console(highlight=False)
configs: ConfigManager = ConfigManager()
