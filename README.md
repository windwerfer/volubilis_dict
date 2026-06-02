# volubilis_dict

   unofficial dictionary (stardict/mdict/yomitan) files for the volubilis project (https://belisan-volubilis.blogspot.com).<br>
   <br>
     most recent version: 01.11.2025 (processed 2025-11-11).<br>
   <br>


  - 106'141 entries thai-english<br>
  - 95'944 entries english-thai<br>
  - thai pronounciation for most words, eg. ม้า [máa] n. classifier: ตัว
  - many expressions, like: ทิ้งไว้ [thíng wái] v. exp. leave behind ; leave undone<br>
  - HTML-formatted definitions with CSS styling for GoldenDict NG<br>
  - Pronunciation-based search dictionaries (.pr and .pr-merge dictionary variants)<br>
  - Inline CSS support (--inline-css) for embedded styling
  - Compressed Stardict dictionaries (.dict.dz) for reduced file sizes<br><br><br>




**GoldenDict NG Setup:**
1. Download and install [GoldenDict NG](https://github.com/xiaoyifang/goldendict-ng)
2. Extract the stardict dictionary files ( https://github.com/windwerfer/volubilis_dict/releases ) into a folder and add that folder in goldendict (edit->dictionaries->sources->files->add..)
4. Supports light/dark mode switching




<img  style="width:500px;"  src="https://github.com/windwerfer/volubilis_dict/blob/main/screenshot/example_thai_lookup.png"><br>
the dictioanry is bilangual: Thai-English <br><br>

<img style='width:500px;' src='https://github.com/windwerfer/volubilis_dict/blob/main/screenshot/example_english_lookup.png'>
    
and English-Thai has a Level to each word, judging how basic it is (B = basic, A1 = intermediate, A2 = advanced, s = special).<br><br><br>

<img  style='width:500px;'  src='https://github.com/windwerfer/volubilis_dict/blob/main/screenshot/example_pronouciation_search-dictbox_android.png'><br>
 there is a pronounciation search. eg .maa (the sound of the thai word) would find มา, ม้า and หมา. almost every word has a pronuciation entry. The .pr-merge variant groups words by pronunciation, showing tone-variants together.<br><br><br>

this project converts the Volubilis Thai-English dictionary (released as spread sheat or pdf) to a standart dictionary format.<br><br><br>


## Installation

### Using uv (recommended)

`uv` is the modern, fast way to manage this project. It uses `pyproject.toml` + `uv.lock` for reproducible environments and automatically uses/manages the venv setup.

```bash
# 1. Install uv (one-time): https://docs.astral.sh/uv/
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Clone and set up the project
git clone https://github.com/windwerfer/volubilis_dict.git
cd volubilis_dict
uv sync
```

Run commands with the locked environment:

```bash
uv run python main.py data/vol_mundo_01.11.2025.xlsx --debug-1000
# or: uv run volubilis-dict data/vol_mundo_01.11.2025.xlsx --debug-1000
```

(After `uv sync` you can also `source .venv/bin/activate` and use plain `python` / `volubilis-dict`.)

### Classic pip (no uv)


```bash
git clone https://github.com/windwerfer/volubilis_dict.git
cd volubilis_dict
pip install -e .
```


## Recommended Installation

Because of the danger of supply chain attacks we *hugely* recommend using the provided devcontainer.

```bash
git clone https://github.com/windwerfer/volubilis_dict.git
```

- Then open the project in VSCode or Zed — it will offer to create the Devcontainer. This gives you a fully reproducible environment that cannot see the rest of your host machine. it should automatically pull all the required packages and uv.

- then open the terminal inside VSCode / Zed and run

```bash
uv run python main.py data/vol_mundo_01.11.2025.xlsx --debug-1000
# or: uv run volubilis-dict data/vol_mundo_01.11.2025.xlsx --debug-1000
```



## Managing Dependencies (uv + pyproject.toml)

`pyproject.toml` is the **single source of truth** for what the project needs.

- Core + required build tools (openpyxl, pyglossary, mdict-utils, python-idzip, etc.) live under `[project] dependencies`.
- Test / development tools live under `[project.optional-dependencies] dev`.

### How the locked reproducible approach works

1. Edit `pyproject.toml` when you want to add or change a dependency.
2. Run `uv lock` to resolve the full tree and update `uv.lock`.
3. Commit `uv.lock`.
4. Other people run `uv sync` (or `uv sync --extra dev`) and get bit-identical packages.


## Usage

### Automated Stardict Package Creation

Create complete Stardict packages from Excel file:
```bash
# Preferred (uv users)
uv run python main.py data/vol_mundo_01.11.2025.xlsx

# Or after `uv sync` + activating the venv, or for classic pip users:
python main.py data/vol_mundo_01.11.2025.xlsx
```

The command will:
1. Process the Excel file to tab-separated text files
2. Convert to Stardict format (.ifo/.idx/.dict files)
3. Convert to MDict format (.mdx/.mdd)


### Command Line Options

```bash
uv run python main.py [OPTIONS] EXCEL_FILE
# or after activating the venv, or with plain pip: python main.py ...

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
  --inline-css          Inline CSS styles in each dictionary entry
  --no-dz               Disable .dict.dz compression for Stardict format
  --create-mobi         Create MOBI format files for Kindle (not working correctly at the moment)
  -v                    show version
```


#### Further details

Two additional pronunciation-based dictionary files are generated by default (alongside the normal `th-en` and `en-th` files):

- `volubilis_th-pr-en.txt` — headwords prefixed with pronunciation (e.g. `.pron - thai (eng)`). One entry per Thai word.
- `volubilis_th-pr-merge-en.txt` — merged by pronunciation (e.g. `,pron - thai1, thai2, ...`). All Thai words sharing the same pronunciation are grouped, with definitions combined.


#### more settings options

The following options are **not available as command-line flags**. They are controlled exclusively via environment variables:

- `VOLUBILIS_TH_PRON` — Enable/disable `th-pr-en` generation (default: `true`)
- `VOLUBILIS_TH_PRON_PREFIX` — Prefix for pronunciation headwords (default: `.`)
- `VOLUBILIS_TH_PRON_INCL_TRANSLATION` — Include English translation in pron headwords (default: `true`)
- `VOLUBILIS_TH_PRON_MAX_LENGTH` — Maximum length for pron headwords (default: `50`)
- `VOLUBILIS_TH_PRON_MERGE` — Enable/disable merged pronunciation dictionary (default: `true`)
- `VOLUBILIS_TH_PRON_MERGE_PREFIX` — Prefix for merged pron headwords (default: `,`)
- `VOLUBILIS_TH_PRON_MERGE_INCL_TRANSLATION` — Include translations in merge headwords (default: `false`)
- `VOLUBILIS_TH_PRON_MERGE_MAX_LENGTH` — Maximum length for merge headwords (default: `50`)

Example — disable the merged pronunciation dictionary:

```bash
VOLUBILIS_TH_PRON_MERGE=false uv run python main.py data/vol_mundo_01.11.2025.xlsx
```

### Caching

The processor includes intelligent caching to speed up repeated processing:

- **Automatic caching**: Processed data is cached to avoid reprocessing the same Excel file
- **Cache validation**: Cache is invalidated when the Excel file changes or configuration changes
- **Cache control**: Command-line options to disable or force refresh cache

```bash
# Force cache refresh
uv run python main.py data/vol_mundo_01.11.2025.xlsx --refresh-cache
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



## Development

### install additional dev packages (installs pkg pytest)

```bash
# using uv
uv sync --extra dev

# old school way
pip install -e ".[dev]"
```


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



## Excel Column Mapping

The authoritative mapping lives in `COLUMN_DEFS` (module-level list in
`src/volubilis_dict/config.py`). `COLUMN_MAPPING` is derived from it and is the
single source of truth for:

- which semantic variable pulls which column (`_get_col("type_word", row)` etc.)
- the "Column mapping:" log lines printed at startup (always truthful, never
  drifts from the extraction code)

Notable:
- 6: TYPE → type_word   (raw grammatical type)
- 7: USAGE → usage      (register/obsol. etc.)
- type_word (col 6) + usage (col 7) are combined when making word definitions:
  the merged label is used for `<span class="word_type">` sections in the
  English→Thai output and appears in the per-entry `<span class="type">` spans
  for all Thai→* outputs.

All columns beyond NOTE log as "unused" for the core dictionary data.
Run the processor to see the exact mapping for your file (it includes the
original header text like "TYPE Arial 11").

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


---

## License

This project follows the same terms as the original Volubilis dictionary data:

> All information contained in the files can be used freely. I just invite you to mention the source.

— Francis Bastien (Belisan Volubilis)

The code and tooling in this GitHub repository (https://github.com/windwerfer/volubilis_dict) are provided under the same permissive terms. You are free to use, modify, and distribute everything without restriction, with attribution appreciated.
