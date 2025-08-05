from pathlib import Path
from typing import Iterator

import pytest
import toml

from changelogbump.PyProject import PyProject
from changelogbump.Version import Version


class TestPyProject:
    @pytest.fixture
    def mock_file(self, tmp_path, monkeypatch) -> Iterator[Path]:
        mock = tmp_path / "pyproject.toml"
        mock.write_text("""[project]
name = "mock_proj"
version = "0.1.0"
""")
        monkeypatch.setattr(PyProject, "path", mock)
        yield mock

    def test_current_version(self, mock_file, monkeypatch):
        """
        Ensure current_version retrieves the value of the project's version from pyproject.toml.
        """
        assert PyProject().current_version == "0.1.0"

    def test_current_version_missing_file(self, monkeypatch):
        monkeypatch.setattr(PyProject, "path", Path("/not_real.toml"))
        with pytest.raises(FileNotFoundError, match="Missing file"):
            _ = PyProject().current_version

    def test_update(self, mock_file, monkeypatch):
        """
        Ensure update() properly sets a new version in pyproject.toml.
        """
        # Use the Version class to specify a new version
        new_version = Version(major=1, minor=2, patch=3)
        PyProject.update(new_version.current)

        # Reload file to check that version changed
        data = toml.load(mock_file)
        assert data["project"]["version"] == "1.2.3"
