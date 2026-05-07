# thingsapp

Read-only Python library and CLI for Things.app on macOS.

## Features

- Query tasks, projects, areas, and tags from Things.app
- Filter by project, area, tag, status, or search query
- Built-in views: inbox, today
- Structured JSON output with `--json`

## Installation

```bash
pip install thingsapp  # or: pipx install thingsapp
```

## CLI

```bash
things --help
things tasks --project UUID --tag "tagname" --status completed
things tasks --search "groceries"
things projects --all
things areas
things tags
things inbox
things today
things --json tasks
```

## Python API

```python
from things_app.client import ThingsClient

client = ThingsClient()
tasks = client.get_tasks(tag="errand", status="incomplete")
projects = client.get_projects()
areas = client.get_areas()
tags = client.get_tags()
inbox = client.inbox()
today = client.today()
```

## Development

```bash
git clone https://github.com/nelsonlove/things-py.git
cd things-py
uv sync --extra dev
uv run pytest
uv run things --help
```

## License

MIT
