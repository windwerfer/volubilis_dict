#!/usr/bin/env python3
"""Simple test script to run the rewritten dictionary processor."""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def test_imports():
    """Test if all modules can be imported."""
    try:
        import config
        print("✓ config imported successfully")
    except ImportError as e:
        print(f"✗ config import failed: {e}")
        return False

    try:
        import text_formatter
        print("✓ text_formatter imported successfully")
    except ImportError as e:
        print(f"✗ text_formatter import failed: {e}")
        return False

    try:
        import file_handler
        print("✓ file_handler imported successfully")
    except ImportError as e:
        print(f"✗ file_handler import failed: {e}")
        return False

    try:
        import dictionary_processor
        print("✓ dictionary_processor imported successfully")
    except ImportError as e:
        print(f"✗ dictionary_processor import failed: {e}")
        return False

    return True

def test_config():
    """Test configuration functionality."""
    try:
        from config import Config, RegexPatterns

        # Test default config
        config = Config()
        print("✓ Config created successfully")

        # Test regex patterns
        patterns = RegexPatterns()
        print("✓ RegexPatterns created successfully")

        # Test validation with non-existent file
        try:
            config.validate()
            print("✗ Validation should have failed for missing file")
        except ValueError as e:
            print(f"✓ Validation correctly failed: {e}")

        return True
    except Exception as e:
        print(f"✗ Config test failed: {e}")
        return False

def test_text_formatter():
    """Test text formatter functionality."""
    try:
        from config import RegexPatterns
        from text_formatter import TextFormatter

        patterns = RegexPatterns()
        formatter = TextFormatter(patterns)

        # Test basic functionality
        result = formatter.clean_text("  test  ")
        assert result == "test", f"Expected 'test', got '{result}'"
        print("✓ TextFormatter clean_text works")

        result = formatter.clean_text("None")
        assert result == "", f"Expected empty string, got '{result}'"
        print("✓ TextFormatter handles None correctly")

        # Test regex replacement
        replacements = {"a": "b", "c": "d"}
        result = formatter.replace_multi("abcd", replacements)
        assert result == "bbdd", f"Expected 'bbdd', got '{result}'"
        print("✓ TextFormatter replace_multi works")

        return True
    except Exception as e:
        print(f"✗ TextFormatter test failed: {e}")
        return False

def test_file_handler():
    """Test file handler functionality."""
    try:
        from file_handler import FileHandler

        handler = FileHandler()

        # Test directory creation
        test_dir = Path("test_output")
        handler.ensure_directory(test_dir)
        assert test_dir.exists(), "Directory should have been created"
        print("✓ FileHandler ensure_directory works")

        # Clean up
        test_dir.rmdir()

        return True
    except Exception as e:
        print(f"✗ FileHandler test failed: {e}")
        return False

def test_excel_processing():
    """Test Excel processing (mock version)."""
    try:
        import dictionary_processor

        # Check if openpyxl is available
        if not dictionary_processor.OPENPYXL_AVAILABLE:
            print("⚠ OpenPyXL not available - skipping Excel processing test")
            return True

        from config import Config
        from dictionary_processor import DictionaryProcessor

        config = Config()
        # Use a non-existent file to test error handling
        config.dictionary.excel_file = Path("nonexistent.xlsx")

        processor = DictionaryProcessor(config)

        try:
            processor.process_excel_file()
            print("✗ Should have failed with missing file")
            return False
        except Exception as e:
            print(f"✓ Correctly handled missing Excel file: {type(e).__name__}")
            return True

    except Exception as e:
        print(f"✗ Excel processing test failed: {e}")
        return False

def test_caching():
    """Test caching functionality."""
    try:
        from config import Config
        from dictionary_processor import DictionaryProcessor

        config = Config()
        config.dictionary.use_cache = True
        config.dictionary.cache_file = Path("test_cache.pkl")

        processor = DictionaryProcessor(config)

        # Test cache key generation
        key1 = processor._generate_cache_key()
        key2 = processor._generate_cache_key()
        assert key1 == key2, "Cache keys should be identical for same config"
        print("✓ Cache key generation works")

        # Test cache save/load (with empty data)
        test_data = {'test': 'data'}
        processor._save_to_cache(test_data)

        loaded_data = processor._load_from_cache()
        assert loaded_data == test_data, "Loaded data should match saved data"
        print("✓ Cache save/load works")

        # Clean up
        if config.dictionary.cache_file.exists():
            config.dictionary.cache_file.unlink()

        return True
    except Exception as e:
        print(f"✗ Caching test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Running Volubilis Dictionary Processor Tests")
    print("=" * 50)

    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Text Formatter", test_text_formatter),
        ("File Handler", test_file_handler),
        ("Excel Processing", test_excel_processing),
        ("Caching", test_caching),
    ]

    passed = 0
    total = len(tests)

    for name, test_func in tests:
        print(f"\nTesting {name}:")
        if test_func():
            passed += 1
        else:
            print(f"❌ {name} test failed")

    print("\n" + "=" * 50)
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())