import pytest

from changelogbump import PyProject
from changelogbump.Changelog import Changelog
from changelogbump.util import inspect_project


def test_successful_inspection(tmp_path, monkeypatch):
    """Test successful project inspection with consistent versions."""
    # Create pyproject.toml
    pyproject_file = tmp_path / "pyproject.toml"
    pyproject_file.write_text("""[project]
    name = "testproj"
    version = "1.2.3"
    """)
    monkeypatch.setattr(PyProject, "path", pyproject_file)

    # Create CHANGELOG.md
    changelog_file = tmp_path / "CHANGELOG.md"
    changelog_file.write_text("""# Changelog
    ## [1.2.3] - 2024-01-01
    Some changes
    """)
    monkeypatch.setattr(Changelog, "path", changelog_file)

    # This should not raise an exception
    inspect_project()


def setup_pyproject(tmp_path, version="1.2.3"):
    py_file = tmp_path / "pyproject.toml"
    py_file.write_text(f"""[project]
name = "testproj"
version = "{version}"
""")
    return py_file


def setup_changelog(tmp_path, content):
    cl_file = tmp_path / "CHANGELOG.md"
    cl_file.write_text(content)
    return cl_file


def test_pyproject_toml_missing(tmp_path, monkeypatch):
    """Test error when pyproject.toml is missing."""
    # Only create CHANGELOG.md
    changelog_file = setup_changelog(tmp_path, "# Changelog\n## [1.2.3] - 2024-01-01\n")
    monkeypatch.setattr(Changelog, "path", changelog_file)
    monkeypatch.setattr(PyProject, "path", tmp_path / "pyproject.toml")
    with pytest.raises(ValueError):
        inspect_project()


def test_changelog_missing(tmp_path, monkeypatch):
    """Test error when CHANGELOG.md is missing."""
    pyproject_file = setup_pyproject(tmp_path)
    monkeypatch.setattr(PyProject, "path", pyproject_file)
    monkeypatch.setattr(Changelog, "path", tmp_path / "CHANGELOG.md")
    # Simulate changelog not found by raising FileNotFoundError
    monkeypatch.setattr(
        Changelog,
        "get_latest_version",
        staticmethod(
            lambda: (_ for _ in ()).throw(FileNotFoundError("CHANGELOG.md not found"))
        ),
    )
    with pytest.raises(ValueError):
        inspect_project()


def test_version_mismatch(tmp_path, monkeypatch):
    """Test error on version mismatch between pyproject.toml and CHANGELOG.md."""
    pyproject_file = setup_pyproject(tmp_path, version="2.0.0")
    changelog_file = setup_changelog(tmp_path, "# Changelog\n## [1.2.3] - 2024-01-01\n")
    monkeypatch.setattr(PyProject, "path", pyproject_file)
    monkeypatch.setattr(Changelog, "path", changelog_file)
    monkeypatch.setattr(Changelog, "get_latest_version", staticmethod(lambda: "1.2.3"))
    with pytest.raises(ValueError):
        inspect_project()
