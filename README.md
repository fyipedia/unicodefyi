# unicodefyi

[![PyPI](https://img.shields.io/pypi/v/unicodefyi)](https://pypi.org/project/unicodefyi/)
[![Python](https://img.shields.io/pypi/pyversions/unicodefyi)](https://pypi.org/project/unicodefyi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Pure Python Unicode character toolkit for developers. Compute [17 encoding representations](https://unicodefyi.com/developers/) (Unicode, HTML, CSS, JavaScript, Python, Java, Go, Ruby, Rust, C/C++, URL, UTF-8, UTF-16, UTF-32), look up full [Unicode properties](https://unicodefyi.com/block/) (name, category, block, script), resolve [92 HTML entities](https://unicodefyi.com/search/), and [search characters by name](https://unicodefyi.com/search/) -- all with zero dependencies.

> **Try the interactive tools at [unicodefyi.com](https://unicodefyi.com/)** -- [Unicode search](https://unicodefyi.com/search/), [Unicode blocks](https://unicodefyi.com/block/), [Unicode scripts](https://unicodefyi.com/script/), and [character collections](https://unicodefyi.com/collection/).

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

## FYIPedia Developer Tools

Part of the [FYIPedia](https://unicodefyi.com/) open-source developer tools ecosystem:

| Package | Description |
|---------|-------------|
| [colorfyi](https://colorfyi.com/) | [Hex to RGB converter](https://colorfyi.com/tools/converter/), [WCAG contrast checker](https://colorfyi.com/tools/contrast-checker/), [color harmonies](https://colorfyi.com/tools/palette-generator/) |
| [emojifyi](https://emojifyi.com/) | [Emoji encoding](https://emojifyi.com/developers/) & metadata for 3,781 Unicode emojis |
| [symbolfyi](https://symbolfyi.com/) | [Symbol encoder](https://symbolfyi.com/developers/) -- 11 encoding formats for any character |
| **unicodefyi** | [Unicode character lookup](https://unicodefyi.com/developers/) -- 17 encodings + character search |
| [fontfyi](https://fontfyi.com/) | [Google Fonts explorer](https://fontfyi.com/developers/) -- metadata, CSS helpers, font pairings |
| [distancefyi](https://pypi.org/project/distancefyi/) | Haversine distance, bearing, travel times -- [distancefyi.com](https://distancefyi.com/) |
| [timefyi](https://pypi.org/project/timefyi/) | Timezone operations, time differences -- [timefyi.com](https://timefyi.com/) |
| [namefyi](https://pypi.org/project/namefyi/) | Korean romanization, Five Elements -- [namefyi.com](https://namefyi.com/) |
| [unitfyi](https://pypi.org/project/unitfyi/) | Unit conversion, 200 units, 20 categories -- [unitfyi.com](https://unitfyi.com/) |
| [holidayfyi](https://pypi.org/project/holidayfyi/) | Holiday dates, Easter calculation -- [holidayfyi.com](https://holidayfyi.com/) |

## Links

- [Unicode Character Search](https://unicodefyi.com/search/) -- Search any Unicode character
- [Unicode Blocks](https://unicodefyi.com/block/) -- Browse all Unicode blocks
- [Unicode Scripts](https://unicodefyi.com/script/) -- Browse all Unicode scripts
- [Character Collections](https://unicodefyi.com/collection/) -- Curated character sets
- [REST API Documentation](https://unicodefyi.com/developers/) -- Free API with OpenAPI spec
- [Source Code](https://github.com/fyipedia/unicodefyi) -- MIT licensed

## License

MIT
