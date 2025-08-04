from changelogbump.Changelog import Changelog


class TestChangelog:
    def test_generate_sections(self, monkeypatch):
        """
        Ensure generate_sections() collects user input until empty entries
        and organizes them under 'added', 'changed', and 'removed'.
        """
        # Simulate user inputs; each call to click.prompt returns the next item in this list,
        # then stops for each section after an empty response.
        user_inputs = iter(
            [
                "First added entry",
                "Second added entry",
                "",
                "Changed item",
                "",
                "Removed item",
                "",
            ]
        )

        def mock_prompt(*args, **kwargs):
            return next(user_inputs)

        monkeypatch.setattr("click.prompt", mock_prompt)

        result = Changelog.generate_sections()
        assert "added" in result and result["added"] == [
            "First added entry",
            "Second added entry",
        ]
        assert "changed" in result and result["changed"] == ["Changed item"]
        assert "removed" in result and result["removed"] == ["Removed item"]

    def test_update_inserts_new_version_top(self, monkeypatch, tmp_path):
        """
        Check that update() inserts a new version entry before the first existing version heading
        and writes the modified changelog back to file.
        """
        # Mock out the generate_sections method to control its output.
        monkeypatch.setattr(
            Changelog,
            "generate_sections",
            lambda: {"added": ["Mocked entry"], "changed": [], "removed": []},
        )

        # Create a simulated file content and assign path to tmp_path for testing file operations.
        original_content = """# Changelog

## [0.1.0] - 2025-08-01
Some existing changelog text
"""
        changelog_file = tmp_path / "CHANGELOG.md"
        changelog_file.write_text(original_content)

        # Point Changelog.path to our tmp file instead of the project root.
        monkeypatch.setattr(Changelog, "path", changelog_file)

        # Run update with a test version
        Changelog.update(new_version="0.2.0", summary_text="Test summary")

        updated_text = changelog_file.read_text()
        # Verify new version section is inserted before [0.1.0]
        assert "## [0.2.0]" in updated_text
        new_version_idx = updated_text.index("## [0.2.0]")
        old_version_idx = updated_text.index("## [0.1.0]")
        assert new_version_idx < old_version_idx
        assert "Mocked entry" in updated_text
        assert "Test summary" in updated_text

    def test_update_appends_if_no_headings_found(self, monkeypatch, tmp_path):
        """
        Check that update() appends a new version entry if no existing version headings are present.
        """
        # Mock generate_sections again
        monkeypatch.setattr(
            Changelog,
            "generate_sections",
            lambda: {"added": ["Mocked add"], "changed": [], "removed": []},
        )

        # Original file has no version headings
        original_content = "# Changelog\n\nSome text but no version headings\n"
        changelog_file = tmp_path / "CHANGELOG.md"
        changelog_file.write_text(original_content)

        monkeypatch.setattr(Changelog, "path", changelog_file)

        Changelog.update(new_version="1.0.0")

        updated_text = changelog_file.read_text()
        # Since no headings found, new version text should appear at the end
        assert updated_text.strip().endswith("### Added\n\n- Mocked add")
        assert "## [1.0.0]" in updated_text
