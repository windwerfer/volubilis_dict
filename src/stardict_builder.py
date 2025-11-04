"""Stardict format conversion and packaging utilities."""

import logging
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)


class StardictBuilder:
    """Handles conversion to Stardict format and packaging."""

    def __init__(self, txt_dir: Path, stardict_dir: Path):
        self.txt_dir = txt_dir
        self.stardict_dir = stardict_dir
        self.unzipped_dir = stardict_dir / "unzipped"

    def convert_to_stardict(self) -> None:
        """Convert all txt files to Stardict format."""
        self.unzipped_dir.mkdir(parents=True, exist_ok=True)

        txt_files = list(self.txt_dir.glob("volubilis_*.txt"))
        if not txt_files:
            raise FileNotFoundError(f"No txt files found in {self.txt_dir}")

        for txt_file in txt_files:
            self._convert_single_file(txt_file)

    def _convert_single_file(self, txt_file: Path) -> None:
        """Convert a single txt file to Stardict format."""
        # Use the txt file stem as the output name
        output_name = txt_file.stem
        logger.debug(f"Processing file: {txt_file.name}, output: {output_name}")

        output_file = self.unzipped_dir / f"{output_name}.ifo"

        logger.info(f"Converting {txt_file} to {output_file}")

        try:
            result = subprocess.run([
                "pyglossary",
                str(txt_file), str(output_file)
            ], capture_output=True, text=True, check=True)

            logger.debug(f"pyglossary output: {result.stdout}")

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to convert {txt_file}: {e}")
            logger.error(f"stderr: {e.stderr}")
            raise

    def create_zip_packages(self) -> List[Path]:
        """Create individual zip packages for each dictionary."""
        zip_files = []

        # Copy res.zip to txt dir as css.zip if it exists
        res_zip = Path("stardict/tmp/res.zip")
        css_zip = self.txt_dir / "css.zip"
        if res_zip.exists():
            shutil.copy(res_zip, css_zip)

        # Find all .ifo files and create zips
        ifo_files = list(self.unzipped_dir.glob("*.ifo"))
        for ifo_file in ifo_files:
            zip_file = self._create_single_zip(ifo_file)
            zip_files.append(zip_file)

        return zip_files

    def _create_single_zip(self, ifo_file: Path) -> Path:
        """Create a zip package for a single dictionary."""
        base_name = ifo_file.stem  # Remove .ifo extension
        zip_file = self.stardict_dir / f"{base_name}.zip"

        # Find all related files
        files_to_zip = []
        for ext in [".ifo", ".idx", ".dict"]:
            f = ifo_file.with_suffix(ext)
            if f.exists():
                files_to_zip.append(f)

        # Add res.zip if css.zip exists in txt dir
        css_zip = self.txt_dir / "css.zip"
        res_file = self.unzipped_dir / f"{base_name}.res.zip"
        if css_zip.exists():
            shutil.copy(css_zip, res_file)
            files_to_zip.append(res_file)

        if not files_to_zip:
            raise FileNotFoundError(f"No files found for {base_name}")

        logger.info(f"Creating zip package: {zip_file}")

        # Create zip file
        import zipfile
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in files_to_zip:
                arcname = file_path.name
                zf.write(file_path, arcname)
                logger.debug(f"Added {file_path} as {arcname}")

        return zip_file