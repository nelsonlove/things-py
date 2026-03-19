---
name: things
description: Query Things.app tasks, projects, areas, and tags. Use when the user asks about their tasks, to-do list, projects, what's due, inbox, or today's schedule.
---

# Things.app Queries

Read-only access to Things.app via the `things` CLI.

## Commands

```bash
${CLAUDE_PLUGIN_ROOT}/bin/run things tasks                          # all incomplete tasks
${CLAUDE_PLUGIN_ROOT}/bin/run things tasks --project UUID           # tasks in a project
${CLAUDE_PLUGIN_ROOT}/bin/run things tasks --tag "Work"             # tasks with a tag
${CLAUDE_PLUGIN_ROOT}/bin/run things tasks --search "keyword"       # search tasks
${CLAUDE_PLUGIN_ROOT}/bin/run things tasks --status completed       # completed tasks
${CLAUDE_PLUGIN_ROOT}/bin/run things tasks --all                    # all statuses

${CLAUDE_PLUGIN_ROOT}/bin/run things projects                       # incomplete projects
${CLAUDE_PLUGIN_ROOT}/bin/run things projects --all                 # all projects

${CLAUDE_PLUGIN_ROOT}/bin/run things areas                          # all areas
${CLAUDE_PLUGIN_ROOT}/bin/run things tags                           # all tags
${CLAUDE_PLUGIN_ROOT}/bin/run things inbox                          # inbox tasks
${CLAUDE_PLUGIN_ROOT}/bin/run things today                          # today's tasks
```

## JSON mode

Always use `--json` for structured output:

```bash
${CLAUDE_PLUGIN_ROOT}/bin/run things --json tasks
${CLAUDE_PLUGIN_ROOT}/bin/run things --json today
${CLAUDE_PLUGIN_ROOT}/bin/run things --json inbox
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
