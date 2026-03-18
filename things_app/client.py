"""Unified client for Things — the single entry point for all operations.

Wraps the `things` library (reads Things' SQLite DB) with typed models
and a consistent API.
"""

from __future__ import annotations

from .models import Area, Project, Tag, Task


def _require_things():
    """Import the things library, raising a clear error if not installed."""
    try:
        import things
        return things
    except ModuleNotFoundError:
        raise RuntimeError(
            "things-py requires the 'things.py' package.\n"
            "Install with: pip install things.py"
        )


class ThingsClient:
    """Things client.

    Provides read access to Things tasks, projects, areas, and tags
    via the things.py library (SQLite DB reader).
    """

    # ── Tasks ────────────────────────────────────────────────────────

    def get_tasks(
        self,
        *,
        project: str | None = None,
        area: str | None = None,
        tag: str | None = None,
        status: str | None = "incomplete",
        start: str | None = None,
        search: str | None = None,
        include_items: bool = False,
    ) -> list[Task]:
        """Get tasks, optionally filtered.

        Args:
            project: Filter by project UUID.
            area: Filter by area UUID.
            tag: Filter by tag title.
            status: "incomplete", "completed", "canceled", or None (all).
            start: "Inbox", "Anytime", "Someday", or None.
            search: Search query (SQL LIKE pattern).
            include_items: Include sub-items (checklist items, headings).
        """
        things = _require_things()
        kwargs = {}
        if project is not None:
            kwargs["project"] = project
        if area is not None:
            kwargs["area"] = area
        if tag is not None:
            kwargs["tag"] = tag
        if status is not None:
            kwargs["status"] = status
        if start is not None:
            kwargs["start"] = start
        if search is not None:
            kwargs["search_query"] = search
        kwargs["include_items"] = include_items

        raw = things.tasks(**kwargs)
        if isinstance(raw, dict):
            raw = [raw]
        return [self._to_task(t) for t in raw]

    def get_task(self, uuid: str) -> Task | None:
        """Get a single task by UUID."""
        things = _require_things()
        raw = things.tasks(uuid=uuid)
        if not raw:
            return None
        if isinstance(raw, list):
            raw = raw[0]
        return self._to_task(raw)

    # ── Projects ─────────────────────────────────────────────────────

    def get_projects(
        self,
        *,
        status: str | None = "incomplete",
        area: str | None = None,
        tag: str | None = None,
    ) -> list[Project]:
        """Get projects, optionally filtered."""
        things = _require_things()
        kwargs = {"type": "project"}
        if status is not None:
            kwargs["status"] = status
        if area is not None:
            kwargs["area"] = area
        if tag is not None:
            kwargs["tag"] = tag
        raw = things.tasks(**kwargs)
        if isinstance(raw, dict):
            raw = [raw]
        return [self._to_project(p) for p in raw]

    # ── Areas ────────────────────────────────────────────────────────

    def get_areas(self) -> list[Area]:
        """Get all areas."""
        things = _require_things()
        raw = things.areas()
        return [
            Area(
                uuid=a["uuid"],
                title=a["title"],
                tags=a.get("tags", []) or [],
            )
            for a in raw
        ]

    # ── Tags ─────────────────────────────────────────────────────────

    def get_tags(self) -> list[Tag]:
        """Get all tags."""
        things = _require_things()
        raw = things.tags()
        return [
            Tag(
                uuid=t["uuid"],
                title=t["title"],
                shortcut=t.get("shortcut"),
            )
            for t in raw
        ]

    # ── Inbox / Today / Upcoming ─────────────────────────────────────

    def inbox(self) -> list[Task]:
        """Get inbox tasks."""
        return self.get_tasks(start="Inbox")

    def today(self) -> list[Task]:
        """Get tasks scheduled for today."""
        things = _require_things()
        raw = things.today()
        if isinstance(raw, dict):
            raw = [raw]
        return [self._to_task(t) for t in raw]

    # ── Show ─────────────────────────────────────────────────────────

    def show(self, uuid: str) -> bool:
        """Open an item in Things. Returns True if found."""
        things = _require_things()
        item = things.get(uuid)
        if item:
            things.show(uuid)
            return True
        return False

    # ── Internal ─────────────────────────────────────────────────────

    @staticmethod
    def _to_task(raw: dict) -> Task:
        return Task(
            uuid=raw["uuid"],
            title=raw.get("title", ""),
            status=raw.get("status", "incomplete"),
            notes=raw.get("notes", ""),
            tags=raw.get("tags", []) or [],
            project=raw.get("project"),
            project_title=raw.get("project_title"),
            area=raw.get("area"),
            area_title=raw.get("area_title"),
            heading=raw.get("heading"),
            heading_title=raw.get("heading_title"),
            start=raw.get("start"),
            start_date=raw.get("start_date"),
            deadline=raw.get("deadline"),
            stop_date=raw.get("stop_date"),
            created=raw.get("created"),
            modified=raw.get("modified"),
            index=raw.get("index", 0),
            today_index=raw.get("today_index", 0),
        )

    @staticmethod
    def _to_project(raw: dict) -> Project:
        return Project(
            uuid=raw["uuid"],
            title=raw.get("title", ""),
            status=raw.get("status", "incomplete"),
            notes=raw.get("notes", ""),
            tags=raw.get("tags", []) or [],
            area=raw.get("area"),
            area_title=raw.get("area_title"),
            start=raw.get("start"),
            start_date=raw.get("start_date"),
            deadline=raw.get("deadline"),
            stop_date=raw.get("stop_date"),
            created=raw.get("created"),
            modified=raw.get("modified"),
            index=raw.get("index", 0),
        )
