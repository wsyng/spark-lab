import json
import time
from pathlib import Path

from rich.panel import Panel
from rich.text import Text
from rich.console import Group

TASKS_DIR = Path("/tmp/claude-1000/-home-wesy-brain/tasks")

SPINNER_FRAMES = [
    "[bold bright_cyan]>>> [/][bright_green]GO[/]",
    "[bold bright_yellow]>>>[/] [bright_green]GO[/]",
    "[bold bright_magenta]>> [/][bright_green]GO[/]",
    "[bold bright_cyan]>  [/][bright_green]GO[/]",
    "[bold bright_yellow] > [/][bright_green]GO[/]",
    "[bold bright_magenta] >>[/][bright_green]GO[/]",
    "[bold bright_cyan]>>>[/] [bright_green]GO[/]",
    "[bold bright_yellow]>>>>[/][bright_green]GO[/]",
]
DONE_ICON = "[bold bright_green]DONE  [/]"
FAIL_ICON = "[bold bright_red]FAIL  [/]"
IDLE_FRAMES = [
    "[dim].....[/]",
    "[dim]o....[/]",
    "[dim].o...[/]",
    "[dim]..o..[/]",
    "[dim]...o.[/]",
    "[dim]....o[/]",
    "[dim].....[/]",
    "[dim].....[/]",
]

_frame_counter = 0


def _parse_agent_file(path: Path) -> dict | None:
    try:
        content = path.read_text()
        raw_lines = content.strip().splitlines()
        if not raw_lines:
            return None

        agent_id = path.stem.replace(".output", "")
        has_error = False
        description = agent_id[:7]

        # Parse the last line as JSON to detect completion
        # Completed agent: last line is assistant with text, no tool_use
        # Running agent: last line is user (tool result) or assistant with tool_use
        is_running = True
        try:
            last = json.loads(raw_lines[-1])
            last_type = last.get("type")
            is_error_msg = last.get("isApiErrorMessage", False)
            if is_error_msg:
                has_error = True
                is_running = False
            elif last_type == "assistant":
                msg = last.get("message", {})
                content_blocks = msg.get("content", [])
                has_tool_use = any(c.get("type") == "tool_use" for c in content_blocks)
                has_text = any(c.get("type") == "text" for c in content_blocks)
                if has_text and not has_tool_use:
                    is_running = False
        except (json.JSONDecodeError, KeyError):
            pass

        # Extract task description from the first user message
        for line in raw_lines:
            if '"role":"user"' in line and '"content":"' in line:
                start = line.find('"content":"') + 11
                snippet = line[start:start + 80]
                if "building" in snippet.lower():
                    idx = snippet.lower().find("building")
                    description = snippet[idx:idx + 40].split("\\n")[0].rstrip('."')
                    break
                elif "SK-" in snippet:
                    idx = snippet.find("SK-")
                    description = snippet[idx:idx + 30].split("\\n")[0].rstrip('."')
                    break
                else:
                    description = snippet[:35].split("\\n")[0].rstrip('."')
                    break

        return {
            "id": agent_id[:7],
            "description": description,
            "running": is_running,
            "error": has_error,
            "mtime": path.stat().st_mtime,
        }
    except Exception:
        return None


def agents_panel() -> Panel:
    global _frame_counter
    _frame_counter += 1
    spinner = SPINNER_FRAMES[_frame_counter % len(SPINNER_FRAMES)]

    text = Text.from_markup("")
    agents = []

    if TASKS_DIR.exists():
        for f in sorted(TASKS_DIR.glob("*.output"), key=lambda p: p.stat().st_mtime, reverse=True):
            info = _parse_agent_file(f)
            if info:
                agents.append(info)

    # Show last 6 agents max
    agents = agents[:6]

    running_count = sum(1 for a in agents if a["running"])
    done_count = sum(1 for a in agents if not a["running"])

    agent_colors = ["bright_cyan", "bright_yellow", "bright_magenta", "bright_green", "bright_red", "bright_blue"]

    if not agents:
        idle = IDLE_FRAMES[_frame_counter % len(IDLE_FRAMES)]
        text = Text.from_markup(f"[dim]Waiting for agents {idle}[/]\n\n[dim italic]Launch agents to see them here[/]")
    else:
        # Pulsing header when agents are active
        if running_count > 0:
            pulse_chars = ["[bold bright_green]", "[bold bright_yellow]", "[bold bright_cyan]"]
            pulse = pulse_chars[_frame_counter % len(pulse_chars)]
            bar_len = min(running_count * 4, 20)
            bar = "=" * bar_len + ">"
            header = Text.from_markup(f" {pulse}{bar}[/] [bold]{running_count}[/] active  [dim]{done_count} done[/]\n")
        else:
            header = Text.from_markup(f" [bold bright_green]ALL CLEAR[/] [dim]{done_count} completed[/]\n")
        lines = [header]

        for i, a in enumerate(agents):
            color = agent_colors[i % len(agent_colors)]
            if a["running"]:
                # Each agent gets its own offset spinner for variety
                offset = (i * 2 + _frame_counter) % len(SPINNER_FRAMES)
                frames = SPINNER_FRAMES[offset]
                line = Text.from_markup(f" {frames} [{color} bold]{a['id']}[/] [dim]{a['description'][:22]}[/]\n")
            elif a["error"]:
                line = Text.from_markup(f" {FAIL_ICON} [{color}]{a['id']}[/] [dim]{a['description'][:22]}[/]\n")
            else:
                line = Text.from_markup(f" {DONE_ICON} [{color}]{a['id']}[/] [dim]{a['description'][:22]}[/]\n")
            lines.append(line)

        text = Text()
        for line in lines:
            text.append_text(line)

    title = "Agents"
    if running_count > 0:
        title = f"Agents [{running_count} live]"
    return Panel(text, title=title, border_style="bright_green", padding=(0, 1))
