from time import monotonic
from rich.console import RenderableType
import textual
from textual._types import WatchCallbackType


from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal, Grid
from textual.dom import DOMNode
from textual.widgets import Button, Header, Footer, Static, Placeholder
from textual.reactive import reactive


class Presence(App):
    """A simple stopwatch app."""

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("g", "toggle_grid", "Toggle grid"),
    ]
    CSS_PATH = "ui.css"
    status = False

    def action_toggle_grid(self) -> None:
        self.status = not self.status
        if not self.status:
            self.query("control_grid").last().remove()
        else:
            result = self.query("Vertical")
            result.last().mount(self.create_control_grid())

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield LogDisplay()
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
        return Grid(
            classes="control_grid",
            id="control_grid",
        )

    def populate_control_grid(self, grid: Grid) -> Grid:
        grid.mount(
            Button("fetch current", classes="control_button third"),
            Button("Skip", classes="control_button third"),
            Button("Solve", classes="control_button third"),
            Button("refresh tasks", classes="control_button wide"),
            Button("dividers", classes="control_button wide"),
        )


class LogDisplay(Static):
    start_time = reactive(monotonic)
    time = reactive(0.0)

    def on_mount(self) -> None:
        self.set_interval(1, self.update_time)

    def update_time(self) -> None:
        self.time = monotonic() - self.start_time

    def watch_time(self, time: float) -> None:
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f"{hours:02,.0f}:{minutes:02.0f}:{seconds:06.3f}")


if __name__ == "__main__":
    app = Presence()
    app.run()


###
# let's split
# | 3x2  |2x2  |
# |     | 2x2 |

# ----------
# |   5x1    |
