"""Click CLI for Things — thin layer over ThingsClient."""

import json
import sys
from dataclasses import asdict

import click

from .client import ThingsClient


@click.group()
@click.option("--json", "as_json", is_flag=True, envvar="THINGS_OUTPUT",
              help="Output as JSON (structured envelope).")
@click.pass_context
def cli(ctx, as_json):
    """Read and query Things.app tasks, projects, areas, and tags."""
    ctx.ensure_object(dict)
    ctx.obj["client"] = ThingsClient()
    ctx.obj["json"] = as_json


def _client(ctx) -> ThingsClient:
    return ctx.obj["client"]


def _emit(ctx, data):
    click.echo(json.dumps({"status": "ok", "data": data}, indent=2, default=str))


# ── tasks ────────────────────────────────────────────────────────────────

@cli.command("tasks")
@click.option("--project", default=None, help="Filter by project UUID.")
@click.option("--area", default=None, help="Filter by area UUID.")
@click.option("--tag", default=None, help="Filter by tag title.")
@click.option("--status", default="incomplete",
              type=click.Choice(["incomplete", "completed", "canceled"]),
              help="Filter by status.")
@click.option("--all", "all_status", is_flag=True, help="Include all statuses.")
@click.option("--search", default=None, help="Search query.")
@click.pass_context
def list_tasks(ctx, project, area, tag, status, all_status, search):
    """List tasks."""
    client = _client(ctx)
    tasks = client.get_tasks(
        project=project, area=area, tag=tag,
        status=None if all_status else status,
        search=search,
    )

    if ctx.obj["json"]:
        _emit(ctx, [asdict(t) for t in tasks])
        return

    if not tasks:
        click.echo("No tasks found.")
        return

    for t in tasks:
        flag = "*" if t.status == "completed" else " "
        tags = f" [{', '.join(t.tags)}]" if t.tags else ""
        proj = f" ({t.project_title})" if t.project_title else ""
        due = f" due:{t.deadline}" if t.deadline else ""
        click.echo(f" {flag} {t.title}{proj}{tags}{due}")


# ── projects ─────────────────────────────────────────────────────────────

@cli.command("projects")
@click.option("--status", default="incomplete",
              type=click.Choice(["incomplete", "completed", "canceled"]))
@click.option("--all", "all_status", is_flag=True, help="Include all statuses.")
@click.pass_context
def list_projects(ctx, status, all_status):
    """List projects."""
    client = _client(ctx)
    projects = client.get_projects(status=None if all_status else status)

    if ctx.obj["json"]:
        _emit(ctx, [asdict(p) for p in projects])
        return

    if not projects:
        click.echo("No projects found.")
        return

    for p in projects:
        area = f" [{p.area_title}]" if p.area_title else ""
        click.echo(f"  {p.title}{area}")


# ── areas ────────────────────────────────────────────────────────────────

@cli.command("areas")
@click.pass_context
def list_areas(ctx):
    """List areas."""
    client = _client(ctx)
    areas = client.get_areas()

    if ctx.obj["json"]:
        _emit(ctx, [asdict(a) for a in areas])
        return

    for a in areas:
        click.echo(f"  {a.title}")


# ── tags ─────────────────────────────────────────────────────────────────

@cli.command("tags")
@click.pass_context
def list_tags(ctx):
    """List tags."""
    client = _client(ctx)
    tags = client.get_tags()

    if ctx.obj["json"]:
        _emit(ctx, [asdict(t) for t in tags])
        return

    for t in tags:
        shortcut = f" ({t.shortcut})" if t.shortcut else ""
        click.echo(f"  {t.title}{shortcut}")


# ── inbox ────────────────────────────────────────────────────────────────

@cli.command("inbox")
@click.pass_context
def inbox_cmd(ctx):
    """List inbox tasks."""
    client = _client(ctx)
    tasks = client.inbox()

    if ctx.obj["json"]:
        _emit(ctx, [asdict(t) for t in tasks])
        return

    if not tasks:
        click.echo("Inbox is empty.")
        return

    for t in tasks:
        click.echo(f"  {t.title}")


# ── today ────────────────────────────────────────────────────────────────

@cli.command("today")
@click.pass_context
def today_cmd(ctx):
    """List today's tasks."""
    client = _client(ctx)
    tasks = client.today()

    if ctx.obj["json"]:
        _emit(ctx, [asdict(t) for t in tasks])
        return

    if not tasks:
        click.echo("Nothing scheduled for today.")
        return

    for t in tasks:
        proj = f" ({t.project_title})" if t.project_title else ""
        click.echo(f"  {t.title}{proj}")
