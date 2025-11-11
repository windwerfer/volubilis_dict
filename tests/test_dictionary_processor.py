"""Tests for dictionary processing logic."""

import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

from src.dictionary_processor import DictionaryProcessor


class TestDictionaryProcessor:
    """Test cases for DictionaryProcessor class."""

    def test_processor_initialization(self, mock_config):
        """Test processor initialization."""
        processor = DictionaryProcessor(mock_config)

        assert processor.config == mock_config.dictionary
        assert processor.formatter is not None
        assert processor.file_handler is not None

    def test_cache_key_generation(self, mock_config):
        """Test cache key generation."""
        processor = DictionaryProcessor(mock_config)

        key1 = processor._generate_cache_key()
        key2 = processor._generate_cache_key()

        assert key1 == key2
        assert isinstance(key1, str)
        assert len(key1) == 32  # MD5 hash length

    def test_cache_key_changes_with_config(self, mock_config):
        """Test that cache key changes when config changes."""
        processor = DictionaryProcessor(mock_config)

        key1 = processor._generate_cache_key()
        mock_config.dictionary.columns = 16
        key2 = processor._generate_cache_key()

        assert key1 != key2

    def test_convert_defaultdict_to_dict(self, mock_config):
        """Test defaultdict to dict conversion."""
        from collections import defaultdict

        processor = DictionaryProcessor(mock_config)

        # Test nested defaultdict conversion
        nested_dd = defaultdict(lambda: defaultdict(list))
        nested_dd['key1']['subkey1'].append('value1')
        nested_dd['key1']['subkey2'].append('value2')

        result = processor._convert_defaultdict_to_dict(nested_dd)

        assert isinstance(result, dict)
        assert 'key1' in result
        assert isinstance(result['key1'], dict)
        assert result['key1']['subkey1'] == ['value1']
        assert result['key1']['subkey2'] == ['value2']

    def test_get_sort_prefix(self, mock_config):
        """Test sort prefix generation."""
        processor = DictionaryProcessor(mock_config)

        assert processor._get_sort_prefix("") == "  "
        assert processor._get_sort_prefix("A") == "A "
        assert processor._get_sort_prefix("A1") == "A1"
        assert processor._get_sort_prefix("ABC") == "AB"

    def test_format_level_info(self, mock_config):
        """Test level and domain information formatting."""
        processor = DictionaryProcessor(mock_config)

        # Test with level only
        result = processor._format_level_info("A1", "")
        assert "Level: A1" in result

        # Test with level and domain
        result = processor._format_level_info("A1", "animal")
        assert "Level: A1" in result
        assert "Category: animal" in result

        # Test with no level or domain
        result = processor._format_level_info("", "")
        assert result == ""

    @patch('src.dictionary_processor.OPENPYXL_AVAILABLE', False)
    def test_process_excel_mock_data(self, mock_config, temp_dir):
        """Test processing with mock data when openpyxl unavailable."""
        mock_config.dictionary.output_folder = temp_dir / "output"
        processor = DictionaryProcessor(mock_config)

        processor._process_mock_data()

        # Check that output files were created
        output_files = list((temp_dir / "output").glob("*.txt"))
        assert len(output_files) > 0

        # Check content of one file
        th_en_file = temp_dir / "output" / "volubilis_th-en.txt"
        assert th_en_file.exists()

        content = th_en_file.read_text(encoding='utf-8')
        assert "สวัสดี" in content
        assert "sawadee" in content

    def test_open_output_files(self, mock_config, temp_dir):
        """Test output file opening."""
        mock_config.dictionary.output_folder = temp_dir / "output"
        mock_config.dictionary.th_pron_merge = True
        processor = DictionaryProcessor(mock_config)

        # Ensure output directory exists (normally done by process_excel_file)
        processor.file_handler.ensure_directory(mock_config.dictionary.output_folder)

        files = processor._open_output_files()

        expected_files = ['th_en', 'th_pron_en', 'en_th', 'th_pron_merge_en']
        for key in expected_files:
            assert key in files
            assert hasattr(files[key], 'write')

        # Close files
        for f in files.values():
            f.close()

    def test_process_row_valid_data(self, mock_config):
        """Test processing a valid data row."""
        from collections import defaultdict
        processor = DictionaryProcessor(mock_config)

        # Sample row data (matching column mapping)
        row = ("", "", "sà-wàt-dii", "สวัสดี", "sawadee", "", "", "greeting", "common", "", "", "", "", "A1", "")

        th_en_data = defaultdict(list)
        th_pron_en_data = defaultdict(list)
        th_pron_merge_en_data = defaultdict(list)
        en_th_data = defaultdict(lambda: defaultdict(list))

        result = processor._process_row(row, th_en_data, th_pron_en_data, th_pron_merge_en_data, en_th_data)

        assert result is True
        assert "สวัสดี" in th_en_data
        assert len(th_en_data["สวัสดี"]) == 1

    def test_process_row_invalid_data(self, mock_config):
        """Test processing invalid data rows."""
        from collections import defaultdict
        processor = DictionaryProcessor(mock_config)

        # Row with missing required data
        row = ("", "", "", "", "", "", "", "", "", "", "", "", "", "", "")
        th_en_data = defaultdict(list)
        th_pron_en_data = defaultdict(list)
        th_pron_merge_en_data = defaultdict(list)
        en_th_data = defaultdict(lambda: defaultdict(list))

        result = processor._process_row(row, th_en_data, th_pron_en_data, th_pron_merge_en_data, en_th_data)

        assert result is False
        assert len(th_en_data) == 0

    def test_format_definition(self, mock_config):
        """Test definition formatting."""
        processor = DictionaryProcessor(mock_config)

        result = processor._format_definition(
            thai="แมว",
            pron_formatted="mɛɛw",
            type_word="noun",
            usage="common",
            classif="ตัว",
            syn="",
            scient="",
            note="",
            level="A1",
            english="cat",
            dom="animal"
        )

        assert "แมว" in result
        assert "mɛɛw" in result
        assert "noun" in result
        assert "cat" in result
        assert "Level: A1" in result
        assert "Category: animal" in result

    def test_add_english_to_thai_entries(self, mock_config):
        """Test adding English to Thai entries."""
        from collections import defaultdict
        processor = DictionaryProcessor(mock_config)

        en_th_data = defaultdict(lambda: defaultdict(list))
        definition = '<span class="thai">แมว</span> <span class="pron">[mɛɛw]</span> <span class="type">noun</span> <span class="def">cat</span>'

        processor._add_english_to_thai_entries("cat", definition, "noun", en_th_data)

        assert "cat" in en_th_data
        assert "noun" in en_th_data["cat"]
        assert len(en_th_data["cat"]["noun"]) == 1