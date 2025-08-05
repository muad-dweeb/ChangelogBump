"""This module defines a CLI using Click for version incrementing and
CHANGELOG initialization. The following commands are provided:

  - init: Initialize a fresh CHANGELOG.md file if one does not exist.
  - add: Increment the project's version and update the changelog accordingly.

Typical usage example:

    changelogbump init

The CLI commands automatically handle errors and print
concise messages via Click exceptions.
"""

import os

import click
from click import Command

from changelogbump import header_path, pyproject
from changelogbump.Changelog import Changelog
from changelogbump.PyProject import PyProject
from changelogbump.Version import Version


class OrderCommands(click.Group):
    def list_commands(self, ctx: click.Context) -> list[str]:
        return list(self.commands)


@click.group(cls=OrderCommands)
def cli() -> Command:
    """Click-based CLI for application version incrementing and CHANGELOG management."""
    pass


@cli.command()
def init():
    """Initialize a fresh CHANGELOG.md in the project root."""
    if os.path.isfile(Changelog.path):
        raise click.ClickException(f"{Changelog.path} already exists. Aborting.")
    with open(Changelog.path, "w") as changelog:
        with open(header_path, "r") as header:
            changelog.write(header.read())


@cli.command()
@click.option("--major", "-M", is_flag=True, help="Increment major version number.")
@click.option("--minor", "-m", is_flag=True, help="Increment minor version number.")
@click.option("--patch", "-p", is_flag=True, help="Increment patch version number.")
@click.option(
    "--summary", "-s", is_flag=False, help="Version descriptive summary header."
)
def add(major, minor, patch, summary):
    """Increment version by one of the semantic parts (major|minor|patch)."""
    if sum([major, minor, patch]) > 1:
        raise click.ClickException(
            "Only one of --major, --minor, or --patch is allowed."
        )
    if not any([major, minor, patch]):
        raise click.ClickException("Specify one of --major, --minor, or --patch.")

    maj_str, min_str, pat_str = pyproject.current_version.split(".")
    version = Version(int(maj_str), int(min_str), int(pat_str))
    print(f"Current version: {version.current}")
    version.bump(major, minor, patch)
    print(f"Incrementing to: {version.current}")
    Changelog.update(version.current, summary)
    PyProject.update(version.current)


if __name__ == "__main__":
    cli()
