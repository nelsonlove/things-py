"""Tests for Things data models."""
from dataclasses import asdict

from things_app.models import Task, Project, Area, Tag


class TestTask:
    def test_creation(self):
        t = Task(uuid="abc", title="Buy milk")
        assert t.uuid == "abc"
        assert t.title == "Buy milk"
        assert t.status == "incomplete"
        assert t.tags == []

    def test_defaults(self):
        t = Task(uuid="x", title="T")
        assert t.notes == ""
        assert t.project is None
        assert t.deadline is None
        assert t.index == 0

    def test_asdict(self):
        t = Task(uuid="abc", title="Buy milk", tags=["errands"])
        d = asdict(t)
        assert d["uuid"] == "abc"
        assert d["tags"] == ["errands"]
        assert isinstance(d, dict)


class TestProject:
    def test_creation(self):
        p = Project(uuid="p1", title="Home reno")
        assert p.status == "incomplete"
        assert p.tags == []

    def test_with_area(self):
        p = Project(uuid="p1", title="Home reno", area="a1", area_title="Home")
        assert p.area_title == "Home"


class TestArea:
    def test_creation(self):
        a = Area(uuid="a1", title="Work")
        assert a.tags == []


class TestTag:
    def test_creation(self):
        t = Tag(uuid="t1", title="Urgent", shortcut="u")
        assert t.shortcut == "u"

    def test_no_shortcut(self):
        t = Tag(uuid="t1", title="Low")
        assert t.shortcut is None
