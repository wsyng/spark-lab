import hashlib
from datetime import date

from rich.panel import Panel
from rich.text import Text

QUOTES = [
    ("The best way to predict the future is to invent it.", "Alan Kay"),
    ("Talk is cheap. Show me the code.", "Linus Torvalds"),
    ("First, solve the problem. Then, write the code.", "John Johnson"),
    ("Simplicity is the soul of efficiency.", "Austin Freeman"),
    ("Make it work, make it right, make it fast.", "Kent Beck"),
    ("Code is like humor. When you have to explain it, it's bad.", "Cory House"),
    ("The only way to go fast is to go well.", "Robert C. Martin"),
    ("Perfection is achieved when there is nothing left to take away.", "Antoine de Saint-Exupery"),
    ("Programs must be written for people to read.", "Harold Abelson"),
    ("Any fool can write code that a computer can understand.", "Martin Fowler"),
    ("Stay hungry, stay foolish.", "Steve Jobs"),
    ("Done is better than perfect.", "Sheryl Sandberg"),
    ("Ship early, ship often.", "Reid Hoffman"),
    ("Debugging is twice as hard as writing the code.", "Brian Kernighan"),
    ("Weeks of coding can save hours of planning.", "Unknown"),
    ("It works on my machine.", "Every Developer"),
    ("Move fast and build things.", "Spark Lab"),
    ("The computer was born to solve problems that did not exist before.", "Bill Gates"),
    ("In the middle of difficulty lies opportunity.", "Albert Einstein"),
    ("Imagination is more important than knowledge.", "Albert Einstein"),
    ("The only limit to our realization of tomorrow is our doubts of today.", "Franklin Roosevelt"),
    ("Creativity is intelligence having fun.", "Albert Einstein"),
]


def quote_panel() -> Panel:
    today = date.today().isoformat()
    idx = int(hashlib.md5(today.encode()).hexdigest(), 16) % len(QUOTES)
    quote, author = QUOTES[idx]

    text = Text()
    text.append(f'"{quote}"', style="italic bright_white")
    text.append(f"\n  — {author}", style="dim")

    return Panel(text, title="Quote of the Day", border_style="bright_magenta")
