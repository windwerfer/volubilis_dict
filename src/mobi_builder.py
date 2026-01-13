"""MOBI format conversion utilities."""

import logging
import shutil
import subprocess
from pathlib import Path
from typing import Optional

from .config import DictionaryConfig

logger = logging.getLogger(__name__)


class MobiBuilder:
    """Handles conversion to MOBI format for Kindle."""

    def __init__(
        self,
        mobi_txt_dir: Path,
        mobi_dir: Path,
        css_content: Optional[str] = None,
        config: Optional[DictionaryConfig] = None,
    ):
        self.mobi_txt_dir = mobi_txt_dir
        self.mobi_dir = mobi_dir
        self.css_content = css_content
        self.config = config

    def convert_to_mobi(self) -> None:
        """Convert all txt files to MOBI format for Kindle."""
        self.mobi_dir.mkdir(parents=True, exist_ok=True)
        # Remove any existing .mobi files to avoid conflicts
        for mobi_file in self.mobi_dir.glob("*.mobi"):
            mobi_file.unlink()

        txt_files = list(self.mobi_txt_dir.glob("volubilis_*.txt"))
        if not txt_files:
            raise FileNotFoundError(f"No txt files found in {self.mobi_txt_dir}")

        for txt_file in txt_files:
            self._convert_single_file_to_mobi(txt_file)

    def _convert_single_file_to_mobi(self, txt_file: Path) -> None:
        """Convert a single txt file to MOBI format."""
        # Always use inline CSS for MOBI
        html_file = self._create_inline_css_html(txt_file)
        output_name = txt_file.stem
        output_file = self.mobi_dir / f"{output_name}.mobi"

        logger.info(f"Converting {html_file} to {output_file}")

        try:
            result = subprocess.run(
                ["ebook-convert", str(html_file), str(output_file)],
                capture_output=True,
                text=True,
                check=True,
            )

            logger.debug(f"ebook-convert output: {result.stdout}")

            # Clean up temporary HTML file
            html_file.unlink()

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to convert {txt_file} to MOBI: {e}")
            logger.error(f"stderr: {e.stderr}")
            # Clean up temporary HTML file even on error
            if html_file.exists():
                html_file.unlink()
            raise

    def _create_inline_css_html(self, txt_file: Path) -> Path:
        """Create an HTML version for MOBI conversion."""
        html_file = txt_file.with_suffix('.html')

        # Read the tab-separated txt file
        with open(txt_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Create HTML content
        html_content = []
        html_content.append('<?xml version="1.0" encoding="utf-8"?>')
        html_content.append('<!DOCTYPE html>')
        html_content.append('<html>')
        html_content.append('<head>')
        html_content.append('<meta charset="utf-8">')
        html_content.append('<title>Volubilis Dictionary</title>')
        html_content.append('</head>')
        html_content.append('<body>')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Split by tab
            parts = line.split('\t', 1)
            if len(parts) == 2:
                headword, definition = parts
                html_content.append(f'<div class="entry">')
                html_content.append(f'<div class="headword">{headword}</div>')
                html_content.append(f'<div class="definition">{definition}</div>')
                html_content.append('</div>')
                html_content.append('<br>')

        html_content.append('</body>')
        html_content.append('</html>')

        # Write HTML file
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(html_content))

        return html_file