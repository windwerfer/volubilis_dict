"""Dictionary processing logic for Excel to text conversion."""

import logging
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    from openpyxl import load_workbook
except ImportError:
    load_workbook = None

from .config import Config, DictionaryConfig
from .file_handler import FileHandler
from .text_formatter import TextFormatter


logger = logging.getLogger(__name__)


class DictionaryProcessor:
    """Processes Excel dictionary files into various output formats."""

    def __init__(self, config: Config):
        self.config = config.dictionary
        self.formatter = TextFormatter(self.config.patterns)
        self.file_handler = FileHandler()

    def process_excel_file(self) -> None:
        """Main method to process the Excel file."""
        if load_workbook is None:
            raise ImportError("openpyxl is required for Excel processing")

        logger.info(f"Processing Excel file: {self.config.excel_file}")

        # Ensure output directory exists
        self.file_handler.ensure_directory(self.config.output_folder)

        # Load workbook
        wb = load_workbook(self.config.excel_file, read_only=True)
        logger.info(f"Sheet names: {wb.sheetnames}")

        # Process the active sheet
        ws = wb.active
        ws.reset_dimensions()

        # Initialize data structures
        th_en_data = defaultdict(list)  # Thai to English
        th_pron_en_data = defaultdict(list)  # Thai with pronunciation to English
        th_dot_pron_en_data = defaultdict(list)  # Dot notation pronunciation to English
        en_th_data = defaultdict(lambda: defaultdict(list))  # English to Thai

        # Open output files
        output_files = self._open_output_files()

        try:
            row_count = 0
            processed_count = 0

            for row in ws.values:
                row_count += 1

                # Skip header rows
                if row_count <= 2:
                    continue

                # Process the row
                processed = self._process_row(row, th_en_data, th_pron_en_data,
                                            th_dot_pron_en_data, en_th_data)
                if processed:
                    processed_count += 1

                # Progress logging
                if row_count == 6:
                    logger.info("Processing rows...")
                if row_count % 1000 == 0:
                    logger.info(f"Processed {row_count} rows")

                # Debug limit
                if self.config.debug_test_1000_rows and row_count >= 1000:
                    logger.info("Debug mode: stopping at 1000 rows")
                    break

            logger.info(f"Total entries processed: {processed_count}")

            # Write the processed data to files
            self._write_output_files(output_files, th_en_data, th_pron_en_data,
                                   th_dot_pron_en_data, en_th_data)

        finally:
            # Close all files
            for f in output_files.values():
                f.close()

    def _open_output_files(self) -> Dict[str, any]:
        """Open all output files."""
        base_path = self.config.output_folder

        return {
            'th_en': open(base_path / "d_th-en.txt", "w", encoding='utf-8'),
            'th_pron_en': open(base_path / "d_th(pr)-en.txt", "w", encoding='utf-8'),
            'th_dot_pron_en': open(base_path / "d_th(dot+pr)-en.txt", "w", encoding='utf-8'),
            'en_th': open(base_path / "d_en-th.txt", "w", encoding='utf-8'),
        }

    def _process_row(
        self,
        row: Tuple,
        th_en_data: Dict,
        th_pron_en_data: Dict,
        th_dot_pron_en_data: Dict,
        en_th_data: Dict
    ) -> bool:
        """Process a single row from the Excel file."""
        # Validate required columns
        if len(row) < 5 or not row[4] or not row[3]:  # English and Thai required
            return False

        # Extract column values
        thai_romanized = self.formatter.clean_text(row[0] if len(row) > 0 else "")
        easythai = self.formatter.clean_text(row[1] if len(row) > 1 else "")
        thaiphon = self.formatter.clean_text(row[2] if len(row) > 2 else "")
        thai = self.formatter.clean_text(row[3])
        english = self.formatter.clean_text(row[4])

        # Additional columns
        type_word = self.formatter.clean_text(row[7] if len(row) > 7 else "")
        usage = self.formatter.clean_text(row[8] if len(row) > 8 else "")
        scient = self.formatter.clean_text(row[9] if len(row) > 9 else "")
        dom = self.formatter.clean_text(row[10] if len(row) > 10 else "")
        classif = self.formatter.clean_text(row[11] if len(row) > 11 else "")
        syn = self.formatter.clean_text(row[12] if len(row) > 12 else "")
        level = self.formatter.clean_text(row[13] if len(row) > 13 else "")
        note = self.formatter.clean_text(row[14] if len(row) > 14 else "")

        # Format pronunciation
        pron_formatted = self.formatter.format_tones(thaiphon.lower(), self.config.paiboon)
        pron_search = self.formatter.format_pronunciation_search(pron_formatted, self.config.paiboon)
        pron_formatted = self.formatter.spaces_workaround_dictbox(pron_formatted)

        # Create pronunciation entry
        pron_entry = ""
        if thaiphon:
            pron_entry = f" - {thai}"

        # Format definition
        definition = self._format_definition(
            thai, pron_formatted, type_word, usage, classif, syn, scient, note, level, english, dom
        )

        # Add sorting prefix for Thai-English
        sort_prefix = self._get_sort_prefix(level)

        # Thai to English entries
        th_en_data[thai].append(sort_prefix + definition)

        # Thai with pronunciation to English
        if pron_entry:
            th_pron_en_data[pron_entry].append(sort_prefix + definition)

        # English to Thai entries
        self._add_english_to_thai_entries(english, definition, type_word, en_th_data)

        return True

    def _format_definition(
        self,
        thai: str,
        pron_formatted: str,
        type_word: str,
        usage: str,
        classif: str,
        syn: str,
        scient: str,
        note: str,
        level: str,
        english: str,
        dom: str = ""
    ) -> str:
        """Format a complete definition string."""
        definition = f'<thai><b>{thai}</b></thai> '

        # Add pronunciation
        if pron_formatted:
            if self.config.paiboon:
                definition += f'<pron style="color:brown"> [{self.formatter.format_final_pronunciation(pron_formatted, self.config.paiboon)}] </pron>'
            else:
                definition += f'[{self.formatter.format_final_pronunciation(pron_formatted, self.config.paiboon)}]'

        # Add type and usage
        definition += f' <type style="color:green">{type_word.lower()} {usage}</type> '

        # Add classifier
        if classif:
            classifiers = self.formatter.split_and_format_classifiers(classif, self.config.paiboon)
            definition += f'<clf style="font-size:0.8em">classifier: {classifiers}</clf>'

        # Add definition
        definition += f"<br><def>{english}</def><br>"

        # Add synonyms
        if syn:
            synonyms = self.formatter.split_and_format_synonyms(syn, self.config.paiboon)
            definition += f'<syn>syn: {synonyms}</syn><br>'

        # Add scientific name
        if scient:
            definition += f'<science style="font-size:0.8em">scient: {scient}</science><br>'

        # Add note
        if note:
            definition += f'<note style="font-size:0.8em">note: {note}</note><br>'

        # Add level
        level_info = self._format_level_info(level, dom)
        if level_info:
            definition += level_info

        return definition

    def _get_sort_prefix(self, level: str) -> str:
        """Get sorting prefix based on level."""
        if len(level) > 1:
            return level[:2]
        elif len(level) == 1:
            return level + " "
        return "  "

    def _format_level_info(self, level: str, dom: str) -> str:
        """Format level and domain information."""
        parts = []
        if level:
            parts.append(f"Level: {level}")
        if level and dom:
            parts.append(" - ")
        if dom:
            parts.append(f"Category: {dom.lower()}")

        if parts:
            return f'<level style="font-size:0.7em">{"".join(parts)}</level>'
        return ""

    def _add_english_to_thai_entries(
        self,
        english: str,
        definition: str,
        type_word: str,
        en_th_data: Dict
    ) -> None:
        """Add entries to English to Thai data structure."""
        english_terms = [term.strip() for term in english.split(";") if term.strip()]

        for term in english_terms:
            if type_word not in en_th_data[term]:
                en_th_data[term][type_word] = []
            en_th_data[term][type_word].append(definition)

    def _write_output_files(
        self,
        files: Dict,
        th_en_data: Dict,
        th_pron_en_data: Dict,
        th_dot_pron_en_data: Dict,
        en_th_data: Dict
    ) -> None:
        """Write all processed data to output files."""
        # Thai to English
        for thai_word, definitions in th_en_data.items():
            definitions.sort()
            for definition in definitions:
                files['th_en'].write(f"{thai_word}\t{definition[2:]}\n")

        # Thai pronunciation to English
        for pron_word, definitions in th_pron_en_data.items():
            definitions.sort()
            for definition in definitions:
                files['th_pron_en'].write(f"{pron_word}\t{definition[2:]}\n")
                files['th_dot_pron_en'].write(f".{pron_word}\t{definition[2:]}\n")

        # English to Thai
        for english_word, type_groups in en_th_data.items():
            word_entry = f'<b>{english_word}</b><br> '

            # Sort types
            sorted_types = sorted(type_groups.items())

            type_entries = []
            for word_type, definitions in sorted_types:
                definitions.sort()
                def_text = "<br>".join(definitions[2:] for definitions in definitions)
                type_entries.append(f'<type style="color:green">{word_type}</type><br>{def_text}')

            word_entry += "<br>".join(type_entries)
            files['en_th'].write(f"{english_word}\t{word_entry}\n")