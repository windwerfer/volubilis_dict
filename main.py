#!/usr/bin/env python
"""Thin wrapper for running the Volubilis dictionary processor.

This allows convenient development usage with:
    python main.py data/vol_mundo_....xlsx --debug-1000

It adds the src directory to the path so the package can be imported
without requiring `pip install -e .` first.

For installed usage, the console script `volubilis-dict` (defined in pyproject.toml)
or `python -m volubilis_dict.cli` can be used.
"""

import sys
from pathlib import Path

# Make `volubilis_dict` importable during development (src layout)
sys.path.insert(0, str(Path(__file__).parent / "src"))

from volubilis_dict.cli import create_parser, main


if __name__ == "__main__":
    sys.exit(main())
