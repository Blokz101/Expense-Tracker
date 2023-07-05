# expense_tracker/cil.py

from typing import Optional
from typing_extensions import Annotated

from rich.console import Console

import typer
import configparser

from expense_tracker import __app_name__, __version__
from expense_tracker.model import Database
from expense_tracker.config_manager import ConfigManager


class CLI:
    """
    ViewController for the application. Deals with command line user interaction.
    """


    app: typer.Typer = typer.Typer()
    
    console: Console
    configs: ConfigManager
    database: Database
        


    def _version_callback(value: bool) -> None:
        """
        Callback for main command and version option.
        """

        if value:
            print(f"{__app_name__} {__version__}")
            raise typer.Exit()

    @staticmethod
    @app.callback()
    def main(
        version: Annotated[
            bool,
            typer.Option(
                help="Display the version and exit.",
                callback=_version_callback,
                is_eager=True,
            ),
        ] = False
    ) -> None:
        """
        Reconcile and track expenses using receipt photos and bank statements.
        """
        
        CLI.console = Console(highlight = False)
        
        
        CLI.configs = ConfigManager()
        
        try:
            CLI.database = Database(CLI.configs)
            
        except configparser.NoOptionError as e:
            CLI.console.print(
                f"\n\t{e}\n", 
                style = "red",
            )
            raise typer.Exit()
            

    @staticmethod
    @app.command()
    def add(
        photo: Annotated[
            bool, typer.Option(help="Create transactions based on photos.")
        ] = True,
        auto: Annotated[
            bool,
            typer.Option(
                help="Automatically create transactions based on photos and bank statement."
            ),
        ] = False,
    ) -> None:
        """
        Create new transactions.
        """

        print("Add")

    @staticmethod
    @app.command()
    def reconcile() -> None:
        """
        Reconcile new transactions with bank statement.
        """

        print("Reconcile")
