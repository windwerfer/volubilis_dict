"""File handling utilities for dictionary processing."""

import io
from pathlib import Path
from typing import Dict, List, Optional, TextIO


class FileHandler:
    """Handles file I/O operations with proper context management."""

    @staticmethod
    def ensure_directory(path: Path) -> None:
        """Ensure directory exists, create if necessary."""
        path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def read_file_lines(file_path: Path, limit: Optional[int] = None) -> List[str]:
        """Read lines from a file with optional limit."""
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if limit is not None:
                lines = lines[:limit]
            return lines

    @staticmethod
    def write_lines_to_file(file_path: Path, lines: List[str], mode: str = 'w') -> None:
        """Write lines to a file."""
        with open(file_path, mode, encoding='utf-8') as f:
            for line in lines:
                f.write(line)

    @staticmethod
    def append_lines_to_file(file_path: Path, lines: List[str]) -> None:
        """Append lines to a file."""
        FileHandler.write_lines_to_file(file_path, lines, mode='a')

    @staticmethod
    def prepend_lines_to_file(file_path: Path, lines: List[str]) -> None:
        """Prepend lines to a file."""
        # Read existing content
        existing_content = ""
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                existing_content = f.read()

        # Write new content + existing content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines) + '\n')
            f.write(existing_content)

    @staticmethod
    def create_tab_separated_file(
        file_path: Path,
        data: Dict[str, List[str]],
        sort_keys: bool = True
    ) -> None:
        """Create a tab-separated file from dictionary data."""
        keys = sorted(data.keys()) if sort_keys else list(data.keys())

        with open(file_path, 'w', encoding='utf-8') as f:
            for key in keys:
                values = data[key]
                if isinstance(values, list):
                    for value in values:
                        f.write(f"{key}\t{value}\n")
                else:
                    f.write(f"{key}\t{values}\n")

    @staticmethod
    def create_mdx_file(
        input_file: Path,
        output_file: Path,
        title: str,
        description: str
    ) -> None:
        """Create MDX file from tab-separated input using pyglossary."""
        # This would integrate with pyglossary
        # For now, just copy the logic from the original
        pass

    @staticmethod
    def batch_write_to_files(
        file_handles: Dict[str, TextIO],
        data: Dict[str, List[str]]
    ) -> None:
        """Write data to multiple open file handles."""
        for filename, handle in file_handles.items():
            if filename in data:
                lines = data[filename]
                for line in lines:
                    handle.write(line)

    @staticmethod
    def flush_files(file_handles: List[TextIO]) -> None:
        """Flush multiple file handles."""
        for handle in file_handles:
            handle.flush()