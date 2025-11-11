"""Tests for main CLI functionality."""

import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

from src.main import create_parser, main


class TestMainCLI:
    """Test cases for main CLI interface."""

    def test_create_parser(self):
        """Test argument parser creation."""
        parser = create_parser()

        assert parser is not None
        assert parser.description is not None

        # Test that required arguments are present
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

    @patch('src.main.DictionaryProcessor')
    @patch('src.main.StardictBuilder')
    @patch('src.main.setup_logging')
    def test_main_successful_run(self, mock_logging, mock_builder, mock_processor, temp_dir):
        """Test successful main execution."""
        # Create a dummy Excel file
        excel_file = temp_dir / "test.xlsx"
        excel_file.touch()

        # Mock the processor
        mock_processor_instance = MagicMock()
        mock_processor.return_value = mock_processor_instance

        # Mock the builder
        mock_builder_instance = MagicMock()
        mock_builder.return_value = mock_builder_instance
        mock_builder_instance.create_zip_packages.return_value = [Path("test.zip")]

        # Mock config
        with patch('src.main.Config') as mock_config_class:
            mock_config = MagicMock()
            mock_config.dictionary.enable_mobi_build = False
            mock_config_class.return_value = mock_config

            # Run main with mocked arguments
            with patch('sys.argv', ['main.py', str(excel_file)]):
                result = main()

                assert result == 0
                mock_processor.assert_called_once()
                mock_builder.assert_called_once()
                mock_processor_instance.process_excel_file.assert_called_once()

    @patch('src.main.setup_logging')
    def test_main_missing_excel_file(self, mock_logging):
        """Test main with missing Excel file."""
        with patch('sys.argv', ['main.py', 'nonexistent.xlsx']):
            result = main()

            assert result == 1

    @patch('src.main.setup_logging')
    def test_main_invalid_config(self, mock_logging, temp_dir):
        """Test main with invalid configuration."""
        excel_file = temp_dir / "test.xlsx"
        excel_file.touch()

        with patch('sys.argv', ['main.py', str(excel_file)]):
            with patch('src.main.Config') as mock_config_class:
                mock_config = MagicMock()
                mock_config.validate.side_effect = ValueError("Invalid config")
                mock_config_class.return_value = mock_config

                result = main()

                assert result == 1

    @patch('src.main.setup_logging')
    @patch('src.main.shutil.which')
    def test_main_mobi_warning(self, mock_which, mock_logging, temp_dir):
        """Test MOBI warning when calibre not available."""
        excel_file = temp_dir / "test.xlsx"
        excel_file.touch()

        # Mock calibre not available
        mock_which.return_value = None

        with patch('sys.argv', ['main.py', str(excel_file)]):
            with patch('src.main.Config') as mock_config_class:
                with patch('src.main.DictionaryProcessor') as mock_processor:
                    with patch('src.main.StardictBuilder') as mock_builder:
                        mock_config = MagicMock()
                        mock_config.dictionary.enable_mobi_build = True
                        mock_config_class.return_value = mock_config

                        mock_processor_instance = MagicMock()
                        mock_processor.return_value = mock_processor_instance

                        mock_builder_instance = MagicMock()
                        mock_builder.return_value = mock_builder_instance
                        mock_builder_instance.create_zip_packages.return_value = []

                        result = main()

                        assert result == 0
                        # Should have printed warning and error message