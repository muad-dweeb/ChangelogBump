import pytest
from changelogbump.Version import Version

class TestVersion:
    @pytest.fixture
    def version(self):
        yield Version(1, 2, 3)

    def test_initial_current(self, version):
        """
        Verify that the current property returns 'major.minor.patch'.
        """
        assert version.current == "1.2.3"

    @pytest.mark.parametrize(
        "major, minor, patch, expected",
        [
            (True, False, False, "2.0.0"),  # major bump
            (False, True, False, "1.3.0"),  # minor bump
            (False, False, True, "1.2.4"),  # patch bump
        ],
    )
    def test_bump_parameterized(self, version, major, minor, patch, expected):
        """
        Test various bump scenarios using parameterization.
        """
        version.bump(major=major, minor=minor, patch=patch)
        assert version.current == expected

    def test_bump_error_if_no_flags(self, version):
        """
        Ensure bump() raises an AttributeError if no part is specified.
        """
        with pytest.raises(AttributeError):
            version.bump()
