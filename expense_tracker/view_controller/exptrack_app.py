# TODO Add the file path here

from textual.app import App, ComposeResult
from textual.widgets import Welcome

class Exptrack_App(App):
    """
    Main app
    """
    
    def compose(self) -> ComposeResult:
        yield Welcome()
