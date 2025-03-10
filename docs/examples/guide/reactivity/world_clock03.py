from datetime import datetime

from pytz import timezone

from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Digits, Label


class WorldClock(Widget):

    clock_time: reactive[datetime] = reactive(datetime.now)

    def __init__(self, timezone: str) -> None:
        self.timezone = timezone
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Label(self.timezone)
        yield Digits()

    def watch_clock_time(self, time: datetime) -> None:
        localized_time = time.astimezone(timezone(self.timezone))
        self.query_one(Digits).update(localized_time.strftime("%H:%M:%S"))


class WorldClockApp(App):
    CSS_PATH = "world_clock01.tcss"

    time: reactive[datetime] = reactive(datetime.now)

    def compose(self) -> ComposeResult:
        yield WorldClock("Europe/London").data_bind(
            clock_time=WorldClockApp.time  # (1)!
        )
        yield WorldClock("Europe/Paris").data_bind(
            clock_time=WorldClockApp.time
        )
        yield WorldClock("Asia/Tokyo").data_bind(clock_time=WorldClockApp.time)

    def update_time(self) -> None:
        self.time = datetime.now()

    def on_mount(self) -> None:
        self.update_time()
        self.set_interval(1, self.update_time)


if __name__ == "__main__":
    WorldClockApp().run()
