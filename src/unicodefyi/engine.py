"""Unicode character computation engine — stateless, <1ms per call.

Computes 17 encoding representations and full Unicode properties for any
character. Uses stdlib ``unicodedata`` for core properties; ``fontTools``
(optional) for Unicode block and script data.

Zero required dependencies. Install ``fonttools`` for block/script info::

    pip install unicodefyi[full]
"""

from __future__ import annotations

import unicodedata
from typing import NamedTuple
from urllib.parse import quote

# Try fontTools for block/script (optional dependency)
try:
    from fontTools.unicodedata import block as ft_block  # type: ignore[import-untyped]
    from fontTools.unicodedata import script as ft_script

    _HAS_FONTTOOLS = True
except ImportError:
    _HAS_FONTTOOLS = False


# ─── Unicode general category names (ISO 15924 / UAX #44) ──────────────────

GENERAL_CATEGORY_NAMES: dict[str, str] = {
    "Lu": "Uppercase Letter",
    "Ll": "Lowercase Letter",
    "Lt": "Titlecase Letter",
    "Lm": "Modifier Letter",
    "Lo": "Other Letter",
    "Mn": "Nonspacing Mark",
    "Mc": "Spacing Mark",
    "Me": "Enclosing Mark",
    "Nd": "Decimal Number",
    "Nl": "Letter Number",
    "No": "Other Number",
    "Pc": "Connector Punctuation",
    "Pd": "Dash Punctuation",
    "Ps": "Open Punctuation",
    "Pe": "Close Punctuation",
    "Pi": "Initial Punctuation",
    "Pf": "Final Punctuation",
    "Po": "Other Punctuation",
    "Sm": "Math Symbol",
    "Sc": "Currency Symbol",
    "Sk": "Modifier Symbol",
    "So": "Other Symbol",
    "Zs": "Space Separator",
    "Zl": "Line Separator",
    "Zp": "Paragraph Separator",
    "Cc": "Control",
    "Cf": "Format",
    "Cs": "Surrogate",
    "Co": "Private Use",
    "Cn": "Unassigned",
}


# ─── Script code to slug mappings ───────────────────────────────────────────

SCRIPT_CODE_TO_SLUG: dict[str, str] = {
    "Arab": "arabic",
    "Armn": "armenian",
    "Bali": "balinese",
    "Beng": "bengali",
    "Bopo": "bopomofo",
    "Brai": "braille",
    "Cans": "canadian-aboriginal",
    "Cher": "cherokee",
    "Copt": "coptic",
    "Cyrl": "cyrillic",
    "Deva": "devanagari",
    "Ethi": "ethiopic",
    "Geor": "georgian",
    "Goth": "gothic",
    "Grek": "greek",
    "Gujr": "gujarati",
    "Guru": "gurmukhi",
    "Hang": "hangul",
    "Hani": "han",
    "Hebr": "hebrew",
    "Hira": "hiragana",
    "Java": "javanese",
    "Kana": "katakana",
    "Khmr": "khmer",
    "Knda": "kannada",
    "Laoo": "lao",
    "Latn": "latin",
    "Mlym": "malayalam",
    "Mong": "mongolian",
    "Mymr": "myanmar",
    "Nkoo": "nko",
    "Ogam": "ogham",
    "Orya": "oriya",
    "Runr": "runic",
    "Sinh": "sinhala",
    "Syrc": "syriac",
    "Tale": "tai-le",
    "Taml": "tamil",
    "Telu": "telugu",
    "Tfng": "tifinagh",
    "Tglg": "tagalog",
    "Thaa": "thaana",
    "Thai": "thai",
    "Tibt": "tibetan",
    "Vaii": "vai",
    "Yiii": "yi",
    "Zinh": "inherited",
    "Zyyy": "common",
}


# ─── HTML5 named character references ───────────────────────────────────────

HTML_ENTITIES: dict[int, str] = {
    0x0026: "&amp;",
    0x003C: "&lt;",
    0x003E: "&gt;",
    0x0022: "&quot;",
    0x0027: "&apos;",
    0x00A0: "&nbsp;",
    0x00A9: "&copy;",
    0x00AE: "&reg;",
    0x2122: "&trade;",
    0x00A3: "&pound;",
    0x00A5: "&yen;",
    0x20AC: "&euro;",
    0x00B0: "&deg;",
    0x00B1: "&plusmn;",
    0x00B5: "&micro;",
    0x00B7: "&middot;",
    0x00D7: "&times;",
    0x00F7: "&divide;",
    0x2013: "&ndash;",
    0x2014: "&mdash;",
    0x2018: "&lsquo;",
    0x2019: "&rsquo;",
    0x201C: "&ldquo;",
    0x201D: "&rdquo;",
    0x2020: "&dagger;",
    0x2021: "&Dagger;",
    0x2022: "&bull;",
    0x2026: "&hellip;",
    0x2032: "&prime;",
    0x2033: "&Prime;",
    0x2039: "&lsaquo;",
    0x203A: "&rsaquo;",
    0x2190: "&larr;",
    0x2191: "&uarr;",
    0x2192: "&rarr;",
    0x2193: "&darr;",
    0x2194: "&harr;",
    0x21B5: "&crarr;",
    0x21D0: "&lArr;",
    0x21D1: "&uArr;",
    0x21D2: "&rArr;",
    0x21D3: "&dArr;",
    0x21D4: "&hArr;",
    0x2200: "&forall;",
    0x2202: "&part;",
    0x2203: "&exist;",
    0x2205: "&empty;",
    0x2207: "&nabla;",
    0x2208: "&isin;",
    0x2209: "&notin;",
    0x220B: "&ni;",
    0x220F: "&prod;",
    0x2211: "&sum;",
    0x2212: "&minus;",
    0x221A: "&radic;",
    0x221E: "&infin;",
    0x2220: "&ang;",
    0x2227: "&and;",
    0x2228: "&or;",
    0x2229: "&cap;",
    0x222A: "&cup;",
    0x222B: "&int;",
    0x2234: "&there4;",
    0x223C: "&sim;",
    0x2245: "&cong;",
    0x2248: "&asymp;",
    0x2260: "&ne;",
    0x2261: "&equiv;",
    0x2264: "&le;",
    0x2265: "&ge;",
    0x2282: "&sub;",
    0x2283: "&sup;",
    0x2284: "&nsub;",
    0x2286: "&sube;",
    0x2287: "&supe;",
    0x2295: "&oplus;",
    0x2297: "&otimes;",
    0x22A5: "&perp;",
    0x22C5: "&sdot;",
    0x2308: "&lceil;",
    0x2309: "&rceil;",
    0x230A: "&lfloor;",
    0x230B: "&rfloor;",
    0x25CA: "&loz;",
    0x2660: "&spades;",
    0x2663: "&clubs;",
    0x2665: "&hearts;",
    0x2666: "&diams;",
    0x2713: "&check;",
    0x2717: "&cross;",
}

# Reverse mapping: entity string → character
HTML_ENTITY_TO_CHAR: dict[str, str] = {v: chr(k) for k, v in HTML_ENTITIES.items()}


# ─── Data types ─────────────────────────────────────────────────────────────


class EncodingInfo(NamedTuple):
    """17 encoding representations for a character."""

    unicode: str
    decimal: str
    html_decimal: str
    html_hex: str
    html_entity: str
    css: str
    javascript: str
    python: str
    java: str
    go: str
    ruby: str
    rust: str
    c_cpp: str
    url_encoded: str
    utf8_bytes: str
    utf16be_bytes: str
    utf32be_bytes: str


class CharInfo(NamedTuple):
    """Full Unicode properties + encodings for a character."""

    codepoint: int
    character: str
    name: str
    category: str
    category_name: str
    block: str
    block_slug: str
    script: str
    script_slug: str
    bidirectional: str
    combining: int
    mirrored: bool
    decomposition: str
    encodings: EncodingInfo


# ─── Core functions ─────────────────────────────────────────────────────────


def _slugify(name: str) -> str:
    """Convert block/script name to URL slug."""
    return name.lower().replace(" ", "-").replace("_", "-")


def get_encodings(char: str) -> EncodingInfo:
    """Compute 17 encoding representations for a single character.

    >>> enc = get_encodings("✓")
    >>> enc.unicode
    'U+2713'
    >>> enc.html_entity
    '&check;'
    >>> enc.utf8_bytes
    'e2 9c 93'
    """
    cp = ord(char)

    # Python/Java/Go/C have different escape formats for BMP vs supplementary
    if cp <= 0xFFFF:
        python_repr = f"\\u{cp:04x}"
        java_repr = f"\\u{cp:04X}"
        go_repr = f"\\u{cp:04X}"
        c_repr = f"\\u{cp:04x}"
    else:
        python_repr = f"\\U{cp:08x}"
        high = 0xD800 + ((cp - 0x10000) >> 10)
        low = 0xDC00 + ((cp - 0x10000) & 0x3FF)
        java_repr = f"\\u{high:04X}\\u{low:04X}"
        go_repr = f"\\U{cp:08X}"
        c_repr = f"\\U{cp:08x}"

    return EncodingInfo(
        unicode=f"U+{cp:04X}",
        decimal=str(cp),
        html_decimal=f"&#{cp};",
        html_hex=f"&#x{cp:X};",
        html_entity=HTML_ENTITIES.get(cp, ""),
        css=f"\\{cp:04X}",
        javascript=f"\\u{{{cp:X}}}",
        python=python_repr,
        java=java_repr,
        go=go_repr,
        ruby=f"\\u{{{cp:X}}}",
        rust=f"\\u{{{cp:X}}}",
        c_cpp=c_repr,
        url_encoded=quote(char),
        utf8_bytes=char.encode("utf-8").hex(" "),
        utf16be_bytes=char.encode("utf-16-be").hex(" "),
        utf32be_bytes=char.encode("utf-32-be").hex(" "),
    )


def get_char_info(codepoint: int) -> CharInfo | None:
    """Compute full character info from a codepoint.

    Returns ``None`` if the codepoint is invalid, unassigned, or a control character.

    >>> info = get_char_info(0x2713)
    >>> info.name if info else None
    'CHECK MARK'
    >>> info.block if info else None  # requires fonttools
    'Dingbats'
    """
    if codepoint < 0 or codepoint > 0x10FFFF:
        return None
    try:
        char = chr(codepoint)
    except (ValueError, OverflowError):
        return None

    name = unicodedata.name(char, None)
    if name is None:
        return None

    category = unicodedata.category(char)

    if _HAS_FONTTOOLS:
        block_name = ft_block(codepoint)
        script_code = ft_script(codepoint)
    else:
        block_name = ""
        script_code = ""

    script_slug = SCRIPT_CODE_TO_SLUG.get(script_code, _slugify(script_code))

    return CharInfo(
        codepoint=codepoint,
        character=char,
        name=name,
        category=category,
        category_name=GENERAL_CATEGORY_NAMES.get(category, category),
        block=block_name,
        block_slug=_slugify(block_name),
        script=script_code,
        script_slug=script_slug,
        bidirectional=unicodedata.bidirectional(char),
        combining=unicodedata.combining(char),
        mirrored=bool(unicodedata.mirrored(char)),
        decomposition=unicodedata.decomposition(char),
        encodings=get_encodings(char),
    )


def get_category_name(category_code: str) -> str:
    """Get the full name for a Unicode general category code.

    >>> get_category_name("Sm")
    'Math Symbol'
    """
    return GENERAL_CATEGORY_NAMES.get(category_code, category_code)


def lookup_html_entity(entity: str) -> str | None:
    """Look up the character for an HTML entity string.

    >>> lookup_html_entity("&amp;")
    '&'
    >>> lookup_html_entity("&hearts;")
    '\u2665'
    """
    return HTML_ENTITY_TO_CHAR.get(entity)


def search(query: str, limit: int = 50) -> list[CharInfo]:
    """Search characters by name substring.

    Performs a linear scan of common Unicode ranges (BMP).
    Returns up to ``limit`` results.

    >>> results = search("CHECK MARK")
    >>> len(results) > 0
    True
    >>> results[0].name
    'CHECK MARK'
    """
    query_upper = query.upper()
    results: list[CharInfo] = []

    search_ranges = [
        (0x0020, 0x007F),  # Basic Latin
        (0x00A0, 0x00FF),  # Latin-1 Supplement
        (0x0100, 0x024F),  # Latin Extended-A/B
        (0x0370, 0x03FF),  # Greek and Coptic
        (0x0400, 0x04FF),  # Cyrillic
        (0x2000, 0x206F),  # General Punctuation
        (0x2070, 0x209F),  # Superscripts and Subscripts
        (0x20A0, 0x20CF),  # Currency Symbols
        (0x2100, 0x214F),  # Letterlike Symbols
        (0x2150, 0x218F),  # Number Forms
        (0x2190, 0x21FF),  # Arrows
        (0x2200, 0x22FF),  # Mathematical Operators
        (0x2300, 0x23FF),  # Miscellaneous Technical
        (0x2500, 0x257F),  # Box Drawing
        (0x2580, 0x259F),  # Block Elements
        (0x25A0, 0x25FF),  # Geometric Shapes
        (0x2600, 0x26FF),  # Miscellaneous Symbols
        (0x2700, 0x27BF),  # Dingbats
        (0x2900, 0x297F),  # Supplemental Arrows-B
        (0x2B00, 0x2BFF),  # Miscellaneous Symbols and Arrows
    ]

    for start, end in search_ranges:
        if len(results) >= limit:
            break
        for cp in range(start, end + 1):
            if len(results) >= limit:
                break
            try:
                name = unicodedata.name(chr(cp), None)
            except (ValueError, OverflowError):
                continue
            if name and query_upper in name:
                info = get_char_info(cp)
                if info:
                    results.append(info)

    return results
