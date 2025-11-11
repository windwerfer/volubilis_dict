"""Tests for file handling utilities."""

import pytest
from pathlib import Path

from src.file_handler import FileHandler


class TestFileHandler:
    """Test cases for FileHandler class."""

    def test_file_handler_creation(self):
        """Test file handler creation."""
        handler = FileHandler()
        assert handler is not None

    def test_ensure_directory_exists(self, temp_dir):
        """Test directory creation."""
        test_dir = temp_dir / "test_dir" / "subdir"

        handler = FileHandler()
        handler.ensure_directory(test_dir)

        assert test_dir.exists()
        assert test_dir.is_dir()

    def test_ensure_directory_parent_exists(self, temp_dir):
        """Test that parent directories are created."""
        test_file = temp_dir / "deep" / "nested" / "path" / "file.txt"

        handler = FileHandler()
        handler.ensure_directory(test_file.parent)

        assert test_file.parent.exists()
        assert test_file.parent.is_dir()

    def test_ensure_directory_no_error_if_exists(self, temp_dir):
        """Test that no error occurs if directory already exists."""
        test_dir = temp_dir / "existing_dir"
        test_dir.mkdir()

        handler = FileHandler()
        # Should not raise an error
        handler.ensure_directory(test_dir)

        assert test_dir.exists()

    def test_ensure_directory_with_file_conflict(self, temp_dir):
        """Test behavior when trying to create directory where file exists."""
        test_file = temp_dir / "conflict"
        test_file.write_text("content")

        handler = FileHandler()

        # This should work - pathlib handles this case
        conflict_dir = temp_dir / "conflict" / "subdir"
        handler.ensure_directory(conflict_dir)

        assert conflict_dir.exists()
        assert conflict_dir.is_dir()
        # Original file should still exist
        assert test_file.exists()
        assert test_file.is_file()