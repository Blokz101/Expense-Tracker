# expense_tracker/cil.py

from typing import Optional
from typing_extensions import Annotated

import typer

from expense_tracker import __app_name__, __version__



app = typer.Typer()



def _version_callback(value: bool) -> None:
    """
    Callback for main command and version option.
    """
    
    if value:
        typer.echo(f"{__app_name__} {__version__}")
        raise typer.Exit()
    
    
    
@app.callback()
def main(
    version: Annotated[bool, typer.Option(
        help = "Display the version and exit.",
        callback = _version_callback,
        is_eager = True,
    )] = False
) -> None:
    """
    Reconcile and track expenses using receipt photos and bank statements.
    """
    
    pass



@app.command()
def reconcile() -> None:
    """
    Reconcile new transactions with bank statement.
    """
    
    print("Reconcile")



@app.command()
def add(
    photo: Annotated[bool, typer.Option(
        help = "Create transactions based on photos."
    )] = True,
    auto: Annotated[bool, typer.Option(
        help = "Automatically create transactions based on photos and bank statement."
    )] = False,
) -> None:
    """
    Create new transactions.
    """
    
    print("Add")
