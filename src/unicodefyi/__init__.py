"""unicodefyi — Pure Python Unicode character toolkit.

Compute 17 encoding representations (Unicode, HTML, CSS, JavaScript,
Python, Java, Go, Ruby, Rust, C/C++, UTF-8, UTF-16, UTF-32, URL)
and full Unicode properties for any character.
Includes 92 HTML entity mappings and character search.

Zero required dependencies. Optional ``fonttools`` for block/script info.

Usage::

    from unicodefyi import get_encodings, get_char_info, search

    # Encode any character (17 formats)
    enc = get_encodings("✓")
    print(enc.unicode)        # U+2713
    print(enc.html_entity)    # &check;
    print(enc.go)             # \\u2713
    print(enc.rust)           # \\u{2713}
    print(enc.utf8_bytes)     # e2 9c 93

    # Full Unicode properties
    info = get_char_info(0x2713)
    print(info.name)          # CHECK MARK
    print(info.block)         # Dingbats (requires fonttools)
    print(info.category_name) # Other Symbol

    # Search characters
    results = search("arrow")
    for r in results[:5]:
        print(r.character, r.name)
"""

from unicodefyi.engine import (
    GENERAL_CATEGORY_NAMES,
    HTML_ENTITIES,
    HTML_ENTITY_TO_CHAR,
    SCRIPT_CODE_TO_SLUG,
    CharInfo,
    EncodingInfo,
    get_category_name,
    get_char_info,
    get_encodings,
    lookup_html_entity,
    search,
)

__version__ = "0.1.0"

__all__ = [
    # Data types
    "EncodingInfo",
    "CharInfo",
    # Core functions
    "get_encodings",
    "get_char_info",
    "get_category_name",
    "lookup_html_entity",
    "search",
    # Data
    "GENERAL_CATEGORY_NAMES",
    "SCRIPT_CODE_TO_SLUG",
    "HTML_ENTITIES",
    "HTML_ENTITY_TO_CHAR",
]
