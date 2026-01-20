"""Yomichan format conversion and packaging utilities."""

import logging
import subprocess
from pathlib import Path
from typing import List, Optional

from .config import DictionaryConfig

logger = logging.getLogger(__name__)


class YomitanBuilder:
    """Handles conversion to Yomichan format."""

    def __init__(
        self,
        txt_dir: Path,
        yomitan_dir: Path,
        css_content: Optional[str] = None,
        config: Optional[DictionaryConfig] = None,
    ):
        self.txt_dir = txt_dir
        self.yomitan_dir = yomitan_dir
        self.css_content = css_content
        self.config = config

    def convert_to_yomitan(self) -> List[Path]:
        """Convert all txt files to Yomichan format."""
        # Inline CSS styles in txt files
        self._inline_styles()

        output_files = []

        txt_files = list(self.txt_dir.glob("volubilis_*.txt"))
        if not txt_files:
            raise FileNotFoundError(f"No txt files found in {self.txt_dir}")

        for txt_file in txt_files:
            output_file = self._convert_single_file(txt_file)
            output_files.append(output_file)

        return output_files

    def _inline_styles(self) -> None:
        """Inline CSS styles in Yomitan txt files by replacing classes with style attributes."""
        import re

        txt_files = list(self.txt_dir.glob("volubilis_*.txt"))
        for txt_file in txt_files:
            content = txt_file.read_text(encoding="utf-8")
            # Remove any <style> blocks
            content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
            # Apply style replacements
            if self.config and self.config.style_mapping:
                for class_attr, style_attr in self.config.style_mapping.items():
                    content = content.replace(class_attr, style_attr)
            txt_file.write_text(content, encoding="utf-8")

    def _convert_single_file(self, txt_file: Path) -> Path:
        """Convert a single txt file to Yomichan format."""
        # Use the txt file stem as the output name
        output_name = txt_file.stem
        logger.debug(f"Processing file: {txt_file.name}, output: {output_name}")

        output_file = self.yomitan_dir / f"{output_name}.zip"

        logger.info(f"Converting {txt_file} to {output_file} using Yomichan format")

        try:
            cmd = ["pyglossary", "--write-format=Yomichan", str(txt_file), str(output_file)]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
            )

            logger.debug(f"pyglossary output: {result.stdout}")

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to convert {txt_file}: {e}")
            logger.error(f"stderr: {e.stderr}")
            raise

        return output_file