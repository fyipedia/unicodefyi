# unicodefyi

[![PyPI](https://img.shields.io/pypi/v/unicodefyi)](https://pypi.org/project/unicodefyi/)
[![Python](https://img.shields.io/pypi/pyversions/unicodefyi)](https://pypi.org/project/unicodefyi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Pure Python Unicode character toolkit. Compute 17 encoding representations and full Unicode properties for any character. Includes character search across 20 Unicode ranges, 90 HTML entity mappings, and 48 script-to-slug conversions.

> Look up any character at [unicodefyi.com](https://unicodefyi.com/)

## Install

```bash
pip install unicodefyi              # Core (zero deps)
pip install "unicodefyi[full]"      # + fonttools for Unicode block/script
```

## Quick Start

```python
from unicodefyi import get_encodings, get_char_info, search

# Encode any character (17 formats)
enc = get_encodings("✓")
print(enc.unicode)        # U+2713
print(enc.html_entity)    # &check;
print(enc.css)            # \2713
print(enc.go)             # \u2713
print(enc.rust)           # \u{2713}
print(enc.utf8_bytes)     # e2 9c 93
print(enc.utf32be_bytes)  # 00 00 27 13

# Full Unicode properties (requires fonttools for block/script)
info = get_char_info(0x2713)
print(info.name)          # CHECK MARK
print(info.category_name) # Other Symbol
print(info.block)         # Dingbats
print(info.script_slug)   # common

# Search characters by name
results = search("arrow")
for r in results[:5]:
    print(f"U+{r.codepoint:04X} {r.character} {r.name}")
```

## API Reference

### Core Functions

| Function | Description |
|----------|-------------|
| `get_encodings(char) -> EncodingInfo` | 17 encoding representations |
| `get_char_info(codepoint) -> CharInfo \| None` | Full Unicode properties + encodings |
| `search(query, limit=50) -> list[CharInfo]` | Search by character name |
| `get_category_name(code) -> str` | Category code to human name |
| `lookup_html_entity(entity) -> str \| None` | Entity string to character |

### Data Types

- **`EncodingInfo`** — 17-field NamedTuple: unicode, decimal, html_decimal, html_hex, html_entity, css, javascript, python, java, go, ruby, rust, c_cpp, url_encoded, utf8_bytes, utf16be_bytes, utf32be_bytes
- **`CharInfo`** — 14-field NamedTuple: codepoint, character, name, category, category_name, block, block_slug, script, script_slug, bidirectional, combining, mirrored, decomposition, encodings

### Constants

| Constant | Count | Description |
|----------|-------|-------------|
| `GENERAL_CATEGORY_NAMES` | 30 | Full UAX #44 category names |
| `SCRIPT_CODE_TO_SLUG` | 48 | ISO 15924 script codes to SEO-friendly slugs |
| `HTML_ENTITIES` | 90 | Codepoint-to-entity mappings |
| `HTML_ENTITY_TO_CHAR` | 90 | Entity-to-character reverse mappings |

## 17 Encoding Formats

| Format | Example (`✓`) | Language |
|--------|---------------|----------|
| Unicode | `U+2713` | Standard |
| Decimal | `10003` | — |
| HTML decimal | `&#10003;` | HTML |
| HTML hex | `&#x2713;` | HTML |
| HTML entity | `&check;` | HTML |
| CSS | `\2713` | CSS |
| JavaScript | `\u2713` | JS |
| Python | `\u2713` | Python |
| Java | `\u2713` | Java |
| Go | `\u2713` | Go |
| Ruby | `\u{2713}` | Ruby |
| Rust | `\u{2713}` | Rust |
| C/C++ | `\u2713` | C/C++ |
| URL-encoded | `%E2%9C%93` | URL |
| UTF-8 bytes | `e2 9c 93` | Binary |
| UTF-16 BE | `27 13` | Binary |
| UTF-32 BE | `00 00 27 13` | Binary |

## Features

- **17 encoding types**: The most comprehensive encoding toolkit — covers 10+ programming languages
- **Unicode properties**: name, category, block, script, bidirectional, combining, mirrored, decomposition
- **Character search**: Scan 20 Unicode ranges (Latin, Greek, Cyrillic, CJK, symbols, etc.)
- **90 HTML entities**: Common entities with bidirectional lookup
- **48 script mappings**: ISO 15924 script codes to SEO-friendly slugs
- **30 general categories**: Full UAX #44 category names
- **Zero required deps**: Core uses only stdlib (`unicodedata`, `urllib.parse`)
- **Optional fonttools**: Install `unicodefyi[full]` for block and script info
- **Type-safe**: Full type annotations, `py.typed` marker (PEP 561)

## Related Packages

| Package | Description |
|---------|-------------|
| [symbolfyi](https://github.com/fyipedia/symbolfyi) | Lighter symbol toolkit with 11 encodings |
| [colorfyi](https://github.com/fyipedia/colorfyi) | Color conversion, contrast, harmonies, shades |
| [emojifyi](https://github.com/fyipedia/emojifyi) | Emoji encoding & metadata for 3,781 emojis |
| [fontfyi](https://github.com/fyipedia/fontfyi) | Google Fonts metadata, CSS helpers, font pairings |

## Links

- [Unicode Character Browser](https://unicodefyi.com/) — Look up any character online
- [API Documentation](https://unicodefyi.com/developers/) — REST API with free access
- [Source Code](https://github.com/fyipedia/unicodefyi)

## License

MIT
