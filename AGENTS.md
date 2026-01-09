You are a good Python developer.
Prefer code that is not redundant.
Building usually with: main.py src/vol_mundo_01.11.2025.xlsx --debug-1000
Only build with refresh cache if necessary.
When changing formatting, test if the first 10 entries are correctly formatted.
Use best practice approaches as often as possible.
Advise the user if better ways to code a specific problem are available.
Important workflow: For en-th entries, the ENG field may contain multiple English definitions separated by '; ' or '|'. Split ENG by '|' to create headwords. For each headword, set the description in the Thai definition to the full unsplit ENG field, providing complete meaning context.
Terminology Clarification:
• "Scient" refers to the scientific/domain tags (e.g., "MEDIC", "RELIGIO").
• "Definition" could mean the English translation (ENG field) or the HTML description span.

Output File Structures:
• volubilis_th-en.txt: Thai headword → HTML definition (Thai word + pronunciation + English translation + metadata)
• volubilis_th-pr-en.txt: Pronunciation-prefixed headword (.pronunciation - thai) → HTML definition
• volubilis_en-th.txt: English headword → HTML definition with nested Thai equivalents (Thai word + pronunciation + English definition)
• volubilis_th-pr-merge-en.txt: Merged pronunciation headword (,pronunciation - thai1, thai2, ...) → merged HTML definitions