"""Main CLI interface for the Volubilis dictionary processor."""

import argparse
import logging
import sys
from pathlib import Path

from .config import Config
from .dictionary_processor import DictionaryProcessor


def setup_logging(verbose: bool = False) -> None:
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        description="Process Volubilis Thai-English dictionary Excel files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.main                    # Process with default settings
  python -m src.main --excel-file custom.xlsx --output-dir output/
  python -m src.main --verbose          # Enable debug logging
  python -m src.main --debug-1000       # Process only first 1000 rows for testing
  python -m src.main --no-cache         # Disable caching
  python -m src.main --refresh-cache    # Force cache refresh
        """
    )

    parser.add_argument(
        '--excel-file', '-f',
        type=Path,
        default=Path("src/vol_mundo_01.06.2023.xlsx"),
        help='Path to the Excel file to process'
    )

    parser.add_argument(
        '--output-dir', '-o',
        type=Path,
        default=Path("vol_mundo"),
        help='Output directory for processed files'
    )

    parser.add_argument(
        '--columns',
        type=int,
        default=32,
        help='Number of columns to process'
    )

    parser.add_argument(
        '--no-paiboon',
        action='store_true',
        help='Disable Paiboon transcription system'
    )

    parser.add_argument(
        '--debug-1000',
        action='store_true',
        help='Process only first 1000 rows for debugging'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )

    parser.add_argument(
        '--config',
        type=Path,
        help='Path to configuration file (future feature)'
    )

    parser.add_argument(
        '--no-cache',
        action='store_true',
        help='Disable caching of processed data'
    )

    parser.add_argument(
        '--refresh-cache',
        action='store_true',
        help='Force refresh of cache even if valid'
    )

    return parser


def main() -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    # Setup logging
    setup_logging(args.verbose)

    try:
        # Load configuration
        config = Config()

        # Override config with command line arguments
        config.dictionary.excel_file = args.excel_file
        config.dictionary.output_folder = args.output_dir
        config.dictionary.columns = args.columns
        config.dictionary.paiboon = not args.no_paiboon
        config.dictionary.debug_test_1000_rows = args.debug_1000
        config.dictionary.use_cache = not args.no_cache
        config.dictionary.force_refresh_cache = args.refresh_cache

        # Validate configuration
        config.validate()

        # Create processor and run
        processor = DictionaryProcessor(config)
        processor.process_excel_file()

        logging.info("Processing completed successfully")
        return 0

    except Exception as e:
        logging.error(f"Processing failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())