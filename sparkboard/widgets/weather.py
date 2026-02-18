import time
import requests
from rich.panel import Panel
from rich.text import Text

_cache: dict = {}
_CACHE_TTL = 30 * 60  # 30 minutes in seconds


def _fetch_weather() -> dict | None:
    now = time.time()
    if _cache.get("data") and now - _cache.get("timestamp", 0) < _CACHE_TTL:
        return _cache["data"]

    try:
        response = requests.get("https://wttr.in/?format=j1", timeout=5)
        response.raise_for_status()
        data = response.json()
        _cache["data"] = data
        _cache["timestamp"] = now
        return data
    except Exception:
        return None


def weather_panel() -> Panel:
    data = _fetch_weather()

    if data is None:
        content = Text("Weather unavailable", style="dim")
        return Panel(content, title="Weather", border_style="yellow")

    try:
        current = data["current_condition"][0]
        temp_f = current["temp_F"]
        feels_like_f = current["FeelsLikeF"]
        condition = current["weatherDesc"][0]["value"]
        humidity = current["humidity"]
        wind_mph = current["windspeedMiles"]
    except (KeyError, IndexError):
        content = Text("Weather unavailable", style="dim")
        return Panel(content, title="Weather", border_style="yellow")

    content = Text()
    content.append(f"{condition}\n", style="bold white")
    content.append(f"{temp_f}°F", style="bold yellow")
    content.append(f"  feels like {feels_like_f}°F\n", style="dim")
    content.append(f"Humidity: ", style="cyan")
    content.append(f"{humidity}%\n", style="white")
    content.append(f"Wind:     ", style="cyan")
    content.append(f"{wind_mph} mph", style="white")

    return Panel(content, title="Weather", border_style="yellow")
