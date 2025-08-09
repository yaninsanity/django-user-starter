"""Test CLI functionality."""

import unittest
from unittest.mock import patch

from django_user_starter.cli import main_en, main_zh, run_script


class TestCLI(unittest.TestCase):
    """Test CLI functions."""

    def test_run_script_file_not_found(self):
        """Test run_script raises SystemExit when script not found."""
        with self.assertRaises(SystemExit):
            run_script("nonexistent_script.sh")

    @patch("django_user_starter.cli.subprocess.call")
    @patch("django_user_starter.cli.os.chmod")
    @patch("django_user_starter.cli.os.path.exists")
    def test_run_script_success(self, mock_exists, mock_chmod, mock_call):
        """Test successful script execution."""
        mock_exists.return_value = True
        mock_call.return_value = 0

        run_script("test_script.sh")

        mock_chmod.assert_called_once()
        mock_call.assert_called_once()

    @patch("django_user_starter.cli.run_script")
    def test_main_zh(self, mock_run_script):
        """Test main_zh calls run_script with correct argument."""
        main_zh()
        mock_run_script.assert_called_once_with("starter-zh.sh")

    @patch("django_user_starter.cli.run_script")
    def test_main_en(self, mock_run_script):
        """Test main_en calls run_script with correct argument."""
        main_en()
        mock_run_script.assert_called_once_with("starter-en.sh")


if __name__ == "__main__":
    unittest.main()
