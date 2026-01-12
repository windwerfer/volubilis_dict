"""Shared utilities for dictionary building."""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class UtilsBuilder:
    """Handles shared setup tasks like directories and static files."""

    @staticmethod
    def setup_resources(stardict_dir: Path, mdict_dir: Path, config) -> None:
        """Setup common directories and static files like CSS."""
        # Create directories
        stardict_dir.mkdir(exist_ok=True)
        (stardict_dir / "txt").mkdir(exist_ok=True)
        (stardict_dir / "unzipped").mkdir(exist_ok=True)
        mdict_dir.mkdir(exist_ok=True)
        (mdict_dir / "txt").mkdir(exist_ok=True)

        # Write CSS to both locations
        css_content = config.dictionary.css_content
        css_file_stardict = stardict_dir / "txt" / "styles.css"
        css_file_mdict_txt = mdict_dir / "txt" / "styles.css"

        css_file_stardict.write_text(css_content, encoding="utf-8")
        css_file_mdict_txt.parent.mkdir(
            parents=True, exist_ok=True
        )  # Ensure txt dir exists
        css_file_mdict_txt.write_text(css_content, encoding="utf-8")

        logger.info(f"CSS written to {css_file_stardict} and {css_file_mdict_txt}")
