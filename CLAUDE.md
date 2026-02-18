# Spark Lab

A creative lab project — Claude builds, Wesy taste-tests. Ideas ignite here.

## Project Overview

This is an experimental sandbox where Claude autonomously designs and builds a cool app, session by session. The goal is to explore what's possible when an AI agent drives development with minimal direction.

## Beads Integration

This project uses [Beads (bd)](https://github.com/steveyegge/beads) for issue tracking and automatic session memory.

### Session Start Protocol
1. Run `bd ready` to see available work
2. Check `.beads/PRIME.md` for session state
3. Pick up where the last session left off

### Session End Protocol
1. Update issue status: `bd update <id> --status=<status>`
2. Update `.beads/PRIME.md` with what you did
3. Sync: `bd sync`

### Quick Reference
- `bd ready` — show ready work
- `bd list --status=open` — all open issues
- `bd create --title="..." --type=task` — create issue
- `bd update <id> --status=in_progress` — claim work
- `bd close <id>` — mark complete
- `bd sync` — sync with git
