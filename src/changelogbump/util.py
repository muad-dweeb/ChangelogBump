from pathlib import Path
import click

from changelogbump.Changelog import Changelog
from changelogbump.PyProject import PyProject


def inspect_project():
    """
    Perform a comprehensive project version inspection.

    Raises:
        ValueError: If any inconsistencies are found.
    """
    errors = []
    warnings = []

    # Check pyproject.toml
    try:
        pyproject = PyProject()
        pyproject_version = pyproject.current_version
        click.echo(
            "Project version: " + click.style(pyproject_version, fg="blue", bold=True)
        )
    except FileNotFoundError as e:
        errors.append(str(e))
        pyproject_version = None

    # Check changelog
    try:
        changelog_version = Changelog.get_latest_version()
        if changelog_version:
            click.echo(
                "Latest changelog version: "
                + click.style(changelog_version, fg="green", bold=True)
            )
        else:
            warnings.append("No version entries found in changelog")
    except FileNotFoundError as e:
        errors.append(str(e))
        changelog_version = None

    # Compare versions
    if pyproject_version and changelog_version:
        if pyproject_version != changelog_version:
            errors.append(
                f"Version mismatch: pyproject.toml ({pyproject_version}) != CHANGELOG.md ({changelog_version})"
            )

    # Display project path
    click.echo(
        f"Project path: {click.style(str(Path.cwd().absolute()), fg='bright_black')}"
    )

    # Handle warnings and errors
    if warnings:
        click.echo()
        click.echo(click.style("Warnings:", fg="yellow", bold=True))
        for warning in warnings:
            click.echo(click.style(f"  ⚠ {warning}", fg="yellow"))

    if errors:
        click.echo()
        click.echo(click.style("Errors:", fg="red", bold=True))
        for error in errors:
            click.echo(click.style(f"  ✗ {error}", fg="red"))
        raise ValueError("Project inspection failed")

    click.echo(click.style("✓ Project inspection passed", fg="green", bold=True))
