import subprocess
from rich.panel import Panel
from rich.text import Text


def _run_bd(args: list[str]) -> str:
    try:
        result = subprocess.run(
            ["bd"] + args,
            capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip()
    except Exception:
        return ""


def beads_panel() -> Panel:
    text = Text()

    # In-progress work
    in_progress = _run_bd(["list", "--status=in_progress"])
    if in_progress:
        text.append("In Progress\n", style="bold bright_yellow")
        for line in in_progress.splitlines():
            line = line.strip()
            if line and ("SK-" in line or "issue" in line.lower()):
                text.append(f"  {line}\n", style="yellow")
    else:
        text.append("No work in progress\n", style="dim")

    text.append("\n")

    # Ready work
    ready = _run_bd(["ready"])
    if ready:
        text.append("Ready\n", style="bold bright_cyan")
        count = 0
        for line in ready.splitlines():
            line = line.strip()
            if line and ("SK-" in line):
                text.append(f"  {line}\n", style="cyan")
                count += 1
                if count >= 5:
                    text.append("  ...\n", style="dim")
                    break
    else:
        text.append("No ready work\n", style="dim")

    return Panel(text, title="Beads", border_style="bright_red", expand=True)
