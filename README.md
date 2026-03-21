# unicodefyi

[![PyPI version](https://agentgif.com/badge/pypi/unicodefyi/version.svg)](https://pypi.org/project/unicodefyi/)
[![Python](https://img.shields.io/pypi/pyversions/unicodefyi)](https://pypi.org/project/unicodefyi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Pure Python Unicode character toolkit for developers. Compute [17 encoding representations](https://unicodefyi.com/developers/) (Unicode, HTML, CSS, JavaScript, Python, Java, Go, Ruby, Rust, C/C++, URL, UTF-8, UTF-16, UTF-32), look up full [Unicode properties](https://unicodefyi.com/block/) (name, category, block, script), resolve [92 HTML entities](https://unicodefyi.com/search/), and [search characters by name](https://unicodefyi.com/search/) -- all with zero dependencies.

> **Try the interactive tools at [unicodefyi.com](https://unicodefyi.com/)** -- [Unicode search](https://unicodefyi.com/search/), [Unicode blocks](https://unicodefyi.com/block/), [Unicode scripts](https://unicodefyi.com/script/), and [character collections](https://unicodefyi.com/collection/).

<p align="center">
  <img src="https://raw.githubusercontent.com/fyipedia/unicodefyi/main/demo.gif" alt="unicodefyi CLI demo" width="800">
</p>

## Table of Contents

- [Install](#install)
- [Quick Start](#quick-start)
- [What You Can Do](#what-you-can-do)
  - [Character Lookup](#character-lookup)
  - [17 Encoding Formats](#17-encoding-formats)
  - [HTML Entities](#html-entities)
- [17 Encoding Formats](#17-encoding-formats-1)
- [HTML Entity Lookup](#html-entity-lookup)
- [Character Search](#character-search)
- [Command-Line Interface](#command-line-interface)
- [MCP Server (Claude, Cursor, Windsurf)](#mcp-server-claude-cursor-windsurf)
- [REST API Client](#rest-api-client)
- [API Reference](#api-reference)
  - [Encoding & Properties](#encoding--properties)
  - [Data Types](#data-types)
  - [Constants](#constants)
- [Features](#features)
- [Learn More About Unicode](#learn-more-about-unicode)
- [Creative FYI Family](#creative-fyi-family)
- [License](#license)

## Install

```bash
pip install unicodefyi                 # Core engine (zero deps)
pip install "unicodefyi[full]"         # + Block/script info (fonttools)
pip install "unicodefyi[cli]"          # + Command-line interface
pip install "unicodefyi[mcp]"          # + MCP server for AI assistants
pip install "unicodefyi[api]"          # + HTTP client for unicodefyi.com API
pip install "unicodefyi[all]"          # Everything
```

## Quick Start

```python
from unicodefyi import get_encodings, get_char_info, search

# Compute 17 encoding representations for any character
enc = get_encodings("\u2713")
print(enc.unicode)        # U+2713
print(enc.html_entity)    # &check;
print(enc.javascript)     # \u{2713}
print(enc.rust)           # \u{2713}
print(enc.utf8_bytes)     # e2 9c 93

# Full Unicode properties (block/script require fonttools)
info = get_char_info(0x2713)
print(info.name)          # CHECK MARK
print(info.category_name) # Other Symbol
print(info.block)         # Dingbats
print(info.script)        # Zyyy

# Search characters by name
results = search("arrow")
for r in results[:5]:
    print(r.character, r.name)
```

## What You Can Do

### Character Lookup

The Unicode Standard version 16.0 defines over 149,000 characters across 168 blocks and 161 scripts, covering every modern and historical writing system. The `get_char_info()` function retrieves the complete set of Unicode properties for any character -- its official name, general category, block assignment, script classification, bidirectional behavior, and all 17 encoding representations. This is essential for internationalization (i18n), text processing, and debugging character encoding issues.

```python
from unicodefyi import get_char_info, search

# Look up full Unicode properties for any character by codepoint
info = get_char_info(0x00E9)  # Latin small letter e with acute
print(info.name)           # LATIN SMALL LETTER E WITH ACUTE
print(info.category_name)  # Lowercase Letter
print(info.block)          # Latin-1 Supplement
print(info.script)         # Latn
print(info.encodings.html_entity)  # &eacute;

# Search Unicode characters by name substring
results = search("check mark")
for r in results[:3]:
    print(f"{r.character}  U+{r.codepoint:04X}  {r.name}")
# ✓  U+2713  CHECK MARK
# ✔  U+2714  HEAVY CHECK MARK
# ☑  U+2611  BALLOT BOX WITH CHECK
```

Learn more: [Unicode Character Search](https://unicodefyi.com/search/) · [Unicode Block Reference](https://unicodefyi.com/block/)

### 17 Encoding Formats

Developers working across different languages and platforms need characters encoded in platform-specific formats. A single Unicode character can be represented as a UTF-8 byte sequence for web transmission, an HTML entity for markup, a CSS escape for stylesheets, or language-specific literals for Python, JavaScript, Java, Go, Ruby, Rust, and C/C++. The `get_encodings()` function computes all 17 formats in one call.

| Category | Formats | Description |
|----------|---------|-------------|
| Unicode | Codepoint, Decimal | `U+00A9`, `169` |
| HTML | Decimal, Hex, Named Entity | `&#169;`, `&#xA9;`, `&copy;` |
| CSS | Content escape | `\00A9` |
| Languages | Python, JavaScript, Java, Go, Ruby, Rust, C/C++ | Language-specific escape sequences |
| URL | Percent-encoded | `%C2%A9` |
| Binary | UTF-8, UTF-16 BE, UTF-32 BE | Raw byte representations |

```python
from unicodefyi import get_encodings

# Compute all 17 encoding representations for any character
enc = get_encodings("\u2713")  # Check mark
print(enc.unicode)         # U+2713
print(enc.html_entity)     # &check;
print(enc.css)             # \2713
print(enc.javascript)      # \u{2713}
print(enc.python)          # \u2713
print(enc.rust)            # \u{2713}
print(enc.go)              # \u2713
print(enc.utf8_bytes)      # e2 9c 93
```

Learn more: [Character Encoding Converter](encoding/)

### HTML Entities

HTML named entities provide human-readable aliases for commonly used characters -- `&copy;` instead of `&#xA9;`, `&hearts;` instead of `&#x2665;`. The package includes 92 HTML5 named entity mappings with bidirectional lookup: convert an entity name to its character, or find the named entity for a given codepoint. This covers mathematical symbols, currency signs, typographic characters, Greek letters, and common special characters.

| Entity Group | Examples | Count |
|-------------|----------|-------|
| Typographic | `&mdash;`, `&hellip;`, `&laquo;`, `&raquo;` | 20+ |
| Mathematical | `&times;`, `&divide;`, `&plusmn;`, `&infin;` | 15+ |
| Currency | `&euro;`, `&pound;`, `&yen;`, `&cent;` | 5 |
| Greek Letters | `&alpha;`, `&beta;`, `&pi;`, `&omega;` | 24 |
| Arrows & Symbols | `&larr;`, `&rarr;`, `&hearts;`, `&spades;` | 15+ |

```python
from unicodefyi import lookup_html_entity, HTML_ENTITIES

# Reverse lookup: resolve an HTML entity name to its character
char = lookup_html_entity("&euro;")
print(char)       # (euro sign)
print(ord(char))  # 8364

# Forward lookup: find the named entity for a codepoint
entity = HTML_ENTITIES.get(0x00A9)
print(entity)     # &copy;

# Total named entities in the database
print(len(HTML_ENTITIES))  # 92
```

Learn more: [Character Collections](https://unicodefyi.com/collection/)

## 17 Encoding Formats

```python
from unicodefyi import get_encodings

enc = get_encodings("\u00a9")  # Copyright sign
print(enc.unicode)         # U+00A9
print(enc.decimal)         # 169
print(enc.html_decimal)    # &#169;
print(enc.html_hex)        # &#xA9;
print(enc.html_entity)     # &copy;
print(enc.css)             # \00A9
print(enc.javascript)      # \u{A9}
print(enc.python)          # \u00a9
print(enc.java)            # \u00A9
print(enc.go)              # \u00A9
print(enc.ruby)            # \u{A9}
print(enc.rust)            # \u{A9}
print(enc.c_cpp)           # \u00a9
print(enc.url_encoded)     # %C2%A9
print(enc.utf8_bytes)      # c2 a9
print(enc.utf16be_bytes)   # 00 a9
print(enc.utf32be_bytes)   # 00 00 00 a9
```

## HTML Entity Lookup

```python
from unicodefyi import lookup_html_entity, HTML_ENTITIES

# Reverse lookup: entity name to character
char = lookup_html_entity("&hearts;")
print(char)       # (U+2665)
print(ord(char))  # 9829

# Forward lookup: codepoint to entity
entity = HTML_ENTITIES.get(0x20AC)
print(entity)     # &euro;

# 92 HTML5 named entities included
print(len(HTML_ENTITIES))  # 92
```

## Character Search

```python
from unicodefyi import search

# Search by name substring (case-insensitive)
results = search("check mark")
for r in results:
    print(f"{r.character}  U+{r.codepoint:04X}  {r.name}")

# Limit results
arrows = search("arrow", limit=10)
```

## Command-Line Interface

```bash
pip install "unicodefyi[cli]"

unicodefyi info U+2713                 # Character info (CHECK MARK)
unicodefyi info A                      # Character info (LATIN CAPITAL LETTER A)
unicodefyi encode U+2713               # All 17 encodings
unicodefyi search "check mark"         # Search by name
unicodefyi entity "&amp;"              # HTML entity reverse lookup
```

## MCP Server (Claude, Cursor, Windsurf)

Add Unicode tools to any AI assistant that supports [Model Context Protocol](https://modelcontextprotocol.io/).

```bash
pip install "unicodefyi[mcp]"
```

Add to your `claude_desktop_config.json`:

```json
{
    "mcpServers": {
        "unicodefyi": {
            "command": "python",
            "args": ["-m", "unicodefyi.mcp_server"]
        }
    }
}
```

**Available tools**: `char_info`, `char_encode`, `unicode_search`, `html_entity_lookup`

## REST API Client

```bash
pip install "unicodefyi[api]"
```

```python
from unicodefyi.api import UnicodeFYI

with UnicodeFYI() as api:
    info = api.char("2713")                # GET /api/char/2713/
    enc = api.encodings("2713")            # GET /api/char/2713/encodings/
    results = api.search("check mark")     # GET /api/search/?q=check+mark
    blocks = api.blocks()                  # GET /api/blocks/
    block = api.block("arrows")            # GET /api/block/arrows/
    scripts = api.scripts()                # GET /api/scripts/
    confusables = api.confusables("A")     # GET /api/confusables/?char=A
    random_char = api.random()             # GET /api/random/
```

Full [API documentation](https://unicodefyi.com/developers/) with OpenAPI spec at [unicodefyi.com/api/openapi.json](https://unicodefyi.com/api/openapi.json).

## API Reference

### Encoding & Properties

| Function | Description |
|----------|-------------|
| `get_encodings(char) -> EncodingInfo` | 17 encoding representations for any character |
| `get_char_info(codepoint) -> CharInfo` | Full Unicode properties + encodings |
| `get_category_name(code) -> str` | Category code to full name (e.g. "Sm" to "Math Symbol") |
| `lookup_html_entity(entity) -> str` | HTML entity to character (e.g. "&amp;" to "&") |
| `search(query, limit) -> list[CharInfo]` | Search characters by name substring |

### Data Types

| Type | Fields |
|------|--------|
| `EncodingInfo` | unicode, decimal, html_decimal, html_hex, html_entity, css, javascript, python, java, go, ruby, rust, c_cpp, url_encoded, utf8_bytes, utf16be_bytes, utf32be_bytes |
| `CharInfo` | codepoint, character, name, category, category_name, block, block_slug, script, script_slug, bidirectional, combining, mirrored, decomposition, encodings |

### Constants

| Constant | Description |
|----------|-------------|
| `GENERAL_CATEGORY_NAMES` | 30 Unicode general categories |
| `SCRIPT_CODE_TO_SLUG` | 48 script code to URL slug mappings |
| `HTML_ENTITIES` | 92 codepoint to HTML entity mappings |
| `HTML_ENTITY_TO_CHAR` | 92 HTML entity to character reverse mappings |

## Features

- **17 encoding formats**: Unicode, HTML (decimal/hex/entity), CSS, JavaScript, Python, Java, Go, Ruby, Rust, C/C++, URL, UTF-8, UTF-16, UTF-32
- **Full Unicode properties**: name, category, block, script, bidirectional, combining, mirrored, decomposition
- **92 HTML entities**: forward and reverse lookup
- **Character search**: name substring search across common Unicode ranges
- **CLI**: Rich terminal output with formatted tables
- **MCP server**: 4 tools for AI assistants (Claude, Cursor, Windsurf)
- **REST API client**: httpx-based client for [unicodefyi.com API](https://unicodefyi.com/developers/)
- **Zero dependencies**: Core engine uses only `unicodedata` from stdlib
- **Type-safe**: Full type annotations, `py.typed` marker (PEP 561)
- **Fast**: All computations under 1ms

## Learn More About Unicode

- **Browse**: [Unicode Search](https://unicodefyi.com/search/) · [Unicode Blocks](https://unicodefyi.com/block/) · [Scripts](https://unicodefyi.com/script/)
- **Tools**: [Character Lookup](lookup/) · [Encoding Tool](encoding/)
- **Guides**: [Glossary](https://unicodefyi.com/glossary/) · - **API**: [REST API Docs](https://unicodefyi.com/developers/) · [OpenAPI Spec](https://unicodefyi.com/api/openapi.json)

## Creative FYI Family

Part of the [FYIPedia](https://fyipedia.com) open-source developer tools ecosystem — design, typography, and character encoding.

| Package | PyPI | npm | Description |
|---------|------|-----|-------------|
| colorfyi | [PyPI](https://pypi.org/project/colorfyi/) | [npm](https://www.npmjs.com/package/@fyipedia/colorfyi) | Color conversion, WCAG contrast, harmonies -- [colorfyi.com](https://colorfyi.com/) |
| emojifyi | [PyPI](https://pypi.org/project/emojifyi/) | [npm](https://www.npmjs.com/package/emojifyi) | Emoji encoding & metadata for 3,953 emojis -- [emojifyi.com](https://emojifyi.com/) |
| symbolfyi | [PyPI](https://pypi.org/project/symbolfyi/) | [npm](https://www.npmjs.com/package/symbolfyi) | Symbol encoding in 11 formats -- [symbolfyi.com](https://symbolfyi.com/) |
| **unicodefyi** | [PyPI](https://pypi.org/project/unicodefyi/) | [npm](https://www.npmjs.com/package/unicodefyi) | **Unicode lookup with 17 encodings -- [unicodefyi.com](https://unicodefyi.com/)** |
| fontfyi | [PyPI](https://pypi.org/project/fontfyi/) | [npm](https://www.npmjs.com/package/fontfyi) | Google Fonts metadata & CSS -- [fontfyi.com](https://fontfyi.com/) |

## License

MIT
