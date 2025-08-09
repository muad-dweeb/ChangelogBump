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

    @pytest.mark.parametrize(
        "v1, v2, expected",
        [
            (Version(1, 0, 0), Version(2, 0, 0), False),
            (Version(2, 0, 0), Version(1, 9, 9), True),
            (Version(1, 2, 3), Version(1, 3, 2), False),
            (Version(1, 3, 4), Version(1, 2, 3), True),
            (Version(1, 2, 4), Version(1, 2, 5), False),
            (Version(1, 2, 4), Version(1, 2, 3), True),
            (Version(1, 2, 3), Version(1, 2, 3), False),
        ],
    )
    def test_is_greater_than(self, v1, v2, expected):
        """
        Ensure is_greater_than correctly determines if v1 is greater than v2.
        """
        assert v1.is_greater_than(v2) == expected

    @pytest.mark.parametrize(
        "version_str, major, minor, patch",
        [
            ("1.2.3", 1, 2, 3),
            ("10.0.1", 10, 0, 1),
            ("0.0.0", 0, 0, 0),
        ],
    )
    def test_from_string(self, version_str, major, minor, patch):
        """
        Ensure from_string() properly parses the string into a Version object.
        """
        v = Version.from_string(version_str)
        assert v.major == major
        assert v.minor == minor
        assert v.patch == patch
