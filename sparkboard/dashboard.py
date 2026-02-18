#!/usr/bin/env python3
"""Spark Board — Your terminal dashboard."""

import time
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

from sparkboard.widgets import (
    system_stats_panel,
    weather_panel,
    quote_panel,
    beads_panel,
    agents_panel,
)


def make_header() -> Panel:
    title = Text()
    title.append(" SPARK BOARD ", style="bold bright_yellow on grey23")
    title.append("  ", style="dim")
    title.append(time.strftime("%H:%M:%S"), style="bright_white")
    return Panel(title, style="bright_yellow", height=3)


def build_layout() -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body"),
        Layout(name="footer", size=3),
    )
    layout["body"].split_column(
        Layout(name="top_row"),
        Layout(name="bottom_row"),
    )
    layout["top_row"].split_row(
        Layout(name="system", ratio=1),
        Layout(name="weather", ratio=1),
    )
    layout["bottom_row"].split_row(
        Layout(name="beads", ratio=1),
        Layout(name="agents", ratio=1),
    )
    return layout


def render(layout: Layout) -> Layout:
    layout["header"].update(make_header())
    layout["system"].update(system_stats_panel())
    layout["weather"].update(weather_panel())
    layout["beads"].update(beads_panel())
    layout["agents"].update(agents_panel())
    layout["footer"].update(quote_panel())
    return layout


def main():
    console = Console()
    layout = build_layout()

    try:
        with Live(render(layout), console=console, refresh_per_second=1, screen=True):
            while True:
                render(layout)
                time.sleep(1)
    except KeyboardInterrupt:
        console.print("[bright_yellow]Spark Board shut down.[/]")


if __name__ == "__main__":
    main()
