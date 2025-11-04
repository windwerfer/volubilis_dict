"""Tests for text formatting utilities."""

import pytest
from src.config import RegexPatterns
from src.text_formatter import TextFormatter


class TestTextFormatter:
    """Test cases for TextFormatter class."""

    @pytest.fixture
    def formatter(self):
        """Create a TextFormatter instance."""
        patterns = RegexPatterns()
        return TextFormatter(patterns)

    def test_clean_text(self, formatter):
        """Test text cleaning."""
        assert formatter.clean_text("  test  ") == "test"
        assert formatter.clean_text("None") == ""
        assert formatter.clean_text("") == ""
        assert formatter.clean_text("valid text") == "valid text"

    def test_format_tones_paiboon(self, formatter):
        """Test tone formatting with Paiboon."""
        # Test basic tone conversion
        result = formatter.format_tones("maa", paiboon=True)
        assert "maa" in result

    def test_format_tones_no_paiboon(self, formatter):
        """Test tone formatting without Paiboon."""
        result = formatter.format_tones("maa", paiboon=False)
        assert isinstance(result, str)

    def test_split_and_format_classifiers(self, formatter):
        """Test classifier splitting and formatting."""
        result = formatter.split_and_format_classifiers("คน; สัตว์", paiboon=True)
        assert "คน" in result
        assert "สัตว์" in result

    def test_split_and_format_synonyms(self, formatter):
        """Test synonym splitting and formatting."""
        result = formatter.split_and_format_synonyms("big; large", paiboon=True)
        assert "big" in result
        assert "large" in result

    def test_replace_multi(self, formatter):
        """Test multiple regex replacements."""
        replacements = {"a": "b", "c": "d"}
        result = formatter.replace_multi("abcd", replacements)
        assert result == "bbdd"