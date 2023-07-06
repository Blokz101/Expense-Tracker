# expense_tracker/cli/tags.py

import typer

from rich.console import Console


class Tags:

    app: typer.Typer = typer.Typer()

    console: Console = Console(highlight=False)

    @app.command()
    def create() -> None:

        Tags.console.print("CREATING TAG")
