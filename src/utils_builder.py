"""Shared utilities for dictionary building."""

import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class UtilsBuilder:
    """Handles shared setup tasks like directories and static files."""

    @staticmethod
    def setup_resources(
        stardict_dir: Path, mdict_dir: Path, config, mobi_dir: Optional[Path] = None, yomitan_dir: Optional[Path] = None
    ) -> None:
        """Setup common directories and static files like CSS."""
        # Create directories
        stardict_dir.mkdir(exist_ok=True)
        (stardict_dir / "txt").mkdir(exist_ok=True)
        (stardict_dir / "unzipped").mkdir(exist_ok=True)
        mdict_dir.mkdir(exist_ok=True)
        (mdict_dir / "txt").mkdir(exist_ok=True)
        if yomitan_dir:
            yomitan_dir.mkdir(exist_ok=True)
            (yomitan_dir / "txt").mkdir(exist_ok=True)
        if config.dictionary.create_mobi and mobi_dir:
            mobi_dir.mkdir(exist_ok=True)
            (mobi_dir / "txt").mkdir(exist_ok=True)

        # Write CSS to locations
        css_content = config.dictionary.css_content
        css_files = [
            stardict_dir / "txt" / "styles.css",
            mdict_dir / "txt" / "styles.css",
        ]
        if yomitan_dir:
            css_files.append(yomitan_dir / "txt" / "styles.css")

        for css_file in css_files:
            css_file.parent.mkdir(parents=True, exist_ok=True)
            css_file.write_text(css_content, encoding="utf-8")

        logger.info(f"CSS written to {', '.join(str(f) for f in css_files)}")
