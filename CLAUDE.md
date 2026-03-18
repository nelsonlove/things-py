# things-py

Python library and CLI for Things.app on macOS.

## Architecture

```
things_app/
  client.py    ← ThingsClient: unified API (single entry point)
  models.py    ← Data classes: Task, Project, Area, Tag
  cli.py       ← Click CLI (calls ThingsClient)
plugin/
  claude-code/ ← Claude Code plugin
```

Dependency direction: `plugin → CLI → ThingsClient → things.py library → SQLite`

Things.app data is read-only via the `things.py` library (reads the SQLite DB directly).
Write operations would require the Things URL scheme (`things:///add?...`).

## Development

```bash
uv run pytest           # run tests
uv run things --help    # run CLI
```

## CLI conventions

- `things --json <command>` for structured JSON output
- Envelope: `{"status": "ok", "data": ...}`
- Read-only — no write operations yet
