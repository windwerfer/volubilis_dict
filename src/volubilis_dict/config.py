"""Configuration management for the Volubilis dictionary processor."""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

try:
    from dotenv import load_dotenv

    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False


@dataclass
class RegexPatterns:
    """Regex patterns for text processing."""

    remove_brackets: Dict[str, str] = field(
        default_factory=lambda: {
            r"[…\.\[\]\(\)]": "",
            r"[\u0300\u0301\u0302\u030c]": "",
        }
    )

    remove_starting_brackets: Dict[str, str] = field(
        default_factory=lambda: {
            r"\[": "(",
            r"\]": ")",
            r"^\((.*)\)$": r"\1",
            r"([-_\\/¯]) ([a-zɔ])": r"\1\2",
        }
    )

    type_friendly_1: Dict[str, str] = field(
        default_factory=lambda: {
            r"ø̅": "øø",
            r"ɔ̅": "ɔɔ",
            r"ē": "ee",
            r"ā": "aa",
            r"ī": "ii",
            r"ū": "uu",
            r"ō": "oo",
        }
    )

    to_paiboon: Dict[str, str] = field(
        default_factory=lambda: {
            r"¯([bcdfghjklmnpqrstvwxyz]*)([aeiouɔ])([a-z]*)": r"-\1\2"
            + "\u0301"
            + r"\3",
            r"\\([bcdfghjklmnpqrstvwxyz]*)([aeiouɔ])([a-z]*)": r"-\1\2"
            + "\u0302"
            + r"\3",
            r"/([bcdfghjklmnpqrstvwxyz]*)([aeiouɔ])([a-z]*)": r"-\1\2"
            + "\u030c"
            + r"\3",
            r"_([bcdfghjklmnpqrstvwxyz]*)([aeiouɔ])([a-z]*)": r"-\1\2"
            + "\u0300"
            + r"\3",
            r"^-": "",
            r"([\(\[])-": r"\1",
        }
    )

    spaces_workaround_dictbox: Dict[str, str] = field(
        default_factory=lambda: {
            r"[ ]-": r"<sp> </sp>",
        }
    )

    type_friendly_2: Dict[str, str] = field(
        default_factory=lambda: {
            r"[-_\\/¯]": " ",
            r"^\s+": "",
            r"\s\s+": " ",
            r"([tkp])h": r"\1",
            r"ñ": "n",
            r"ɔ": "o",
        }
    )

    pron: Dict[str, str] = field(
        default_factory=lambda: {
            r"ø": "ø̅",
            r"ǿ": "ø",
            r"ø̅": "ɔ̅",
        }
    )

    pron2: Dict[str, str] = field(
        default_factory=lambda: {
            r"ø": "ɔ",
        }
    )

    default: Dict[str, str] = field(
        default_factory=lambda: {
            r"\t": "    ",
            r"^\s+": "",
            r"\s+$": "",
        }
    )

    final_pron: Dict[str, str] = field(
        default_factory=lambda: {
            r"\\": r"&#x5c;",
        }
    )

    classifier: Dict[str, str] = field(
        default_factory=lambda: {
            r"\s*(.*?)\s*\(([ก-๛]+).*\s*": r"\2",
        }
    )


# Single source of truth for Excel column semantics.
# Small list: (0-based index, semantic_key for code/_get_col, log_label or None to use key).
# Both the log output and the imported column variables are generated from this list.
# "type_word" key for column 6 so that extraction uses type_word = _get_col("type_word")
# without needing to rename variables elsewhere in the code.
COLUMN_DEFS: list[tuple[int, str, str | None]] = [
    (0, "thai_romanized", None),
    (1, "easythai", None),
    (2, "thaiphon", "thaiphon (pronunciation)"),
    (3, "thai", "thai (word)"),
    (4, "english", "english (definition)"),
    (5, "french", None),
    (6, "type_word", "type_word"),
    (7, "usage", "usage"),
    (8, "scient", None),
    (9, "dom", None),
    (10, "classif", None),
    (11, "syn", None),
    (12, "level", None),
    (13, "note", None),
    # (14, "spanish", None),
    # (15, "italian", None),
    # (16, "portuguese", None),
    # (17, "german", None),
    # (18, "dutch", None),
    # (19, "norwegian", None),
    # (20, "turkish", None),
    # (21, "malay", None),
    # (22, "indonesian", None),
    # (23, "filipino", None),
    # (24, "vietnamese", None),
    # (25, "russian1", None),
    # (26, "russian2", None),
    # (27, "lao1", None),
    # (28, "lao2", None),
    # (29, "korean1", None),
    # (30, "korean2", None),
    # higher columns in the source file (e.g. ZHO) will log as "unused"
]


def get_column_log_label(index: int) -> str:
    """Return the log label for a column index from the single source COLUMN_DEFS."""
    for idx, key, label in COLUMN_DEFS:
        if idx == index:
            return label or key
    return "unused"


@dataclass
class DictionaryConfig:
    """Configuration for dictionary processing."""

    # File paths
    excel_file: Path = Path("data/vol_mundo_01.11.2025.xlsx")
    output_folder: Path = Path("vol_mundo")

    # Processing options
    columns: int = 32
    paiboon: bool = True
    debug: bool = False
    debug_test_1000_rows: bool = True

    # Pronunciation file options
    th_pron: bool = True
    th_pron_prefix: str = "."
    th_pron_incl_translation_in_headword: bool = True
    th_pron_merge: bool = True
    th_pron_merge_prefix: str = ","
    th_pron_merge_incl_translation_in_headword: bool = False
    th_pron_max_headword_length: int = 50
    th_pron_merge_max_headword_length: int = 50

    # MOBI build options (requires calibre to be installed)
    enable_mobi_build: bool = False
    create_mobi: bool = False

    # Caching options
    use_cache: bool = True
    cache_file: Path = Path("cache.pkl")
    force_refresh_cache: bool = False

    # CSS options
    inline_css: bool = False

    # removed dark theme css style, dict readers convert it by themselfs
    # dictango can not handle custom dark theme, it reconverts it to light -> black text on black bg
    css_content: str = """

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

"""

    # MOBI style mapping for inline styles
    style_mapping: Dict[str, str] = field(
        default_factory=lambda: {
            'class="thai"': 'style="font-weight: bold; color: #000080;"',
            'class="pron"': 'style="color: #008000; font-style: italic;"',
            'class="def"': 'style=""',
            'class="syn"': 'style="font-style: italic; color: #800080;"',
            'class="note"': 'style="color: #808080; font-size: smaller;"',
            'class="level"': 'style="font-size: smaller;"',
            'class="english"': 'style="font-weight: bold; color: #800000;"',
            'class="type"': 'style="font-style: italic; color: #000080;"',
            'class="clf"': 'style="font-style: italic;"',
        }
    )

    # Compression options
    no_dz: bool = False

    # Dictionary metadata
    title_en_th: str = "volubilis v2 (en-th)"
    title_th_en: str = "volubilis v2 (th-en)"
    title_th_pron_en: str = "volubilis v2 (.th-en)"
    title_th_pron_merge_en: str = "volubilis v2 (,th-en)"
    description: str = (
        "description=Volubilis English-Thai dictionary by Belisan (Fr. Bastien)<br>"
        "พจนานุกรม วอลุบิลิส ภาษาอังกฤษ-ไทย<br>"
        "v. 21.3 (1.11.2025) - 103 000  entr.<br>"
        "(http://belisan-volubilis.blogspot.com)<br><br>"
        'ā = long vowel "a"<br>'
        "start pronounciation search: type . (dot) plus searchterm (eg. .maa -> dog, horse,come,..)"
    )

    # Regex patterns
    patterns: RegexPatterns = field(default_factory=RegexPatterns)

    # COLUMN_MAPPING is derived from the single source COLUMN_DEFS (see top of file).
    # Do not edit the mapping directly; update COLUMN_DEFS instead.
    COLUMN_MAPPING: Dict[str, int] = field(
        default_factory=lambda: {key: idx for idx, key, _ in COLUMN_DEFS}
    )


@dataclass
class Config:
    """Main configuration class."""

    dictionary: DictionaryConfig = field(default_factory=DictionaryConfig)

    @classmethod
    def from_file(cls, config_path: Optional[Path] = None) -> "Config":
        """Load configuration from environment variables or file."""
        config = cls()

        # Load .env file if available
        if DOTENV_AVAILABLE:
            load_dotenv(config_path or Path(".env"))

        # Load from environment variables
        config.dictionary.excel_file = Path(
            os.getenv("VOLUBILIS_EXCEL_FILE", str(config.dictionary.excel_file))
        )
        config.dictionary.output_folder = Path(
            os.getenv("VOLUBILIS_OUTPUT_FOLDER", str(config.dictionary.output_folder))
        )
        config.dictionary.columns = int(
            os.getenv("VOLUBILIS_COLUMNS", config.dictionary.columns)
        )
        config.dictionary.paiboon = (
            os.getenv("VOLUBILIS_PAIBOON", str(config.dictionary.paiboon)).lower()
            == "true"
        )
        config.dictionary.debug = (
            os.getenv("VOLUBILIS_DEBUG", str(config.dictionary.debug)).lower() == "true"
        )
        config.dictionary.debug_test_1000_rows = (
            os.getenv(
                "VOLUBILIS_DEBUG_TEST_1000_ROWS",
                str(config.dictionary.debug_test_1000_rows),
            ).lower()
            == "true"
        )

        # Pronunciation options
        config.dictionary.th_pron = (
            os.getenv("VOLUBILIS_TH_PRON", str(config.dictionary.th_pron)).lower()
            == "true"
        )
        config.dictionary.th_pron_prefix = os.getenv(
            "VOLUBILIS_TH_PRON_PREFIX", config.dictionary.th_pron_prefix
        )
        config.dictionary.th_pron_incl_translation_in_headword = (
            os.getenv(
                "VOLUBILIS_TH_PRON_INCL_TRANSLATION",
                str(config.dictionary.th_pron_incl_translation_in_headword),
            ).lower()
            == "true"
        )
        config.dictionary.th_pron_merge = (
            os.getenv(
                "VOLUBILIS_TH_PRON_MERGE", str(config.dictionary.th_pron_merge)
            ).lower()
            == "true"
        )
        config.dictionary.th_pron_merge_prefix = os.getenv(
            "VOLUBILIS_TH_PRON_MERGE_PREFIX", config.dictionary.th_pron_merge_prefix
        )
        config.dictionary.th_pron_merge_incl_translation_in_headword = (
            os.getenv(
                "VOLUBILIS_TH_PRON_MERGE_INCL_TRANSLATION",
                str(config.dictionary.th_pron_merge_incl_translation_in_headword),
            ).lower()
            == "true"
        )
        config.dictionary.th_pron_max_headword_length = int(
            os.getenv(
                "VOLUBILIS_TH_PRON_MAX_LENGTH",
                config.dictionary.th_pron_max_headword_length,
            )
        )
        config.dictionary.th_pron_merge_max_headword_length = int(
            os.getenv(
                "VOLUBILIS_TH_PRON_MERGE_MAX_LENGTH",
                config.dictionary.th_pron_merge_max_headword_length,
            )
        )

        # MOBI options
        config.dictionary.enable_mobi_build = (
            os.getenv(
                "VOLUBILIS_ENABLE_MOBI_BUILD", str(config.dictionary.enable_mobi_build)
            ).lower()
            == "true"
        )

        # Caching options
        config.dictionary.use_cache = (
            os.getenv("VOLUBILIS_USE_CACHE", str(config.dictionary.use_cache)).lower()
            == "true"
        )
        config.dictionary.cache_file = Path(
            os.getenv("VOLUBILIS_CACHE_FILE", str(config.dictionary.cache_file))
        )
        config.dictionary.force_refresh_cache = (
            os.getenv(
                "VOLUBILIS_FORCE_REFRESH_CACHE",
                str(config.dictionary.force_refresh_cache),
            ).lower()
            == "true"
        )

        # Metadata
        config.dictionary.title_en_th = os.getenv(
            "VOLUBILIS_TITLE_EN_TH", config.dictionary.title_en_th
        )
        config.dictionary.title_th_en = os.getenv(
            "VOLUBILIS_TITLE_TH_EN", config.dictionary.title_th_en
        )
        config.dictionary.title_th_pron_en = os.getenv(
            "VOLUBILIS_TITLE_TH_PRON_EN", config.dictionary.title_th_pron_en
        )
        config.dictionary.title_th_pron_merge_en = os.getenv(
            "VOLUBILIS_TITLE_TH_PRON_MERGE_EN", config.dictionary.title_th_pron_merge_en
        )
        config.dictionary.description = os.getenv(
            "VOLUBILIS_DESCRIPTION", config.dictionary.description
        )

        return config

    def validate(self) -> None:
        """Validate configuration values."""
        if not self.dictionary.excel_file.exists():
            raise ValueError(f"Excel file not found: {self.dictionary.excel_file}")

        if self.dictionary.columns < 1:
            raise ValueError("Columns must be positive")

        # Validate column mapping doesn't exceed columns
        max_col = max(self.dictionary.COLUMN_MAPPING.values())
        if max_col >= self.dictionary.columns:
            raise ValueError(
                f"Column mapping references column {max_col} but only {self.dictionary.columns} columns configured"
            )
