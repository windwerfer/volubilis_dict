"""Tests for main CLI functionality."""

import sys
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

# Import via the thin root main.py wrapper (which adds src/ to path and re-exports from volubilis_dict.cli)
sys.path.insert(0, str(Path(__file__).parent.parent))
from main import create_parser, main


class TestMainCLI:
    """Test cases for main CLI interface."""

    def test_create_parser(self):
        """Test argument parser creation."""
        parser = create_parser()

        assert parser is not None
        assert parser.description is not None

        # Test that required arguments are present (positional excel_file)
        args = parser.parse_args(['test.xlsx'])
        assert args.excel_file == Path('test.xlsx')

    def test_parser_default_values(self):
        """Test parser default values."""
        parser = create_parser()
        args = parser.parse_args(['dummy.xlsx'])

        assert args.output_dir == Path('stardict/txt')
        assert args.columns == 32
        assert args.no_paiboon is False
        assert args.debug_1000 is False
        assert args.verbose is False
        assert args.inline_css is False
        assert args.no_dz is False
        assert args.create_mobi is False

    def test_parser_debug_1000_flag(self):
        """Test debug-1000 flag parsing."""
        parser = create_parser()
        args = parser.parse_args(['dummy.xlsx', '--debug-1000'])

        assert args.debug_1000 is True

    def test_parser_verbose_flag(self):
        """Test verbose flag parsing."""
        parser = create_parser()
        args = parser.parse_args(['dummy.xlsx', '--verbose'])

        assert args.verbose is True

    def test_parser_output_dir(self):
        """Test output directory parsing."""
        parser = create_parser()
        args = parser.parse_args(['dummy.xlsx', '--output-dir', 'custom_output'])

        assert args.output_dir == Path('custom_output')

    def test_parser_columns(self):
        """Test columns argument parsing."""
        parser = create_parser()
        args = parser.parse_args(['dummy.xlsx', '--columns', '16'])

        assert args.columns == 16

    @patch('volubilis_dict.cli.setup_logging')
    def test_main_missing_excel_file(self, mock_logging):
        """Test main with missing Excel file."""
        with patch('sys.argv', ['main.py', 'nonexistent.xlsx']):
            result = main()

            assert result == 1

    @patch('volubilis_dict.cli.setup_logging')
    def test_main_invalid_config(self, mock_logging, temp_dir):
        """Test main with invalid configuration."""
        excel_file = temp_dir / "test.xlsx"
        excel_file.touch()

        with patch('sys.argv', ['main.py', str(excel_file)]):
            with patch('volubilis_dict.cli.Config') as mock_config_class:
                mock_config = MagicMock()
                mock_config.validate.side_effect = ValueError("Invalid config")
                mock_config_class.return_value = mock_config

                result = main()

                assert result == 1

    # Note: Full end-to-end main() success tests are integration level and
    # require mocking many builders (UtilsBuilder, MdictBuilder, YomitanBuilder,
    # StardictBuilder, ...). Parser and error-path tests above cover CLI wiring.
    # Complex pipeline tests belong in integration or manual runs.