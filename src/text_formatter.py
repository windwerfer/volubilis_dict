"""Text formatting utilities for dictionary processing."""

import re
from typing import Dict, List, Tuple

from .config import RegexPatterns


class TextFormatter:
    """Handles text formatting and regex transformations for dictionary entries."""

    def __init__(self, patterns: RegexPatterns):
        self.patterns = patterns

    def replace_multi(self, text: str, replacements: Dict[str, str], debug: bool = False) -> str:
        """Apply multiple regex replacements to text."""
        result = text
        for pattern, replacement in replacements.items():
            if pattern:  # Skip empty patterns
                result = re.sub(pattern, replacement, result)
                if debug:
                    print(f"{pattern} -> {text} {result}")
        return result

    def format_tones(self, text: str, paiboon: bool = False) -> str:
        """Format tone marks in pronunciation text."""
        text = self.replace_multi(text, self.patterns.default)
        text = self.replace_multi(text, self.patterns.remove_starting_brackets)
        text = self.replace_multi(text, self.patterns.pron)
        text = self.replace_multi(text, self.patterns.pron2)
        if paiboon:
            text = self.replace_multi(text, self.patterns.type_friendly_1)
            text = self.replace_multi(text, self.patterns.to_paiboon)
        return text

    def format_definition(self, text: str) -> str:
        """Format definition text."""
        return self.replace_multi(text, self.patterns.default)

    def format_final_pronunciation(self, text: str, paiboon: bool = False) -> str:
        """Format final pronunciation text."""
        if not paiboon:
            text = self.replace_multi(text, self.patterns.final_pron)
        return text

    def format_classifier(self, text: str, paiboon: bool = False) -> str:
        """Format classifier text."""
        text = self.replace_multi(text, self.patterns.classifier)
        text = self.replace_multi(text, self.patterns.default)
        text = self.replace_multi(text, self.patterns.remove_starting_brackets)
        text = self.replace_multi(text, self.patterns.pron)
        text = self.replace_multi(text, self.patterns.pron2)
        if paiboon:
            text = self.replace_multi(text, self.patterns.type_friendly_1)
            text = self.replace_multi(text, self.patterns.to_paiboon)
        return text

    def spaces_workaround_dictbox(self, text: str) -> str:
        """Apply Dictbox spaces workaround."""
        return self.replace_multi(text, self.patterns.spaces_workaround_dictbox)

    def format_pronunciation_search(self, text: str, paiboon: bool = False) -> str:
        """Format text for pronunciation search."""
        text = self.replace_multi(text, self.patterns.remove_brackets)
        if not paiboon:
            text = self.replace_multi(text, self.patterns.type_friendly_1)
        text = self.replace_multi(text, self.patterns.type_friendly_2)
        return text

    def clean_text(self, text: str) -> str:
        """General text cleaning."""
        if not text or text == "None":
            return ""
        return str(text).strip()

    def split_and_format_classifiers(self, classifiers: str, paiboon: bool = False) -> str:
        """Split classifier string by semicolon and format each part."""
        if not classifiers:
            return ""

        parts = [self.clean_text(part) for part in classifiers.split(";")]
        formatted_parts = [self.format_classifier(part, paiboon) for part in parts if part]
        return ", ".join(formatted_parts)

    def split_and_format_synonyms(self, synonyms: str, paiboon: bool = False) -> str:
        """Split synonym string by semicolon and format each part."""
        return self.split_and_format_classifiers(synonyms, paiboon)

    def get_tone_priority(self, thai: str) -> int:
        """Get tone priority for sorting: 0 mid, 1 low, 2 falling, 3 high, 4 rising."""
        if '\u0e48' in thai:  # ่ low
            return 1
        elif '\u0e49' in thai:  # ้ falling
            return 2
        elif '\u0e4a' in thai:  # ๊ high
            return 3
        elif '\u0e4b' in thai:  # ๋ rising
            return 4
        else:
            return 0  # mid

    def sort_thai_words_by_tone_and_level(self, items: List[Tuple[str, str, str, str]], get_sort_prefix) -> List[Tuple[str, str, str, str]]:
        """Sort list of (thai_word, eng, level) by tone priority then level prefix."""
        return sorted(items, key=lambda x: (self.get_tone_priority(x[0]), get_sort_prefix(x[2])))