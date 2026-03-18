"""Data classes for Things objects."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass
class Task:
    """A Things to-do."""

    uuid: str
    title: str
    status: str = "incomplete"
    notes: str = ""
    tags: list[str] = field(default_factory=list)
    project: str | None = None
    project_title: str | None = None
    area: str | None = None
    area_title: str | None = None
    heading: str | None = None
    heading_title: str | None = None
    start: str | None = None
    start_date: date | None = None
    deadline: date | None = None
    stop_date: date | None = None
    created: datetime | None = None
    modified: datetime | None = None
    index: int = 0
    today_index: int = 0


@dataclass
class Project:
    """A Things project."""

    uuid: str
    title: str
    status: str = "incomplete"
    notes: str = ""
    tags: list[str] = field(default_factory=list)
    area: str | None = None
    area_title: str | None = None
    start: str | None = None
    start_date: date | None = None
    deadline: date | None = None
    stop_date: date | None = None
    created: datetime | None = None
    modified: datetime | None = None
    index: int = 0


@dataclass
class Area:
    """A Things area."""

    uuid: str
    title: str
    tags: list[str] = field(default_factory=list)


@dataclass
class Tag:
    """A Things tag."""

    uuid: str
    title: str
    shortcut: str | None = None
