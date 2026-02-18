import platform
import time

import psutil
from rich.panel import Panel
from rich.table import Table


def system_stats_panel() -> Panel:
    cpu_percent = psutil.cpu_percent(interval=0.1)

    mem = psutil.virtual_memory()
    mem_used_gb = mem.used / (1024 ** 3)
    mem_total_gb = mem.total / (1024 ** 3)
    mem_percent = mem.percent

    disk = psutil.disk_usage("/")
    disk_used_gb = disk.used / (1024 ** 3)
    disk_total_gb = disk.total / (1024 ** 3)
    disk_percent = disk.percent

    boot_time = psutil.boot_time()
    uptime_seconds = int(time.time() - boot_time)
    uptime_hours, remainder = divmod(uptime_seconds, 3600)
    uptime_minutes, _ = divmod(remainder, 60)
    uptime_str = f"{uptime_hours}h {uptime_minutes}m"

    hostname = platform.node()

    table = Table.grid(padding=(0, 1))
    table.add_column(style="bold cyan", no_wrap=True)
    table.add_column(style="white")

    table.add_row("Host", hostname)
    table.add_row("CPU", f"{cpu_percent:.1f}%")
    table.add_row(
        "Memory",
        f"{mem_percent:.1f}%  {mem_used_gb:.1f} / {mem_total_gb:.1f} GB",
    )
    table.add_row(
        "Disk",
        f"{disk_percent:.1f}%  {disk_used_gb:.1f} / {disk_total_gb:.1f} GB",
    )
    table.add_row("Uptime", uptime_str)

    return Panel(table, title="System", border_style="bright_blue")
