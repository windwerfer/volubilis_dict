"""Tests for Stardict builder functionality."""

import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

from src.stardict_builder import StardictBuilder


class TestStardictBuilder:
    """Test cases for StardictBuilder class."""

    def test_builder_initialization(self, temp_dir):
        """Test builder initialization."""
        txt_dir = temp_dir / "txt"
        stardict_dir = temp_dir / "stardict"

        builder = StardictBuilder(txt_dir, stardict_dir)

        assert builder.txt_dir == txt_dir
        assert builder.stardict_dir == stardict_dir
        assert builder.unzipped_dir == stardict_dir / "unzipped"

    @patch('subprocess.run')
    def test_convert_single_file(self, mock_subprocess, temp_dir):
        """Test single file conversion to Stardict format."""
        txt_dir = temp_dir / "txt"
        stardict_dir = temp_dir / "stardict"
        txt_dir.mkdir()
        stardict_dir.mkdir()

        # Create a dummy txt file
        txt_file = txt_dir / "test.txt"
        txt_file.write_text("test\tcontent\n")

        builder = StardictBuilder(txt_dir, stardict_dir)

        # Mock successful subprocess run
        mock_subprocess.return_value = MagicMock(stdout="", stderr="", returncode=0)

        builder._convert_single_file(txt_file)

        # Check that subprocess was called with correct arguments
        mock_subprocess.assert_called_once()
        args = mock_subprocess.call_args[0][0]
        assert "pyglossary" in args
        assert "--no-sqlite" in args
        assert str(txt_file) in args

    @patch('subprocess.run')
    def test_convert_single_file_to_mobi(self, mock_subprocess, temp_dir):
        """Test single file conversion to MOBI format."""
        txt_dir = temp_dir / "txt"
        stardict_dir = temp_dir / "stardict"
        mobi_dir = stardict_dir / "mobi"
        txt_dir.mkdir()
        stardict_dir.mkdir()

        # Create a dummy txt file
        txt_file = txt_dir / "test.txt"
        txt_file.write_text("test\tcontent\n")

        builder = StardictBuilder(txt_dir, stardict_dir)

        # Mock successful subprocess run
        mock_subprocess.return_value = MagicMock(stdout="", stderr="", returncode=0)

        builder._convert_single_file_to_mobi(txt_file, mobi_dir)

        # Check that subprocess was called with correct arguments
        mock_subprocess.assert_called_once()
        args = mock_subprocess.call_args[0][0]
        assert "ebook-convert" in args
        assert str(txt_file) in args
        assert str(mobi_dir / "test.mobi") in args

    def test_convert_to_mobi_creates_directory(self, temp_dir):
        """Test that convert_to_mobi creates the mobi directory."""
        txt_dir = temp_dir / "txt"
        stardict_dir = temp_dir / "stardict"
        txt_dir.mkdir()
        stardict_dir.mkdir()

        # Create a dummy txt file
        txt_file = txt_dir / "test.txt"
        txt_file.write_text("test\tcontent\n")

        builder = StardictBuilder(txt_dir, stardict_dir)

        # Mock the conversion method
        with patch.object(builder, '_convert_single_file_to_mobi') as mock_convert:
            builder.convert_to_mobi()

            # Check that mobi directory was created
            mobi_dir = stardict_dir / "mobi"
            assert mobi_dir.exists()

            # Check that conversion was called
            mock_convert.assert_called_once()

    def test_convert_to_mobi_removes_existing_directory(self, temp_dir):
        """Test that convert_to_mobi removes existing mobi directory."""
        txt_dir = temp_dir / "txt"
        stardict_dir = temp_dir / "stardict"
        mobi_dir = stardict_dir / "mobi"
        txt_dir.mkdir()
        stardict_dir.mkdir()
        mobi_dir.mkdir()

        # Create a file in the existing mobi directory
        old_file = mobi_dir / "old.mobi"
        old_file.write_text("old content")

        # Create a dummy txt file
        txt_file = txt_dir / "test.txt"
        txt_file.write_text("test\tcontent\n")

        builder = StardictBuilder(txt_dir, stardict_dir)

        # Mock the conversion method
        with patch.object(builder, '_convert_single_file_to_mobi') as mock_convert:
            builder.convert_to_mobi()

            # Check that old file was removed
            assert not old_file.exists()

            # Check that conversion was called
            mock_convert.assert_called_once()

    def test_convert_to_mobi_no_txt_files(self, temp_dir):
        """Test convert_to_mobi with no txt files."""
        txt_dir = temp_dir / "txt"
        stardict_dir = temp_dir / "stardict"
        txt_dir.mkdir()
        stardict_dir.mkdir()

        builder = StardictBuilder(txt_dir, stardict_dir)

        with pytest.raises(FileNotFoundError, match="No txt files found"):
            builder.convert_to_mobi()

    @patch('subprocess.run')
    def test_convert_single_file_subprocess_error(self, mock_subprocess, temp_dir):
        """Test handling of subprocess errors in file conversion."""
        txt_dir = temp_dir / "txt"
        stardict_dir = temp_dir / "stardict"
        txt_dir.mkdir()
        stardict_dir.mkdir()

        # Create a dummy txt file
        txt_file = txt_dir / "test.txt"
        txt_file.write_text("test\tcontent\n")

        builder = StardictBuilder(txt_dir, stardict_dir)

        # Mock failed subprocess run
        mock_subprocess.side_effect = Exception("Conversion failed")

        with pytest.raises(Exception, match="Conversion failed"):
            builder._convert_single_file_to_mobi(txt_file, stardict_dir / "mobi")

    def test_update_ifo_file(self, temp_dir):
        """Test IFO file updating."""
        stardict_dir = temp_dir / "stardict"
        stardict_dir.mkdir()
        ifo_file = stardict_dir / "test.ifo"

        # Create a sample IFO file
        ifo_content = """version=2.4.2
bookname=test
wordcount=100
idxfilesize=1000
author=test
description=test dictionary
"""

        ifo_file.write_text(ifo_content)

        builder = StardictBuilder(temp_dir / "txt", stardict_dir)
        builder._update_ifo_file(ifo_file)

        # Check that version and description were updated
        updated_content = ifo_file.read_text()
        assert "version=1.0.5" in updated_content
        assert "description=Volubilis Thai-English Dictionary v1.0.5" in updated_content

    def test_create_single_zip(self, temp_dir):
        """Test creation of individual zip packages."""
        txt_dir = temp_dir / "txt"
        stardict_dir = temp_dir / "stardict"
        unzipped_dir = stardict_dir / "unzipped"
        txt_dir.mkdir(parents=True)
        stardict_dir.mkdir()
        unzipped_dir.mkdir()

        # Create dummy Stardict files
        ifo_file = unzipped_dir / "test.ifo"
        idx_file = unzipped_dir / "test.idx"
        dict_file = unzipped_dir / "test.dict"

        ifo_file.write_text("dummy ifo")
        idx_file.write_text("dummy idx")
        dict_file.write_text("dummy dict")

        builder = StardictBuilder(txt_dir, stardict_dir)

        zip_file = builder._create_single_zip(ifo_file)

        # Check that zip file was created
        assert zip_file.exists()
        assert zip_file.name == "test.zip"

        # Check zip contents
        import zipfile
        with zipfile.ZipFile(zip_file, 'r') as zf:
            files = zf.namelist()
            assert "test.ifo" in files
            assert "test.idx" in files
            assert "test.dict" in files