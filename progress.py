import textual
from textual.app import App, ComposeResult, RenderResult
from textual.reactive import reactive
from textual.widgets import Header, Footer
from textual.containers import Container, Center
from datetime import datetime
from textual.screen import Screen
from textual.widgets import Static, ProgressBar, Label
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
    CSS_PATH = "progress.css"
    BINDINGS = [
        ("g", "update_trello_actions", "Get progress"),
    ]
    output = reactive("actions go here")

    trello_actions = []
    T_HELPER = trello(BOARD_ID, TRELLO_KEY, TRELLO_TOKEN)
    last_action_received_id = reactive(datetime.now().strftime("%Y-%m-%d"))
    new_cards = 0
    solved_cards = 0
    total_cards = 0
    seen_card_ids = []
    TARGET_LIST_ID = "5f0dee6c5026590ce3004732"

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Container(
            DisplayWidget(self.output),
            Center(
                Label("Task progress: "),
                ProgressBar(
                    total=self.total_cards,
                    show_bar=True,
                    show_percentage=True,
                    show_eta=False,
                    name="Tasks percentage",
                ),
            ),
        )
        yield Footer()

    def on_mount(self) -> None:
        """Called when the app is mounted."""
        self.seen_card_ids = [
            c["id"]
            for c in self.T_HELPER.fetch_trello_cards()
            if c["idList"] == self.TARGET_LIST_ID
        ]
        self.total_cards = len(self.seen_card_ids)
        self.action_update_trello_actions()
        self.set_interval(5, self.action_update_trello_actions)
        self.set_interval(5, self.update_progress_bar)

    def update_output_text(self):
        """Update the output text"""
        self.query_one(DisplayWidget).output = self.output

    def update_progress_bar(self):
        """Update the progress bar"""
        progress_bar = self.query_one(ProgressBar)
        progress_bar.update(progress=self.solved_cards, total=self.total_cards)

    def action_update_trello_actions(self):
        """Update the list of actions with the latest actions"""
        actions = self.T_HELPER.fetch_actions_for_board(
            since=self.last_action_received_id, limit=1000
        )
        if len(actions) == 0:
            return
        self.last_action_received_id = actions[0]["id"]
        self.trello_actions = actions + self.trello_actions
        output = ""
        counter = -1
        for action in self.trello_actions:
            counter += 1
            action = self.recategorize_actions(action)
            action = self.colour_action(action)
            self.update_totals_from_action(action)
            if action is None:
                continue
            output += f"[{action['colour']}]"
            output += f"{action['type'] }"
            output += f" {action['data']['card']['id'][-5:]} "
            if len(action["subtypes"]) > 0:
                output += "- "
                output += ", ".join(action["subtypes"])
            output += f" [/{action['colour']}]"
            if (
                "data" in action
                and "card" in action["data"]
                and "name" in action["data"]["card"]
            ):
                output += f"{action['data']['card']['name']} "

                output += f"\t{action['date']}"
            output += "\n"
        self.output = output
        self.update_output_text()

    def update_totals_from_action(self, action: dict, initial=False):
        """Update the total, new, and solved cards counts based on the action."""
        # if a card is deleted or archived, then we increase the solve count

        if action["type"] == "deleteCard":
            self.solved_cards += 1
        elif action["type"] == "updateCard" and "archive" in action["subtypes"]:
            self.solved_cards += 1

        # if a card is new, fetch it and increase the new & total cards count.
        if action["type"] == "createCard":
            self.new_cards += 1

        return None

    def recategorize_actions(self, action) -> dict:
        """adds 'archiveCard' and 'moveCard' to the kinds of actions that can be returned."""
        action["subtypes"] = []
        if action["type"] == "updateCard":
            old_data = action["data"].get("old", {})
            if "due" in old_data:
                action["subtypes"].append("due")
            if "idList" in old_data:
                action["subtypes"].append("moved_list")
            if "name" in old_data or "desc" in old_data:
                action["subtypes"].append("rewrite")
            # if 'due', 'idlist', and 'name' not in old_data:
            if "pos" in old_data:
                action["subtypes"].append("reorder")
            if "closed" in old_data and not old_data["closed"]:
                action["subtypes"].append("archive")

            if not any(
                x in old_data
                for x in ["due", "idList", "name", "pos", "closed", "desc"]
            ):
                action["subtypes"].append("other")
        return action

    def colour_action(self, action) -> dict:
        action["colour"] = "white"

        # don't have a convenient way of ordering, so used ifs instead of elifs as a way of prioritizing

        # new tasks are red
        if action["type"] == "createCard":
            action["colour"] = "red"

        if "due" in action["subtypes"]:
            action["colour"] = "red"

        # paused tasks are yellow
        if "moved_list" in action["subtypes"]:
            action["colour"] = "yellow"

        # completed tasks are green
        if "archive" in action["subtypes"] or action["type"] == "deleteCard":
            action["colour"] = "green"

        return action


if __name__ == "__main__":
    app = Progress()
    app.run()
