---
name: things
description: Query Things.app tasks, projects, areas, and tags. Use when the user asks about their tasks, to-do list, projects, what's due, inbox, or today's schedule.
---

# Things.app Queries

Read-only access to Things.app via the `things` CLI.

## Commands

```bash
things tasks                          # all incomplete tasks
things tasks --project UUID           # tasks in a project
things tasks --tag "Work"             # tasks with a tag
things tasks --search "keyword"       # search tasks
things tasks --status completed       # completed tasks
things tasks --all                    # all statuses

things projects                       # incomplete projects
things projects --all                 # all projects

things areas                          # all areas
things tags                           # all tags
things inbox                          # inbox tasks
things today                          # today's tasks
```

## JSON mode

Always use `--json` for structured output:

```bash
things --json tasks
things --json today
things --json inbox
```

Returns: `{"status": "ok", "data": [...]}`

## Data model

- **Task**: uuid, title, status, notes, tags, project_title, area_title, deadline, start_date
- **Project**: uuid, title, status, notes, tags, area_title, deadline
- **Area**: uuid, title, tags
- **Tag**: uuid, title, shortcut

## Notes

- Read-only — Things data comes from the SQLite database
- No write operations (creating tasks requires the Things URL scheme)
- Status values: "incomplete", "completed", "canceled"
