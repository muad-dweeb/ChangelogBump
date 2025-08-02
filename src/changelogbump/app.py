import os

import click

from changelogbump import header_path
from changelogbump.Bumper import Bumper
from changelogbump.Changelog import Changelog
from changelogbump.PyProject import PyProject


class OrderCommands(click.Group):
    def list_commands(self, ctx: click.Context) -> list[str]:
        return list(self.commands)


@click.group(cls=OrderCommands)
def cli():
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

    bumper = Bumper()
    new_version = bumper.bump(major, minor, patch)
    print(f"Current version: {bumper.current}")
    print(f"Incrementing to: {new_version}")
    Changelog.update(new_version, summary)
    PyProject.update(new_version)


if __name__ == "__main__":
    cli()
