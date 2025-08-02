"""Manages semantic versioning for the application.

This module provides the Version dataclass with properties and methods that
handle version increments according to the semantic versioning specification.
"""

from dataclasses import dataclass


@dataclass
class Version:
    """Represents a semantic version number.

    Attributes:
        major (int): The major version component.
        minor (int): The minor version component.
        patch (int): The patch version component.
    """

    major: int
    minor: int
    patch: int

    @property
    def current(self) -> str:
        """Return the current version as a string in the format 'major.minor.patch'."""
        return f"{self.major}.{self.minor}.{self.patch}"

    def bump(
        self, major: bool = False, minor: bool = False, patch: bool = False
    ) -> None:
        """Increment one of the semantic version parts.

        Args:
            major (bool, optional): If True, increase the major version and reset the minor and patch. Defaults to False.
            minor (bool, optional): If True, increase the minor version and reset the patch. Defaults to False.
            patch (bool, optional): If True, increase the patch version. Defaults to False.

        Raises:
            AttributeError: If none of major, minor, or patch is True.
        """
        if major:
            self.major += 1
            self.minor = 0
            self.patch = 0
        elif minor:
            self.minor += 1
            self.patch = 0
        elif patch:
            self.patch += 1
        else:
            raise AttributeError("must provide one of ['major', 'minor', 'patch']")
