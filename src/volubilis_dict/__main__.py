"""Allow running the package as a module: python -m volubilis_dict

This re-exports the CLI main for `python -m volubilis_dict`.
"""

from .cli import main

if __name__ == "__main__":
    import sys
    sys.exit(main())
