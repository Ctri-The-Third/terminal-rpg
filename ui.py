import textual

from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Button, Header, Footer, Static


class GameDisplay(Static):
    pass


class TextDisplay(Static):
    pass


class Game(App):
    """A simple stopwatch app."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    CSS_PATH = "ui.css"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Image", classes="box")
        yield Static("Console", classes="box")
        yield Static("input space", classes="input_box")

        yield Footer()
        return super().compose()


if __name__ == "__main__":
    app = Game()
    app.run()


###
# let's split
# | 3x2  |2x2  |
# |     | 2x2 |

# ----------
# |   5x1    |
