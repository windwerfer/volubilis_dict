"""Shared test fixtures and configuration."""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock

from src.config import Config, DictionaryConfig
from src.dictionary_processor import DictionaryProcessor
from src.text_formatter import TextFormatter
from src.file_handler import FileHandler


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_config(temp_dir):
    """Create a mock configuration for testing."""
    config = Config()
    config.dictionary.excel_file = temp_dir / "test.xlsx"
    config.dictionary.output_folder = temp_dir / "output"
    config.dictionary.cache_file = temp_dir / "cache.pkl"
    config.dictionary.use_cache = False  # Disable caching for tests
    config.dictionary.debug_test_1000_rows = True
    config.dictionary.enable_mobi_build = False  # Disable MOBI for tests
    return config


@pytest.fixture
def text_formatter():
    """Create a TextFormatter instance."""
    from src.config import RegexPatterns
    patterns = RegexPatterns()
    return TextFormatter(patterns)


@pytest.fixture
def file_handler():
    """Create a FileHandler instance."""
    return FileHandler()


@pytest.fixture
def sample_excel_data():
    """Sample Excel-like data for testing."""
    return [
        ["", "", "sà-wàt-dii", "สวัสดี", "sawadee", "hello", "", "greeting", "common", "", "", "", "", "A1", ""],
        ["", "", "khòp-khùn", "ขอบคุณ", "khopkhun", "thank you", "", "expression", "common", "", "", "", "", "A1", ""],
        ["", "", "mɛɛw", "แมว", "maew", "cat", "", "noun", "common", "", "animal", "ตัว", "", "A1", ""],
    ]


@pytest.fixture
def mock_openpyxl():
    """Mock openpyxl for testing without actual Excel files."""
    mock_wb = Mock()
    mock_ws = Mock()
    mock_ws.values = [
        ["THAIROM", "EASYTHAI", "THAIPHON", "THA", "ENG", "FRA", "TYPE", "USAGE", "SCIENT", "DOM", "CLASSIF", "SYN", "LEVEL", "NOTE"],
        ["", "", "sà-wàt-dii", "สวัสดี", "sawadee", "hello", "", "greeting", "common", "", "", "", "", "A1", ""],
        ["", "", "khòp-khùn", "ขอบคุณ", "khopkhun", "thank you", "", "expression", "common", "", "", "", "", "A1", ""],
        ["", "", "mɛɛw", "แมว", "maew", "cat", "", "noun", "common", "", "animal", "ตัว", "", "A1", ""],
    ]
    mock_ws.reset_dimensions = Mock()
    mock_wb.active = mock_ws
    mock_wb.sheetnames = ["Sheet1"]

    mock_load = Mock(return_value=mock_wb)

    import sys
    from unittest.mock import patch
    with patch('src.dictionary_processor.load_workbook', mock_load):
        yield mock_load