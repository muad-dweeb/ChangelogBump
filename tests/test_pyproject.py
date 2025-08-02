import toml

from changelogbump.PyProject import PyProject
from changelogbump.Version import Version


class TestPyProject:
    def test_current_version(self, tmp_path, monkeypatch):
        """
        Ensure current_version retrieves the value of the project's version from pyproject.toml.
        """
        mock_file = tmp_path / "pyproject.toml"
        mock_file.write_text("""[project]
name = "mockproj"
version = "0.1.0"
""")

        # Point our PyProject path to the temporary file
        monkeypatch.setattr(PyProject, "path", mock_file)

        pyproject = PyProject()
        assert pyproject.current_version == "0.1.0"

    def test_update(self, tmp_path, monkeypatch):
        """
        Ensure update() properly sets a new version in pyproject.toml.
        """
        mock_file = tmp_path / "pyproject.toml"
        mock_file.write_text("""[project]
name = "mockproj"
version = "0.1.0"
""")

        monkeypatch.setattr(PyProject, "path", mock_file)

        # Use the Version class to specify a new version
        new_version = Version(major=1, minor=2, patch=3)
        PyProject.update(new_version)

        # Reload file to check that version changed
        data = toml.load(mock_file)
        assert data["project"]["version"] == "1.2.3"
