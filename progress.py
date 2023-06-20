import textual
from textual.app import App, ComposeResult, RenderResult
from textual.reactive import reactive
from textual.widgets import Header, Footer
from textual.containers import Container, Vertical
from datetime import datetime
from textual.screen import Screen
from textual.widgets import Static
from serviceHelpers.trello import trello
import os

from textual import work

TRELLO_KEY = os.getenv("TRELLO_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
BOARD_ID = "5f0dee6c5026590ce300472c"


class DisplayWidget(Static):
    output = reactive("")

    def render(self) -> RenderResult:
        return self.output


class Progress(App):
    BINDINGS = [
        ("g", "update_trello_actions", "Get progress"),
        ("o", "update_output_text", "Update output text"),
    ]
    output = reactive("actions go here")
    trello_actions = []
    T_HELPER = trello(BOARD_ID, TRELLO_KEY, TRELLO_TOKEN)
    last_action_received_id = reactive(datetime.now().strftime("%Y-%m-%d"))

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield DisplayWidget(self.output)
        yield Footer()

    def on_mount(self) -> None:
        self.action_update_trello_actions()
        self.action_update_output_text()

    def action_update_output_text(self):
        self.query_one(DisplayWidget).output = self.output

    def action_update_trello_actions(self):
        print(self.output)
        """Update the list of actions with the latest actions"""
        actions = self.T_HELPER.fetch_actions_for_board(
            since=self.last_action_received_id, limit=1000
        )
        if len(actions) > 0:
            self.last_action_received_id = actions[0]["id"]
            self.trello_actions = actions + self.trello_actions
        output = ""
        for action in self.trello_actions:
            if (
                "data" in action
                and "card" in action["data"]
                and "name" in action["data"]["card"]
            ):
                output += f"{action['type']}: {action['data']['card']['name']} {action['date']}\n"
            else:
                output += f"{action['type']}: {action['date']}\n"
        self.output = output
        return


if __name__ == "__main__":
    app = Progress()
    app.run()
