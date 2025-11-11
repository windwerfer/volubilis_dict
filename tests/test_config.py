"""Tests for configuration management."""

import pytest
from pathlib import Path

from src.config import Config, DictionaryConfig, RegexPatterns


class TestRegexPatterns:
    """Test regex pattern configurations."""

    def test_patterns_initialization(self):
        """Test that regex patterns are properly initialized."""
        patterns = RegexPatterns()

        assert isinstance(patterns.remove_brackets, dict)
        assert isinstance(patterns.remove_starting_brackets, dict)
        assert isinstance(patterns.type_friendly_1, dict)
        assert isinstance(patterns.type_friendly_2, dict)
        assert isinstance(patterns.pron, dict)
        assert isinstance(patterns.pron2, dict)
        assert isinstance(patterns.default, dict)
        assert isinstance(patterns.final_pron, dict)
        assert isinstance(patterns.classifier, dict)

    def test_remove_brackets_patterns(self):
        """Test bracket removal patterns."""
        patterns = RegexPatterns()

        # Test that patterns contain expected keys
        assert r"[…\.\[\]\(\)]" in patterns.remove_brackets
        assert r"[\u0300\u0301\u0302\u030c]" in patterns.remove_brackets

    def test_type_friendly_patterns(self):
        """Test type-friendly transformation patterns."""
        patterns = RegexPatterns()

        assert "ø̅" in patterns.type_friendly_1
        assert "øø" == patterns.type_friendly_1["ø̅"]
        assert "ā" in patterns.type_friendly_1
        assert "aa" == patterns.type_friendly_1["ā"]


class TestDictionaryConfig:
    """Test dictionary configuration."""

    def test_default_config(self):
        """Test default configuration values."""
        config = DictionaryConfig()

        assert config.columns == 32
        assert config.paiboon is True
        assert config.debug is False
        assert config.debug_test_1000_rows is True  # Updated default
        assert config.th_pron is True
        assert config.th_pron_prefix == '.'
        assert config.enable_mobi_build is True

    def test_excel_file_validation(self, temp_dir):
        """Test Excel file validation."""
        config = Config()
        config.dictionary.excel_file = temp_dir / "nonexistent.xlsx"

        # Should raise ValueError for missing file
        with pytest.raises(ValueError, match="Excel file not found"):
            config.validate()

    def test_column_validation(self, temp_dir):
        """Test column count validation."""
        config = Config()
        config.dictionary.excel_file = temp_dir / "test.xlsx"
        config.dictionary.excel_file.touch()  # Create dummy file
        config.dictionary.columns = 0

        with pytest.raises(ValueError, match="Columns must be positive"):
            config.validate()

    def test_column_mapping_validation(self, temp_dir):
        """Test column mapping validation."""
        config = Config()
        config.dictionary.excel_file = temp_dir / "test.xlsx"
        config.dictionary.excel_file.touch()  # Create dummy file
        config.dictionary.columns = 5  # Less than max column index

        with pytest.raises(ValueError, match="Column mapping references column"):
            config.validate()

    def test_column_mapping_keys(self):
        """Test that all expected column mapping keys exist."""
        config = DictionaryConfig()

        expected_keys = [
            'thai_romanized', 'easythai', 'thaiphon', 'thai', 'thai_pron_added',
            'english', 'french', 'type', 'usage', 'scient', 'dom', 'classif',
            'syn', 'level', 'note', 'spanish', 'italian', 'portuguese',
            'german', 'dutch', 'norwegian', 'turkish', 'malay', 'indonesian',
            'filipino', 'vietnamese', 'russian1', 'russian2', 'lao1', 'lao2',
            'korean1', 'korean2'
        ]

        for key in expected_keys:
            assert key in config.COLUMN_MAPPING
            assert isinstance(config.COLUMN_MAPPING[key], int)


class TestConfig:
    """Test main configuration class."""

    def test_config_creation(self):
        """Test config creation."""
        config = Config()
        assert isinstance(config.dictionary, DictionaryConfig)

    def test_config_from_file(self):
        """Test config loading from file (currently returns defaults)."""
        config = Config.from_file()
        assert isinstance(config, Config)
        assert isinstance(config.dictionary, DictionaryConfig)

    def test_config_validation(self, temp_dir):
        """Test full config validation."""
        config = Config()
        config.dictionary.excel_file = temp_dir / "test.xlsx"

        # Create a dummy file for validation
        config.dictionary.excel_file.touch()

        # Should not raise any errors
        config.validate()