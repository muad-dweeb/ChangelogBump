"""Handles reading and updating the project's pyproject.toml file.

This module provides the PyProject class for retrieving and updating the
current version in pyproject.toml.
"""

from pathlib import Path

import toml

from changelogbump.Version import Version


class PyProject:
    """Manages interactions with the project's pyproject.toml."""

    path: Path = Path("pyproject.toml")

    @property
    def current_version(self) -> str:
        """Retrieve the current version from pyproject.toml.

        Returns:
            str: The version string as specified in pyproject.toml.
        """

        content = toml.load(self.path)
        return content["project"]["version"]

    @classmethod
    def update(cls, new_version: Version):
        """Set the new version in pyproject.toml.

        Args:
            new_version (Version): The new version to write into the file.
        """
        data = toml.load(cls.path)
        data["project"]["version"] = new_version.current
        with cls.path.open("w") as fh:
            toml.dump(data, fh)  # type: ignore
