"""Tests for Things CLI — --json output and command structure."""
import json
from unittest.mock import patch, MagicMock

from click.testing import CliRunner

from things_app.cli import cli
from things_app.models import Task, Project, Area, Tag


MOCK_TASKS = [
    Task(uuid="t1", title="Buy milk", status="incomplete", tags=["errands"]),
    Task(uuid="t2", title="Write report", status="incomplete", project_title="Work"),
]

MOCK_PROJECTS = [
    Project(uuid="p1", title="Home reno", status="incomplete"),
]

MOCK_AREAS = [Area(uuid="a1", title="Work"), Area(uuid="a2", title="Home")]
MOCK_TAGS = [Tag(uuid="tg1", title="Urgent", shortcut="u")]


def _mock_client():
    client = MagicMock()
    client.get_tasks.return_value = MOCK_TASKS
    client.get_projects.return_value = MOCK_PROJECTS
    client.get_areas.return_value = MOCK_AREAS
    client.get_tags.return_value = MOCK_TAGS
    client.inbox.return_value = [MOCK_TASKS[0]]
    client.today.return_value = MOCK_TASKS
    return client


class TestTasksJson:
    @patch("things_app.cli.ThingsClient")
    def test_tasks_json(self, mock_cls):
        mock_cls.return_value = _mock_client()
        runner = CliRunner()
        result = runner.invoke(cli, ["--json", "tasks"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["status"] == "ok"
        assert len(data["data"]) == 2
        assert data["data"][0]["title"] == "Buy milk"

    @patch("things_app.cli.ThingsClient")
    def test_tasks_human(self, mock_cls):
        mock_cls.return_value = _mock_client()
        runner = CliRunner()
        result = runner.invoke(cli, ["tasks"])
        assert result.exit_code == 0
        assert "Buy milk" in result.output


class TestProjectsJson:
    @patch("things_app.cli.ThingsClient")
    def test_projects_json(self, mock_cls):
        mock_cls.return_value = _mock_client()
        runner = CliRunner()
        result = runner.invoke(cli, ["--json", "projects"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["data"][0]["title"] == "Home reno"


class TestAreasJson:
    @patch("things_app.cli.ThingsClient")
    def test_areas_json(self, mock_cls):
        mock_cls.return_value = _mock_client()
        runner = CliRunner()
        result = runner.invoke(cli, ["--json", "areas"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data["data"]) == 2


class TestTagsJson:
    @patch("things_app.cli.ThingsClient")
    def test_tags_json(self, mock_cls):
        mock_cls.return_value = _mock_client()
        runner = CliRunner()
        result = runner.invoke(cli, ["--json", "tags"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["data"][0]["shortcut"] == "u"


class TestInboxJson:
    @patch("things_app.cli.ThingsClient")
    def test_inbox_json(self, mock_cls):
        mock_cls.return_value = _mock_client()
        runner = CliRunner()
        result = runner.invoke(cli, ["--json", "inbox"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data["data"]) == 1


class TestTodayJson:
    @patch("things_app.cli.ThingsClient")
    def test_today_json(self, mock_cls):
        mock_cls.return_value = _mock_client()
        runner = CliRunner()
        result = runner.invoke(cli, ["--json", "today"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data["data"]) == 2


class TestHelp:
    def test_main_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "tasks" in result.output
        assert "projects" in result.output

    def test_tasks_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["tasks", "--help"])
        assert result.exit_code == 0
        assert "--project" in result.output
        assert "--tag" in result.output
