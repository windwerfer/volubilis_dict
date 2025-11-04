"""Configuration management for the Volubilis dictionary processor."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional




@dataclass
class RegexPatterns:
    """Regex patterns for text processing."""

    remove_brackets: Dict[str, str] = field(default_factory=lambda: {
        r"[…\.\[\]\(\)]": "",
        r"[\u0300\u0301\u0302\u030c]": "",
    })

    remove_starting_brackets: Dict[str, str] = field(default_factory=lambda: {
        r"\[": "(",
        r"\]": ")",
        r"^\((.*)\)$": r"\1",
        r"([-_\\/¯]) ([a-zɔ])": r"\1\2",
    })

    type_friendly_1: Dict[str, str] = field(default_factory=lambda: {
        r"ø̅": "øø",
        r"ɔ̅": "ɔɔ",
        r"ē": "ee",
        r"ā": "aa",
        r"ī": "ii",
        r"ū": "uu",
        r"ō": "oo",
    })

    to_paiboon: Dict[str, str] = field(default_factory=lambda: {
        r"¯([bcdfghjklmnpqrstvwxyz]*)([aeiouɔ])([a-z]*)": r"-\1\2" + "\u0301" + r"\3",
        r"\\([bcdfghjklmnpqrstvwxyz]*)([aeiouɔ])([a-z]*)": r"-\1\2" + "\u0302" + r"\3",
        r"/([bcdfghjklmnpqrstvwxyz]*)([aeiouɔ])([a-z]*)": r"-\1\2" + "\u030c" + r"\3",
        r"_([bcdfghjklmnpqrstvwxyz]*)([aeiouɔ])([a-z]*)": r"-\1\2" + "\u0300" + r"\3",
        r"^-": "",
        r"([\(\[])-": r"\1",
    })

    spaces_workaround_dictbox: Dict[str, str] = field(default_factory=lambda: {
        r"[ ]-": r"<sp> </sp>",
    })

    type_friendly_2: Dict[str, str] = field(default_factory=lambda: {
        r"[-_\\/¯]": " ",
        r"^\s+": "",
        r"\s\s+": " ",
        r"([tkp])h": r"\1",
        r"ñ": "n",
        r"ɔ": "o",
    })

    pron: Dict[str, str] = field(default_factory=lambda: {
        r"ø": "ø̅",
        r"ǿ": "ø",
        r"ø̅": "ɔ̅",
    })

    pron2: Dict[str, str] = field(default_factory=lambda: {
        r"ø": "ɔ",
    })

    default: Dict[str, str] = field(default_factory=lambda: {
        r"\t": "    ",
        r"^\s+": "",
        r"\s+$": "",
    })

    final_pron: Dict[str, str] = field(default_factory=lambda: {
        r"\\": r"&#x5c;",
    })

    classifier: Dict[str, str] = field(default_factory=lambda: {
        r"\s*(.*?)\s*\(([ก-๛]+).*\s*": r"\2",
    })


@dataclass
class DictionaryConfig:
    """Configuration for dictionary processing."""

    # File paths
    excel_file: Path = Path("src/vol_mundo_01.06.2023.xlsx")
    output_folder: Path = Path("vol_mundo")

    # Processing options
    columns: int = 32
    paiboon: bool = True
    debug: bool = False
    debug_test_1000_rows: bool = False

    # Caching options
    use_cache: bool = True
    cache_file: Path = Path("cache.pkl")
    force_refresh_cache: bool = False

    # Dictionary metadata
    title_en_th: str = "volubilis v074 (en-th)"
    title_th_en: str = "volubilis v074 (th-en)"
    title_th_pron_en: str = "volubilis v074 (.th-en)"
    description: str = (
        'description=Volubilis English-Thai dictionary by Belisan (Fr. Bastien)<br>'
        'พจนานุกรม วอลุบิลิส ภาษาอังกฤษ-ไทย<br>'
        'v. 21.3 (1.11.2022) - 103 000  entr.<br>'
        '(http://belisan-volubilis.blogspot.com)<br><br>'
        'ā = long vowel "a"<br>'
        'start pronounciation search: type . (dot) plus searchterm (eg. .maa -> dog, horse,come,..)'
    )

    # Regex patterns
    patterns: RegexPatterns = field(default_factory=RegexPatterns)

    # Column indices (0-based)
    COLUMN_MAPPING: Dict[str, int] = field(default_factory=lambda: {
        'thai_romanized': 0,
        'easythai': 1,
        'thaiphon': 2,
        'thai': 3,
        'thai_pron_added': 4,
        'english': 5,
        'french': 6,
        'type': 7,
        'usage': 8,
        'scient': 9,
        'dom': 10,
        'classif': 11,
        'syn': 12,
        'level': 13,
        'note': 14,
        'spanish': 15,
        'italian': 16,
        'portuguese': 17,
        'german': 18,
        'dutch': 19,
        'norwegian': 20,
        'turkish': 21,
        'malay': 22,
        'indonesian': 23,
        'filipino': 24,
        'vietnamese': 25,
        'russian1': 26,
        'russian2': 27,
        'lao1': 28,
        'lao2': 29,
        'korean1': 30,
        'korean2': 31,
    })


@dataclass
class Config:
    """Main configuration class."""

    dictionary: DictionaryConfig = field(default_factory=DictionaryConfig)

    @classmethod
    def from_file(cls, config_path: Optional[Path] = None) -> 'Config':
        """Load configuration from file (future enhancement)."""
        # For now, return default config
        # TODO: Implement TOML/YAML loading
        return cls()

    def validate(self) -> None:
        """Validate configuration values."""
        if not self.dictionary.excel_file.exists():
            raise ValueError(f"Excel file not found: {self.dictionary.excel_file}")

        if self.dictionary.columns < 1:
            raise ValueError("Columns must be positive")

        # Validate column mapping doesn't exceed columns
        max_col = max(self.dictionary.COLUMN_MAPPING.values())
        if max_col >= self.dictionary.columns:
            raise ValueError(f"Column mapping references column {max_col} but only {self.dictionary.columns} columns configured")