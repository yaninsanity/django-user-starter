"""Test version management."""

import unittest

from django_user_starter import __version__


class TestVersion(unittest.TestCase):
    """Test version functionality."""

    def test_version_exists(self):
        """Test that version is defined."""
        self.assertIsNotNone(__version__)
        self.assertIsInstance(__version__, str)

    def test_version_format(self):
        """Test version follows semantic versioning format."""
        # Basic semantic version regex pattern
        pattern = r"^\d+\.\d+\.\d+(?:-[\w\d\.]+)*$"
        self.assertRegex(__version__, pattern)


if __name__ == "__main__":
    unittest.main()
