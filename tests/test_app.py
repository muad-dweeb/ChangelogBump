import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from click.testing import CliRunner

import changelogbump
import src.changelogbump.PyProject
from changelogbump import pyproject
from changelogbump.Changelog import Changelog
from changelogbump.app import cli, OrderCommands


class TestApp:
    def test_order_commands_list_commands(self):
        """
        Ensure OrderCommands.list_commands() returns the command names in the order declared.
        """

        order_group = OrderCommands()
        # Collect subcommands from cli
        for name, cmd in cli.commands.items():
            order_group.add_command(cmd, name)

        commands_list = order_group.list_commands(...)
        assert commands_list == ["version", "init", "add"]

    def test_version_command(self):
        """Ensure the 'version' command displays a package version."""
        runner = CliRunner()
        result = runner.invoke(cli, ["version"])
        assert result.exit_code == 0
        assert "Installed: " in result.output

    @pytest.mark.parametrize(
        "local_version, remote_version",
        [
            ("1.2.3", "1.2.3"),  # same version
            ("1.2.3", "2.0.0"),  # newer version available
        ],
    )
    def test_version_command_coverage(self, monkeypatch, local_version, remote_version):
        """Parametrized test for the 'version' command to cover both matching and newer versions."""

        def mock_local_version(_: str) -> str:
            return local_version

        def mock_remote_version() -> str:
            return remote_version

        monkeypatch.setattr("importlib.metadata.version", mock_local_version)
        monkeypatch.setattr(
            "changelogbump.Metadata._PyPiMetadata.version", mock_remote_version
        )

        runner = CliRunner()
        result = runner.invoke(cli, ["version"])
        assert result.exit_code == 0
        assert f"Installed: {local_version}" in result.output
        assert f"Available: {remote_version}" in result.output

    def test_init_creates_changelog_if_missing(self, tmp_path, monkeypatch):
        """Verify that 'init' creates a new CHANGELOG.md if none exists."""
        runner = CliRunner()

        # Point the Changelog to a temporary path
        monkeypatch.setattr(Changelog, "path", tmp_path / "CHANGELOG.md")

        # Confirm the file doesn't exist yet
        assert not Changelog.path.is_file()

        result = runner.invoke(cli, ["init"])
        assert result.exit_code == 0
        assert Changelog.path.is_file()
        assert "## [Unreleased]" in Changelog.path.read_text()

    def test_init_fails_if_changelog_exists(self, tmp_path, monkeypatch):
        """Verify that 'init' raises an error if CHANGELOG.md already exists."""
        runner = CliRunner()
        existing_changelog = tmp_path / "CHANGELOG.md"
        existing_changelog.write_text("Existing content")

        monkeypatch.setattr(Changelog, "path", existing_changelog)

        result = runner.invoke(cli, ["init"])
        assert result.exit_code != 0
        assert "already exists. Aborting." in result.output

    def test_add_command_no_flags(self):
        """Ensure the 'add' command fails if no increment flags are supplied."""
        runner = CliRunner()
        result = runner.invoke(cli, ["add"])
        assert result.exit_code != 0
        assert "Specify one of --major, --minor, or --patch." in result.output

    def test_add_command_multiple_flags(self):
        """Ensure the 'add' command fails if multiple flags are supplied."""
        runner = CliRunner()
        result = runner.invoke(cli, ["add", "--major", "--minor"])
        assert result.exit_code != 0
        assert "Only one of --major, --minor, or --patch is allowed." in result.output

    @pytest.fixture(scope="function")
    def temp_files(self, tmp_path, monkeypatch):
        pyproject_file = tmp_path / "pyproject.toml"
        pyproject_file.write_text("""[project]
        name = "testproj"
        version = "0.1.0"
        """)
        print(f"TMP PyProject: {pyproject_file}")
        monkeypatch.setattr(type(src.changelogbump.pyproject), "path", pyproject_file)

        changelog_file = tmp_path / "CHANGELOG.md"
        changelog_file.write_text("# Changelog\n")
        monkeypatch.setattr(Changelog, "path", changelog_file)
        print(f"TMP ChangeLog: {changelog_file}")

        yield

        os.remove(pyproject_file)
        os.remove(changelog_file)
        print(
            f"TMP FILES DELETED: {not pyproject_file.exists() and not changelog_file.exists()}"
        )

    @pytest.mark.parametrize(
        "flag,expected",
        [
            ("--major", "1.0.0"),
            ("--minor", "0.2.0"),
            ("--patch", "0.1.1"),
        ],
    )
    def test_add_command_bumps_version(self, temp_files, monkeypatch, flag, expected):
        """
        Ensure the 'add' command bumps version properly when major, minor, or patch is specified.
        """

        monkeypatch.setattr("click.prompt", MagicMock(return_value=""))

        runner = CliRunner()
        result = runner.invoke(cli, ["add", flag])
        assert result.exit_code == 0
        assert f"Incrementing to: {expected}" in result.output

        # Validate the updated pyproject version
        assert pyproject.current_version == expected

    def test_main_subprocess(self):
        """Launch the script as if run from the command line"""
        script: Path = changelogbump.src / "changelogbump/app.py"
        result = subprocess.run(
            [sys.executable, script, "--help"], capture_output=True, text=True
        )
        assert "Click-based CLI for application version incrementing" in result.stdout
