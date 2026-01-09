"""MDX format conversion and processing utilities."""

import logging
import re
import subprocess
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class MdictBuilder:
    """Handles conversion to MDX format for Mdict."""

    def __init__(
        self, txt_dir: Path, mdict_dir: Path, css_prefix: Optional[str] = None
    ):
        self.txt_dir = txt_dir
        self.mdict_dir = mdict_dir
        self.mdict_txt_dir = mdict_dir / "txt"
        self.css_prefix = (
            css_prefix  # String to prepend to each definition (e.g., CSS styles)
        )

    def convert_to_mdx(self) -> None:
        """Convert all txt files to MDX format via mdict-utils."""
        self.mdict_txt_dir.mkdir(parents=True, exist_ok=True)

        # Copy res.zip to mdict/txt for resources
        res_zip = Path("res.zip")
        if res_zip.exists():
            import shutil

            shutil.copy(res_zip, self.mdict_txt_dir / "res.zip")

        txt_files = list(self.txt_dir.glob("volubilis_*.txt"))
        if not txt_files:
            raise FileNotFoundError(f"No txt files found in {self.txt_dir}")

        for txt_file in txt_files:
            self._convert_single_file(txt_file)

    def _convert_single_file(self, txt_file: Path) -> None:
        """Convert a single txt file to MDX format."""
        # Process to MDX txt format first
        mdx_txt_file = self._process_to_mdx_txt(txt_file)

        # Then convert to MDX using mdict-utils (assuming mdict command)
        output_name = txt_file.stem
        output_file = self.mdict_dir / f"{output_name}.mdx"

        logger.info(f"Converting {mdx_txt_file} to {output_file} with mdict-utils")

        try:
            # Use mdict-utils command: mdict -a input output
            result = subprocess.run(
                ["mdict", "-a", str(mdx_txt_file), str(output_file)],
                capture_output=True,
                text=True,
                check=True,
            )

            logger.debug(f"mdict output: {result.stdout}")

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to convert {txt_file} to MDX: {e}")
            logger.error(f"stderr: {e.stderr}")
            raise

    def _process_to_mdx_txt(self, txt_file: Path) -> Path:
        """Process txt file to MDX import format, handling synonyms and optional prefix."""
        mdx_txt_file = self.mdict_txt_dir / f"{txt_file.stem}.txt"

        with open(txt_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Process in chunks like the sample code
        processed_content = self._process_content_to_mdx(content)

        with open(mdx_txt_file, "w", encoding="utf-8") as f:
            f.write(processed_content)

        return mdx_txt_file

    def _process_content_to_mdx(self, content: str) -> str:
        """Process the entire content to MDX format."""
        lines = content.splitlines()
        processed_lines = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            tmp = line.split("\t")
            # Ignore invalid entries
            if len(tmp) != 2 or not tmp[0] or not tmp[1]:
                continue

            # Handle synonyms
            syn = [s.strip() for s in tmp[0].split("|") if s.strip()]
            if not syn:
                continue  # Skip if no valid headwords
            tmp[0] = syn[0]
            # Add @@@LINK entries for additional synonyms
            for synonym in syn[1:]:
                if synonym:  # Ensure synonym is not empty
                    synonym = synonym.replace("\n", " ")  # Remove any \n in synonym
                    processed_lines.append(f"{synonym}\n@@@LINK={tmp[0]}\n</>\n")

            # Remove escaped newlines and add optional prefix (e.g., CSS)
            tmp[1] = re.sub(r"\\n", "", tmp[1])
            if self.css_prefix:
                tmp[1] = self.css_prefix + tmp[1]

            # Ensure headword has no \n and is not empty
            headword = tmp[0].replace("\n", " ").strip()
            if not headword:
                continue

            # Ensure definition ends cleanly, then add newline before </>
            definition = tmp[1].rstrip("\n")
            # Format as headword\n definition\n</>\n
            processed_lines.append(f"{headword}\n{definition}\n</>\n")

        return "".join(processed_lines)
