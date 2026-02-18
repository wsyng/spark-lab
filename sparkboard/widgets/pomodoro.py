import json
import time
from datetime import datetime
from pathlib import Path

from rich.panel import Panel
from rich.progress_bar import ProgressBar
from rich.text import Text
from rich.console import Group

STATE_FILE = Path("/tmp/sparkboard_pomodoro.json")

WORK_DURATION = 25 * 60  # seconds
BREAK_DURATION = 5 * 60  # seconds


def _load_state() -> dict:
    if STATE_FILE.exists():
        try:
            with STATE_FILE.open() as f:
                return json.load(f)
        except (json.JSONDecodeError, KeyError):
            pass
    return _create_state()


def _create_state() -> dict:
    state = {
        "start_time": time.time(),
        "mode": "work",
        "session_count": 0,
    }
    _save_state(state)
    return state


def _save_state(state: dict) -> None:
    with STATE_FILE.open("w") as f:
        json.dump(state, f)


def pomodoro_panel() -> Panel:
    state = _load_state()

    mode = state.get("mode", "work")
    start_time = state.get("start_time", time.time())
    session_count = state.get("session_count", 0)

    duration = WORK_DURATION if mode == "work" else BREAK_DURATION
    elapsed = time.time() - start_time

    if elapsed >= duration:
        # Session has ended — advance to next session
        if mode == "work":
            session_count += 1
            new_mode = "break"
        else:
            new_mode = "work"
        state = {
            "start_time": time.time(),
            "mode": new_mode,
            "session_count": session_count,
        }
        _save_state(state)
        mode = new_mode
        start_time = state["start_time"]
        elapsed = 0.0
        duration = WORK_DURATION if mode == "work" else BREAK_DURATION

    remaining = max(0.0, duration - elapsed)
    mins = int(remaining) // 60
    secs = int(remaining) % 60

    color = "green" if mode == "work" else "cyan"
    mode_label = "WORK" if mode == "work" else "BREAK"

    mode_text = Text(f"  {mode_label}", style=f"bold {color}")

    time_text = Text(f"  {mins:02d}:{secs:02d}", style=f"bold {color}")

    progress_bar = ProgressBar(
        total=duration,
        completed=elapsed,
        width=28,
        style="bar.back",
        complete_style=color,
        finished_style=color,
    )

    sessions_text = Text(
        f"  Sessions completed: {session_count}", style="dim"
    )

    content = Group(
        mode_text,
        time_text,
        Text(""),
        progress_bar,
        Text(""),
        sessions_text,
    )

    return Panel(
        content,
        title="Pomodoro",
        border_style="green",
        padding=(0, 1),
    )
