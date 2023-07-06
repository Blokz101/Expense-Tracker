# expense_tracker/cli/merchants.py


import typer

from rich.console import Console

from expense_tracker.cli import console, configs


class Merchants:

    app: typer.Typer = typer.Typer()

    @app.command()
    def create() -> None:

        console.print("CREATING MERCHANT")
