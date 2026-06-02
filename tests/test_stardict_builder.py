"""Tests for Stardict builder functionality."""

import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

from volubilis_dict.stardict_builder import StardictBuilder
from volubilis_dict import __version__
from volubilis_dict.config import DictionaryConfig


class TestStardictBuilder:
    """Test cases for StardictBuilder class."""

    def test_builder_initialization(self, temp_dir):
        """Test builder initialization."""
        txt_dir = temp_dir / "txt"
        stardict_dir = temp_dir / "stardict"
        cfg = DictionaryConfig()

        builder = StardictBuilder(txt_dir, stardict_dir, config=cfg)

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

        cfg = DictionaryConfig(no_dz=False)
        builder = StardictBuilder(txt_dir, stardict_dir, config=cfg)

        # Mock successful subprocess run
        mock_subprocess.return_value = MagicMock(stdout="", stderr="", returncode=0)

        # The real convert would create the ifo; simulate it for _update_ifo_file
        output_ifo = stardict_dir / "unzipped" / "test.ifo"
        output_ifo.parent.mkdir(parents=True, exist_ok=True)
        output_ifo.write_text("version=2.4\nwordcount=1\nidxfilesize=10\nbookname=test\ndate=2026\nsametypesequence=m\n")

        with patch.object(builder, '_update_ifo_file') as mock_update:
            builder._convert_single_file(txt_file)

        # Check that subprocess was called with correct arguments
        mock_subprocess.assert_called_once()
        args = mock_subprocess.call_args[0][0]
        assert "pyglossary" in args
        assert "--no-sqlite" in args
        assert str(txt_file) in args
        mock_update.assert_called_once()

    # MOBI conversion was moved to separate MobiBuilder; these tests removed.

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

        cfg = DictionaryConfig()
        builder = StardictBuilder(txt_dir, stardict_dir, config=cfg)

        # Mock failed subprocess run
        mock_subprocess.side_effect = Exception("Conversion failed")

        with pytest.raises(Exception, match="Conversion failed"):
            builder._convert_single_file(txt_file)

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

        cfg = DictionaryConfig()
        builder = StardictBuilder(temp_dir / "txt", stardict_dir, config=cfg)
        builder._update_ifo_file(ifo_file)

        # Check that version and description were updated
        updated_content = ifo_file.read_text()
        assert f"version={__version__}" in updated_content
        assert f"description=Volubilis Thai-English Dictionary v{__version__}" in updated_content

    def test_create_zip_packages(self, temp_dir):
        """Test creation of combined zip package."""
        txt_dir = temp_dir / "txt"
        stardict_dir = temp_dir / "stardict"
        unzipped_dir = stardict_dir / "unzipped"
        txt_dir.mkdir(parents=True)
        stardict_dir.mkdir()
        unzipped_dir.mkdir()

        # Create dummy Stardict files for one dict
        ifo_file = unzipped_dir / "test.ifo"
        idx_file = unzipped_dir / "test.idx"
        dict_file = unzipped_dir / "test.dict.dz"

        ifo_file.write_text("dummy ifo")
        idx_file.write_text("dummy idx")
        dict_file.write_text("dummy dict")

        cfg = DictionaryConfig(no_dz=False, inline_css=True)  # avoid res.zip side effect
        builder = StardictBuilder(txt_dir, stardict_dir, config=cfg)

        zip_files = builder.create_zip_packages()

        # Should have created the combined zip
        assert len(zip_files) == 1
        zip_file = zip_files[0]
        assert zip_file.exists()
        assert zip_file.name == "volubilis_all_stardict.zip"

        # Check zip contents
        import zipfile
        with zipfile.ZipFile(zip_file, 'r') as zf:
            files = zf.namelist()
            assert "test.ifo" in files
            assert "test.idx" in files
            assert "test.dict.dz" in files