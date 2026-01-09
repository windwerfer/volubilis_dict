"""Shared utilities for dictionary building."""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class UtilsBuilder:
    """Handles shared setup tasks like directories and static files."""

    @staticmethod
    def setup_resources(stardict_dir: Path, mdict_dir: Path) -> None:
        """Setup common directories and static files like CSS."""
        # Create directories
        stardict_dir.mkdir(exist_ok=True)
        mdict_dir.mkdir(exist_ok=True)

        # Write CSS to both locations
        css_content = """\
/* Light theme */
.thai { font-weight: bold; color: #000080; }
.pron { color: #008000; font-style: italic; }
.def { }
.syn { font-style: italic; color: #800080; }
.description { }
.note { color: #808080; font-size: smaller; }
.level { font-size: smaller; }
.english { font-weight: bold; color: #800000; }
.type { font-style: italic; color: #000080; }
.clf { font-style: italic; }

/* Dark theme */
@media (prefers-color-scheme: dark) {
    body { background-color: #121212; color: #ffffff; }
    .thai { color: #87ceeb; }
    .pron { color: #90ee90; }
    .syn { color: #dda0dd; }
    .description { }
    .science { font-size: smaller; }
    .note { color: #d3d3d3; }
    .level { font-size: smaller; }
    .english { color: #ff6347; }
    .type { color: #87ceeb; }
}
"""
        css_file_stardict = stardict_dir / "styles.css"
        css_file_mdict_txt = mdict_dir / "txt" / "styles.css"

        css_file_stardict.write_text(css_content, encoding='utf-8')
        css_file_mdict_txt.parent.mkdir(parents=True, exist_ok=True)  # Ensure txt dir exists
        css_file_mdict_txt.write_text(css_content, encoding='utf-8')

        logger.info(f"CSS written to {css_file_stardict} and {css_file_mdict_txt}")