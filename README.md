# volubilis_dict

   unofficial dictionary (stardict/mdict/mobi) files for the volubilis project (https://belisan-volubilis.blogspot.com).<br>
   <br>
    most recent version: 01.11.2025 (processed 2025-11-11).<br>
    software version: 1.2.0<br>
  <br>


  - 106'141 entries thai-english<br>
  - 95'944 entries english-thai<br>
 - thai pronounciation for most words, eg. ม้า [máa] n. classifier: ตัว
 - many expressions, like: ทิ้งไว้ [thíng wái] v. exp. leave behind ; leave undone<br>
  - **New**: HTML-formatted definitions with CSS styling for GoldenDict NG<br>
  - **New**: Pronunciation-based search dictionaries (.pr and .pr-merge variants)<br>
  - **New**: Inline CSS support (--inline-css) for embedded styling
  - **New**: Compressed Stardict dictionaries (.dict.dz) for reduced file sizes<br><br><br>




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

```bash
git clone https://github.com/windwerfer/volubilis_dict.git
cd volubilis_dict
pip install -r requirements.txt
```

## Usage

### Automated Stardict Package Creation

Create complete Stardict packages from Excel file:
```bash
# Create Stardict and MDict packages
python main.py src/vol_mundo_01.11.2025.xlsx

```

The command will:
1. Process the Excel file to tab-separated text files
2. Convert to Stardict format (.ifo/.idx/.dict files)
3. Convert to MDict format (.mdx/.mdd)


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
   --inline-css          Inline CSS styles in each dictionary entry
   --no-dz               Disable .dict.dz compression for Stardict format
   --create-mobi         Create MOBI format files for Kindle (not working correctly at the moment)
```


#### Pronunciation Dictionaries
- `th_pron`: Enable/disable pronunciation dictionary generation (default: True)
- `th_pron_prefix`: Prefix for pronunciation headwords (default: '.')
- `th_pron_incl_translation_in_headword`: Include English translations in pron headwords (default: True)
- `th_pron_max_headword_length`: Maximum length for pron headwords (default: 50)
- `th_pron_merge`: Enable/disable merged pronunciation dictionary (default: True)
- `th_pron_merge_prefix`: Prefix for merged pron headwords (default: ',')
- `th_pron_merge_incl_translation_in_headword`: Include translations in merge headwords (default: False)
- `th_pron_merge_max_headword_length`: Maximum length for merge headwords (default: 50)



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


---

copyright of the volubilis project:
All information contained in the files can be used freely. I just invite you to mention the source.
--Francis Bastien

the copyright of this github project is therefore the same (all files may be used without restrain)
