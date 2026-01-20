"""Yomichan format conversion and packaging utilities."""

import logging
import subprocess
import zipfile
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
        self.unzipped_dir = yomitan_dir / "unzipped"
        self.css_content = css_content
        self.config = config

    def convert_to_yomitan(self) -> List[Path]:
        """Convert all txt files to Yomichan format."""
        # Inline CSS styles in txt files
        self._inline_styles()

        # Create unzipped directory
        self.unzipped_dir.mkdir(exist_ok=True)

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

        # Output the zip to unzipped dir first
        temp_zip = self.unzipped_dir / f"{output_name}.zip"
        final_zip = self.yomitan_dir / f"{output_name}.zip"

        logger.info(f"Converting {txt_file} to {final_zip} using Yomichan format")

        try:
            cmd = ["pyglossary", "--write-format=Yomichan", str(txt_file), str(temp_zip)]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
            )

            logger.debug(f"pyglossary output: {result.stdout}")

            # Unzip to unzipped dir
            with zipfile.ZipFile(temp_zip, 'r') as zf:
                zf.extractall(self.unzipped_dir)

            # Remove the temp zip
            temp_zip.unlink()

            # Zip the unzipped files with compression level 6
            with zipfile.ZipFile(final_zip, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
                for file_path in self.unzipped_dir.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(self.unzipped_dir)
                        zf.write(file_path, arcname)
                        logger.debug(f"Added {file_path} as {arcname} to {final_zip}")

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to convert {txt_file}: {e}")
            logger.error(f"stderr: {e.stderr}")
            raise

        return final_zip