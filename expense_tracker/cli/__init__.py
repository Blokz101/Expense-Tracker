# expense_tracker/cli/__init__.py

from rich.console import Console

from expense_tracker.config_manager import ConfigManager

# Define the console and configs manager for the entire CLI modules use
console: Console = Console(highlight=False)
configs: ConfigManager = ConfigManager()
