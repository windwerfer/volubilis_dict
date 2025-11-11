# volubilis_dict

   unofficial dictionary (stardict/mdict/mobi) files for the volubilis project (https://belisan-volubilis.blogspot.com).<br>
   <br>
    most recent version: 01.11.2025 (processed 2025-11-11).<br>
    software version: 1.1.0<br>
  <br>


  - 106'141 entries thai-english<br>
  - 95'944 entries english-thai<br>
 - thai pronounciation for most words, eg. ม้า [máa] n. classifier: ตัว
 - many expressions, like: ทิ้งไว้ [thíng wái] v. exp. leave behind ; leave undone<br>
  - **New**: HTML-formatted definitions with CSS styling for GoldenDict NG<br>
  - **New**: Pronunciation-based search dictionaries (.pr and .pr-merge variants)<br>
  - **New**: Automatic MOBI file generation for Kindle using Calibre<br>
  - **New**: Environment variable configuration support with .env files<br>
  - **New**: Comprehensive unit test suite (50+ tests)<br><br><br>

## Installation

```bash
pip install -r requirements.txt
# Optional: for Stardict format conversion
pip install pyglossary tqdm progressbar2
# Optional: for MOBI format generation (recommended)
# Install Calibre from https://calibre-ebook.com/
# Optional: for .env file support
pip install python-dotenv
```

## Quick Start

```bash
# Process Excel file and create Stardict packages
python main.py src/vol_mundo_01.11.2025.xlsx

# The stardict/ directory will contain:
# - Individual zip packages for each dictionary variant
# - CSS resources for GoldenDict NG
# - Intermediate files organized in subdirectories
```

## Usage

### Automated Stardict Package Creation

Create complete Stardict packages from Excel file:
```bash
python main.py src/vol_mundo_01.11.2025.xlsx
```

This single command will:
1. Process the Excel file to tab-separated text files
2. Convert to Stardict format (.ifo/.idx/.dict files)
3. Package each dictionary with CSS resources into individual zip files

### Command Line Options

```bash
python main.py [OPTIONS] EXCEL_FILE

positional arguments:
  excel_file            Path to the Excel file to process

options:
  --output-dir OUTPUT_DIR, -o OUTPUT_DIR
                        Output directory for processed txt files (default: stardict/txt)
  --columns COLUMNS     Number of columns to process (default: 32)
  --no-paiboon          Disable Paiboon transcription system
  --debug-1000          Process only first 1000 rows for debugging
  --verbose, -v         Enable verbose logging
  --config CONFIG       Path to configuration file (future feature)
  --no-cache            Disable caching of processed data
  --refresh-cache       Force refresh of cache even if valid
```

### Configuration

The dictionary generation can be customized via environment variables or `src/config.py`. A `.env` file is provided with all default values.

#### Using Environment Variables

1. Copy `.env` to your working directory
2. Modify values as needed
3. The application will automatically load these variables

```bash
# Example: Change output directory
VOLUBILIS_OUTPUT_FOLDER=my_output python main.py src/vol_mundo_01.11.2025.xlsx
```

#### Configuration Options

Key options include:

#### Dictionary Processing
- `columns`: Number of columns to process (default: 32)
- `paiboon`: Enable Paiboon transcription system (default: True)
- `debug_test_1000_rows`: Process only first 1000 rows for testing (default: True)

#### Pronunciation Dictionaries
- `th_pron`: Enable/disable pronunciation dictionary generation (default: True)
- `th_pron_prefix`: Prefix for pronunciation headwords (default: '.')
- `th_pron_incl_translation_in_headword`: Include English translations in pron headwords (default: True)
- `th_pron_max_headword_length`: Maximum length for pron headwords (default: 50)
- `th_pron_merge`: Enable/disable merged pronunciation dictionary (default: True)
- `th_pron_merge_prefix`: Prefix for merged pron headwords (default: ',')
- `th_pron_merge_incl_translation_in_headword`: Include translations in merge headwords (default: False)
- `th_pron_merge_max_headword_length`: Maximum length for merge headwords (default: 50)

#### MOBI Build Options
- `enable_mobi_build`: Enable/disable MOBI file generation for Kindle (default: True)
  - **Requires**: Calibre (`ebook-convert` command) must be installed
  - **Output**: Creates `.mobi` files in `stardict/mobi/` directory

### Python API

```python
from src.config import Config
from src.dictionary_processor import DictionaryProcessor

# Load configuration (supports environment variables)
config = Config.from_file()
processor = DictionaryProcessor(config)
processor.process_excel_file()
```

### Caching

The processor includes intelligent caching to speed up repeated processing:

- **Automatic caching**: Processed data is cached to avoid reprocessing the same Excel file
- **Cache validation**: Cache is invalidated when the Excel file changes or configuration changes
- **Cache control**: Command-line options to disable or force refresh cache

```bash
# Force cache refresh
python main.py src/vol_mundo_01.11.2025.xlsx --refresh-cache
```

## Dictionary Formats

### Output File Structures

The processor generates four main dictionary variants in tab-separated format (`headword<TAB>definition`):

#### Thai to English (volubilis_th-en.txt)
- **Headword**: Thai word (may include synonyms joined with `|`)
- **Definition**: HTML-formatted entry containing:
  - Thai word display
  - Pronunciation in brackets
  - Word type and usage
  - English definition
  - Synonyms, scientific names, notes, level information

#### Thai Pronunciation to English (volubilis_th-pr-en.txt)
- **Headword**: Pronunciation-prefixed format (`.pronunciation - thai_word`)
- **Definition**: Same HTML format as Thai to English

#### English to Thai (volubilis_en-th.txt)
- **Headword**: English word (may include synonyms joined with `|`)
- **Definition**: HTML-formatted entry containing:
  - English headword
  - Thai equivalent(s) with pronunciation
  - **Nested English definition** of each Thai word (providing complete context)
  - Word type, usage, and metadata
  - Multiple Thai words for the same English headword are listed separately

#### Pronunciation-Merged Thai to English (volubilis_th-pr-merge-en.txt)
- **Headword**: Merged format (`,pronunciation - thai_word1, thai_word2, ...`)
- **Definition**: Combined HTML definitions for all words sharing the same pronunciation, separated by `<br><br>`

### HTML Format for GoldenDict NG

The processed dictionary uses standard HTML with CSS classes instead of custom tags:

- `<span class="thai">` for Thai text
- `<span class="pron">` for pronunciation
- `<span class="type">` for word type
- `<span class="def">` for definitions
- `<span class="syn">` for synonyms
- `<span class="note">` for notes
- `<span class="science">` for scientific classifications

**GoldenDict NG Setup:**
1. Download and install [GoldenDict NG](https://github.com/xiaoyifang/goldendict-ng)
2. Extract the `res.zip` file to your GoldenDict NG data directory
3. The CSS will be automatically loaded from the `res/` folder
4. Supports light/dark mode switching

### Stardict Format

Convert tab-separated output to Stardict format:

```bash
# Install pyglossary
pip install pyglossary

# Convert Thai-English
pyglossary stardict/txt/volubilis_th-en.txt stardict_output/volubilis_th-en.ifo

# Convert English-Thai
pyglossary stardict/txt/volubilis_en-th.txt stardict_output/volubilis_en-th.ifo
```

The latest Stardict files are available in the `stardict/` directory as individual zip packages.

### MOBI Format for Kindle

MOBI files for Kindle are automatically generated when `enable_mobi_build = True` in the configuration.

**Requirements:**
- Install [Calibre](https://calibre-ebook.com/) (provides the `ebook-convert` command)
- Ensure `ebook-convert` is in your PATH

**Usage:**
```bash
# MOBI files are created automatically during build
python main.py src/vol_mundo_01.11.2025.xlsx

# Files will be available in stardict/mobi/:
# - volubilis_th-en.mobi
# - volubilis_en-th.mobi
# - volubilis_th-pr-en.mobi
# - volubilis_th-pr-merge-en.mobi
```

Transfer these `.mobi` files directly to your Kindle device or use with Kindle apps.

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_config.py

# Run tests with verbose output
pytest -v
```

### Project Structure

```
main.py                 # Root-level CLI entry point
.env                    # Environment variable configuration template
res.zip                 # CSS resources for GoldenDict NG
requirements.txt        # Python dependencies
setup.py               # Package setup
pytest.ini            # Test configuration
src/
├── __init__.py          # Package initialization
├── config.py            # Configuration management
├── exceptions.py        # Custom exceptions
├── file_handler.py      # File I/O utilities
├── text_formatter.py    # Text processing and regex transformations
├── dictionary_processor.py  # Main Excel processing logic
├── stardict_builder.py  # Stardict conversion and packaging
└── main.py              # Legacy CLI (deprecated)

stardict/               # Generated Stardict packages
├── txt/                 # Intermediate files
│   ├── css.zip          # CSS resources (copied from root)
│   ├── cache.pkl        # Processing cache
│   ├── volubilis_en-th.txt      # English to Thai (tab-separated)
│   ├── volubilis_th-en.txt      # Thai to English (tab-separated)
│   ├── volubilis_th-pr-en.txt   # Thai pronunciation to English (tab-separated)
│   └── volubilis_th-pr-merge-en.txt # Pronunciation-merged Thai to English (tab-separated)
├── unzipped/            # Raw Stardict files
│   ├── volubilis_th-en.ifo
│   ├── volubilis_th-en.idx
│   ├── volubilis_th-en.dict
│   └── volubilis_th-en.res.zip  # CSS resources per dictionary
├── volubilis_th-en.zip      # Thai to English package
├── volubilis_en-th.zip      # English to Thai package
├── volubilis_th-pr-en.zip   # Thai with pronunciation package
└── volubilis_th-pr-merge-en.zip # Pronunciation-merged Thai package

mobi/                         # Kindle MOBI format files
├── volubilis_th-en.mobi       # Thai to English MOBI (ready for Kindle)
├── volubilis_en-th.mobi       # English to Thai MOBI (ready for Kindle)
├── volubilis_th-pr-en.mobi    # Thai with pronunciation MOBI (ready for Kindle)
└── volubilis_th-pr-merge-en.mobi # Pronunciation-merged MOBI (ready for Kindle)

 tests/
 ├── conftest.py          # Shared test fixtures
 ├── test_config.py       # Configuration tests
 ├── test_dictionary_processor.py  # Core processing tests
 ├── test_stardict_builder.py     # Stardict building tests
 ├── test_file_handler.py         # File I/O tests
 ├── test_main.py         # CLI interface tests
 └── test_text_formatter.py       # Text processing tests

 requirements.txt         # Python dependencies
 setup.py                # Package setup
 pytest.ini             # Test configuration
```
src/
├── __init__.py          # Package initialization
├── config.py            # Configuration management
├── exceptions.py        # Custom exceptions
├── file_handler.py      # File I/O utilities
├── text_formatter.py    # Text processing and regex transformations
├── dictionary_processor.py  # Main Excel processing logic
├── main.py              # CLI interface
├── vol_mundo_01.11.2025.xlsx  # Source Excel file
├── readme.txt           # Legacy documentation
├── convert_tabTxt_to_mdxTxt.py  # Legacy MDX conversion
└── main__excel_extract_columns_to_txt-v10.py  # Legacy processing script

res/
└── styles.css           # CSS styling for GoldenDict NG

stardict_output/         # Generated Stardict files
├── volubilis_th-en.ifo
├── volubilis_th-en.idx
├── volubilis_th-en.dict
├── volubilis_en-th.ifo
├── volubilis_en-th.idx
├── volubilis_en-th.dict
└── ... (additional variants)



tests/
└── test_text_formatter.py  # Unit tests

requirements.txt         # Python dependencies
setup.py                # Package setup
pytest.ini             # Test configuration
res.zip                 # CSS resources for GoldenDict NG
volubilis_stardict_2025-11-11.zip  # Latest Stardict package
```

<img  style='width:90%;max-width:1445px;'  src='https://github.com/windwerfer/volubilis_dict/blob/main/screenshot/example_thai_lookup.png'><br>
the dictioanry is bilangual: Thai-English <br><br>

<img style='width:90%;max-width:1445px;' src='https://github.com/windwerfer/volubilis_dict/blob/main/screenshot/example_english_lookup.png'>
and English-Thai has a Level to each word, judging how basic it is (B = basic, A1 = intermediate, A2 = advanced, s = special).<br><br><br>

<img  style='width:80%;max-width:1445px;'  src='https://github.com/windwerfer/volubilis_dict/blob/main/screenshot/example_pronouciation_search-dictbox_android.png'><br>
 there is a pronounciation search. eg .maa (the sound of the thai word) would find มา, ม้า and หมา. almost every word has a pronuciation entry. The .pr-merge variant groups words by pronunciation, showing tone-variants together.<br><br><br>

this project converts the Volubilis Thai-English dictionary (released as spread sheat or pdf) to a standart dictionary format.<br><br><br>

 Readable through <a href='http://www.huzheng.org/stardict/'>Stardict</a> (win/linux), <a href='https://www.mdict.cn/'>Mdict</a> (android/ios), <a href='http://goldendict.org/'>GoldenDict</a> (win/linux/android), <a href='https://www.google.co.th/url?sa=t&source=web&rct=j&url=https://play.google.com/store/apps/details%3Fid%3Dcom.grandsons.dictboxxth%26hl%3Den%26gl%3DUS%26referrer%3Dutm_source%253Dgoogle%2526utm_medium%253Dorganic%2526utm_term%253Ddict%2Bbox%2Bapp%2Bstore%26pcampaignid%3DAPPU_1_nfq6Y6nnDfOgz7sPt-CzqAU&ved=2ahUKEwjpqcaUvbj8AhVz0HMBHTfwDFUQ8oQBegQIChAB&usg=AOvVaw0SlLHjPWaRVXbk4INevGNt'>Dictbox</a> (android 4-9), Kindle (MOBI/EPUB format)<br><br><br><br>

  <b>Install / use:</b>
  to be able to use the dictionary files, you need to download one of the dictionary apps from above and then download the compiled Stardict zip packages from the `stardict/` directory (.ifo/.idx/.dict/.syn/.res.zip for Stardict/GoldenDict, convert to .mdx for Mdict) and after extracting, copy them into the dictionary folder.<br><br>

**GoldenDict NG Users:** Each Stardict zip package includes a `res.zip` with CSS for automatic styling with light/dark themes.<br><br>

**Kindle Users:** The `stardict/mobi/` folder contains ready-to-use `.mobi` files created with Calibre. These can be directly transferred to your Kindle device or used with Kindle apps.<br><br><br><br><br><br><br>


## Excel Column Mapping

The Excel file uses the following column mapping for data extraction:

- 0: THAIROM → thai_romanized
- 1: EASYTHAI → easythai
- 2: THAIPHON → thaiphon (pronunciation)
- 3: THA (Thai) → thai (word)
- 4: ENG (English) → english (definition)
- 5: FRA (French) → unused
- 6: TYPE → unused
- 7: USAGE → type_word
- 8: SCIENT/abbrev. → scient
- 9: DOM → dom
- 10: CLASSIF → classif
- 11: SYN → syn
- 12: LEVEL → level
- 13: NOTE → note
- 14: SPA (Spanish) → unused
- 15: ITA (Italian) → unused
- 16: POR (Portuguese) → unused
- 17: DEU (German) → unused
- 18: NLD (Dutch) → unused
- 19: NOR (Norwegian [bokmål]) → unused
- 20: TUR (Turkish) → unused
- 21: MSA (Malay [Rumi script]) → unused
- 22: IND (Indonesian) → unused
- 23: FIL (Filipino [Tagalog (tgl)]) → unused
- 24: VIE (Vietnamese [chữ quốc ngữ]) → unused
- 25: RUS1 (Russian) → unused
- 26: RUS2 (Russian [GOST romanization]) → unused
- 27: LAO1 (Lao) → unused
- 28: LAO2 (Lao) → unused
- 29: TTS1 [Isan] → unused
- 30: TTS2 [Isan] → unused
- 31: KOR1 (Korean [Hangeul]) → unused
- 32: KOR2 (Korean [Revised Romanization of Korean]) → unused
- 33: ZHO1 (Chinese [simplified/traditional]) → unused
- 34: ZHO2 (Chinese [Pinyin [effective]]) → unused

Synonyms are extracted from columns 3 (THA; split by `;`) and 11 (SYN; Thai words in parentheses), joined with `|` for headword synonyms in Stardict format.

---


## For Developers

The codebase has been completely rewritten with modern Python practices:

- **Modular Architecture**: Separated concerns into focused classes
- **Type Hints**: Full type annotation coverage
- **Configuration Management**: Centralized settings with validation
- **Error Handling**: Custom exceptions and proper logging
- **Testing**: Unit tests with pytest
- **CLI Interface**: Command-line interface with argparse

### Key Improvements

1. **TextFormatter**: Handles all regex transformations and text processing
2. **DictionaryProcessor**: Main Excel parsing and data processing logic with intelligent caching
3. **FileHandler**: Safe file I/O with context managers
4. **Config**: Centralized configuration with environment variable support
5. **Custom Exceptions**: Proper error handling hierarchy
6. **Caching System**: Automatic caching with validation for faster development and testing
7. **HTML Conversion**: Transforms custom tags to standard HTML with CSS classes for modern dictionary apps
8. **GoldenDict NG Support**: Includes CSS themes with light/dark mode for enhanced readability
9. **Automated Pipeline**: Single command creates complete Stardict packages with proper directory structure
10. **Stardict Builder**: Integrated conversion and packaging system for professional distribution
11. **Pronunciation Dictionaries**: Generates pronunciation-based search variants (.pr and .pr-merge)
12. **Tone-Aware Sorting**: Pronunciation merge groups words by sound with proper tone ordering
13. **MOBI Support**: Automatic Kindle .mobi file generation using Calibre
14. **Environment Configuration**: Flexible configuration via .env files and environment variables
15. **Comprehensive Testing**: Extensive unit test suite with 50+ tests covering all major components
16. **Modern Python**: Type hints, dataclasses, and clean architecture throughout

### Legacy Code

The original scripts are preserved in `src/` for reference:
- `convert_tabTxt_to_mdxTxt.py`: MDX conversion utility
- `main__excel_extract_columns_to_txt-v10.py`: Original Excel processing script

The new codebase provides the same functionality with better maintainability and extensibility.

the script was written without any thought of publishing it (bad coding, and lots of manual intervention, so just: for research purposes), but because i use the final product myself a lot, i thought i make it available.

---

copyright of the volubilis project:
All information contained in the files can be used freely. I just invite you to mention the source.
--Francis Bastien

the copyright of this github project is therefore the same (all files may be used without restrain)
