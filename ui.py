from rich.console import RenderableType
import textual

from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal, Grid
from textual.widgets import Button, Header, Footer, Static


class Presence(App):
    """A simple stopwatch app."""

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("g", "hide_grid", "Toggle grid"),
    ]
    CSS_PATH = "ui.css"
    status = False

    def action_toggle_grid(self) -> None:
        self.status = not self.status
        if not self.status:
            self.query("control_grid").last().remove()
        else:
            self.query_one("#control_grid_holder").mount(self.create_control_grid())

    def compose(self) -> ComposeResult:
        control_grid = self.create_control_grid()
        yield Header()
        yield Static("Image", classes="box")
        if self.status:
            yield Container(
                Vertical(
                    Static("Presence controls"),
                    id="control_grid_holder",
                ),
                classes="console box",
                id="right_console",
            )
        else:
            yield Static("Console blob would go here")
        yield Static("input space", classes="input_box")

        yield Footer()
        return super().compose()

    def create_control_grid(self) -> Grid:
        # does this need to be Return or Yield????? this is breaking because everything is a generator and this isn't, I think.
        yield (
            Grid(
                Button("fetch current", classes="control_button third"),
                Button("Skip", classes="control_button third"),
                Button("Solve", classes="control_button third"),
                Button("refresh tasks", classes="control_button wide"),
                Button("dividers", classes="control_button wide"),
                classes="control_grid",
                id="control_grid",
            ),
        )


if __name__ == "__main__":
    app = Presence()
    app.action_toggle_grid()
    app.run()


###
# let's split
# | 3x2  |2x2  |
# |     | 2x2 |

# ----------
# |   5x1    |
