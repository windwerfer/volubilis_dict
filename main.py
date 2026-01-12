"""Main CLI interface for the Volubilis dictionary processor."""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

from src.config import Config
from src.dictionary_processor import DictionaryProcessor
from src.mdict_builder import MdictBuilder
from src.stardict_builder import StardictBuilder
from src.utils_builder import UtilsBuilder


def setup_logging(verbose: bool = False) -> None:
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def _load_css_for_mdx(mdict_dir: Path) -> Optional[str]:
    """Load CSS content for embedding in MDX definitions."""
    css_file = mdict_dir / "txt" / "styles.css"
    if css_file.exists():
        return css_file.read_text(encoding="utf-8")
    return None


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        description="Process Volubilis Thai-English dictionary Excel files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py vol_mundo_01.06.2023.xlsx    # Process Excel file
  python main.py custom.xlsx --output-dir output/
  python main.py file.xlsx --verbose          # Enable debug logging
  python main.py file.xlsx --debug-1000       # Process only first 1000 rows for testing
  python main.py file.xlsx --no-cache         # Disable caching
  python main.py file.xlsx --refresh-cache    # Force cache refresh
        """,
    )

    parser.add_argument(
        "excel_file", type=Path, help="Path to the Excel file to process"
    )

    parser.add_argument(
        "--output-dir",
        "-o",
        type=Path,
        default=Path("stardict/txt"),
        help="Output directory for processed txt files",
    )

    parser.add_argument(
        "--columns", type=int, default=32, help="Number of columns to process"
    )

    parser.add_argument(
        "--no-paiboon", action="store_true", help="Disable Paiboon transcription system"
    )

    parser.add_argument(
        "--debug-1000",
        action="store_true",
        help="Process only first 1000 rows for debugging",
    )

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    parser.add_argument(
        "--config", type=Path, help="Path to configuration file (future feature)"
    )

    parser.add_argument(
        "--no-cache", action="store_true", help="Disable caching of processed data"
    )

    parser.add_argument(
        "--refresh-cache",
        action="store_true",
        help="Force refresh of cache even if valid",
    )

    parser.add_argument(
        "--inline-css",
        action="store_true",
        help="Inline CSS styles in each dictionary entry",
    )

    parser.add_argument(
        "--no-dz",
        action="store_true",
        help="Disable .dict.dz compression for Stardict format",
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
        config = Config.from_file()

        # Override config with command line arguments
        config.dictionary.excel_file = args.excel_file
        config.dictionary.output_folder = args.output_dir
        config.dictionary.columns = args.columns
        config.dictionary.paiboon = not args.no_paiboon
        config.dictionary.debug_test_1000_rows = args.debug_1000
        config.dictionary.use_cache = not args.no_cache
        config.dictionary.force_refresh_cache = args.refresh_cache
        config.dictionary.inline_css = args.inline_css
        config.dictionary.no_dz = args.no_dz

        # Validate configuration
        config.validate()

        # Setup shared resources
        stardict_dir = Path("stardict")
        mdict_dir = Path("mdict")
        UtilsBuilder.setup_resources(stardict_dir, mdict_dir, config)

        # Create processor and run
        processor = DictionaryProcessor(config, config.dictionary.css_content)
        processor.process_excel_file()

        # Build Stardict packages
        builder = StardictBuilder(
            args.output_dir, stardict_dir, css_content=config.dictionary.css_content, config=config.dictionary
        )
        logging.info("Converting to Stardict format...")
        builder.convert_to_stardict()

        logging.info("Creating zip packages...")
        zip_files = builder.create_zip_packages()

        # Convert to MDX format (CSS handled in definitions)
        mdx_builder = MdictBuilder(args.output_dir, mdict_dir, None)
        logging.info("Converting to MDX format...")
        mdx_builder.convert_to_mdx()

        # Convert to MOBI format if enabled and calibre is available
        if config.dictionary.enable_mobi_build:
            import shutil

            if shutil.which("ebook-convert"):
                logging.info("Converting to MOBI format...")
                builder.convert_to_mobi()
            else:
                logging.warning("Calibre not found - skipping MOBI conversion")

        logging.info("Processing completed successfully")
        logging.info(f"Created {len(zip_files)} Stardict packages:")
        for zip_file in zip_files:
            logging.info(f"  - {zip_file}")

        # Final check for MOBI build requirements
        if config.dictionary.enable_mobi_build:
            import shutil

            if not shutil.which("ebook-convert"):
                print(
                    "\033[91mError: calibre not found. Please install calibre to build MOBI files.\033[0m"
                )

        return 0

    except Exception as e:
        logging.error(f"Processing failed: {e}")
        if args.verbose:
            import traceback

            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
