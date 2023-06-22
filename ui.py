from time import monotonic
from rich.console import RenderableType
import textual
from textual._types import WatchCallbackType


from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal, Grid
from textual.dom import DOMNode
from textual.widgets import Button, Header, Footer, Static, Placeholder
from textual.reactive import reactive
from textual.widgets import Static, ProgressBar
from progress import DisplayWidget


class Presence(App):
    """A simple stopwatch app."""

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("g", "progress", "Progress the bar"),
    ]
    CSS_PATH = "ui.css"
    status = False

    def action_progress(self) -> None:
        self.query_one(ProgressBar).advance(1)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield ProgressBar(45g)
        yield DisplayWidget()
        yield ProgressBar(45)
        yield Footer()
        return super().compose()


if __name__ == "__main__":
    app = Presence()
    app.run()


###
# let's split
# | 3x2  |2x2  |
# |     | 2x2 |

# ----------
# |   5x1    |
