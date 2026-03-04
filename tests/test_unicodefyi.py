"""Tests for unicodefyi package."""

from __future__ import annotations

from unicodefyi import (
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


# =============================================================================
# Encoding (17 formats)
# =============================================================================
class TestGetEncodings:
    def test_returns_encoding_info(self) -> None:
        enc = get_encodings("✓")
        assert isinstance(enc, EncodingInfo)

    def test_unicode_notation(self) -> None:
        assert get_encodings("✓").unicode == "U+2713"

    def test_decimal(self) -> None:
        assert get_encodings("✓").decimal == "10003"

    def test_html_decimal(self) -> None:
        assert get_encodings("✓").html_decimal == "&#10003;"

    def test_html_hex(self) -> None:
        assert get_encodings("✓").html_hex == "&#x2713;"

    def test_html_entity(self) -> None:
        assert get_encodings("✓").html_entity == "&check;"

    def test_html_entity_empty(self) -> None:
        assert get_encodings("A").html_entity == ""

    def test_css(self) -> None:
        assert get_encodings("✓").css == "\\2713"

    def test_javascript(self) -> None:
        assert get_encodings("✓").javascript == "\\u{2713}"

    def test_python_bmp(self) -> None:
        assert get_encodings("✓").python == "\\u2713"

    def test_python_supplementary(self) -> None:
        assert get_encodings("\U0001f600").python == "\\U0001f600"

    def test_java_bmp(self) -> None:
        assert get_encodings("✓").java == "\\u2713"

    def test_java_surrogate_pair(self) -> None:
        assert get_encodings("\U0001f600").java == "\\uD83D\\uDE00"

    def test_go_bmp(self) -> None:
        assert get_encodings("✓").go == "\\u2713"

    def test_go_supplementary(self) -> None:
        assert get_encodings("\U0001f600").go == "\\U0001F600"

    def test_ruby(self) -> None:
        assert get_encodings("✓").ruby == "\\u{2713}"

    def test_rust(self) -> None:
        assert get_encodings("✓").rust == "\\u{2713}"

    def test_c_cpp_bmp(self) -> None:
        assert get_encodings("✓").c_cpp == "\\u2713"

    def test_c_cpp_supplementary(self) -> None:
        assert get_encodings("\U0001f600").c_cpp == "\\U0001f600"

    def test_utf8_bytes(self) -> None:
        assert get_encodings("✓").utf8_bytes == "e2 9c 93"

    def test_utf16be_bytes(self) -> None:
        assert get_encodings("✓").utf16be_bytes == "27 13"

    def test_utf32be_bytes(self) -> None:
        assert get_encodings("✓").utf32be_bytes == "00 00 27 13"

    def test_url_encoded(self) -> None:
        assert get_encodings("✓").url_encoded == "%E2%9C%93"

    def test_ascii_character(self) -> None:
        enc = get_encodings("A")
        assert enc.unicode == "U+0041"
        assert enc.utf8_bytes == "41"
        assert enc.url_encoded == "A"
        assert enc.decimal == "65"


# =============================================================================
# Character info
# =============================================================================
class TestGetCharInfo:
    def test_returns_char_info(self) -> None:
        info = get_char_info(0x2713)
        assert info is not None
        assert isinstance(info, CharInfo)

    def test_basic_properties(self) -> None:
        info = get_char_info(0x2192)
        assert info is not None
        assert info.name == "RIGHTWARDS ARROW"
        assert info.codepoint == 0x2192
        assert info.character == "\u2192"
        assert info.category == "Sm"
        assert info.category_name == "Math Symbol"

    def test_block_with_fonttools(self) -> None:
        info = get_char_info(0x2192)
        assert info is not None
        assert info.block == "Arrows"
        assert info.block_slug == "arrows"

    def test_script_with_fonttools(self) -> None:
        info = get_char_info(0x0041)
        assert info is not None
        assert info.script == "Latn"
        assert info.script_slug == "latin"

    def test_script_slug_mapping(self) -> None:
        info = get_char_info(0x0410)  # Cyrillic A
        assert info is not None
        assert info.script == "Cyrl"
        assert info.script_slug == "cyrillic"

    def test_encodings_included(self) -> None:
        info = get_char_info(0x2713)
        assert info is not None
        assert isinstance(info.encodings, EncodingInfo)
        assert info.encodings.html_entity == "&check;"

    def test_none_for_control_chars(self) -> None:
        assert get_char_info(0x0000) is None

    def test_none_for_invalid_codepoint(self) -> None:
        assert get_char_info(-1) is None
        assert get_char_info(0x110000) is None

    def test_mirrored(self) -> None:
        info = get_char_info(0x0028)  # (
        assert info is not None
        assert info.mirrored is True

    def test_not_mirrored(self) -> None:
        info = get_char_info(0x0041)  # A
        assert info is not None
        assert info.mirrored is False

    def test_supplementary_plane(self) -> None:
        info = get_char_info(0x1F600)  # grinning face
        assert info is not None
        assert info.name == "GRINNING FACE"
        assert info.encodings.java == "\\uD83D\\uDE00"


# =============================================================================
# Category names
# =============================================================================
class TestGetCategoryName:
    def test_known_category(self) -> None:
        assert get_category_name("Sm") == "Math Symbol"
        assert get_category_name("Lu") == "Uppercase Letter"
        assert get_category_name("Cs") == "Surrogate"

    def test_unknown_category(self) -> None:
        assert get_category_name("Xx") == "Xx"


# =============================================================================
# HTML entities
# =============================================================================
class TestHTMLEntities:
    def test_lookup_entity(self) -> None:
        assert lookup_html_entity("&amp;") == "&"
        assert lookup_html_entity("&hearts;") == "\u2665"
        assert lookup_html_entity("&copy;") == "\u00a9"

    def test_lookup_not_found(self) -> None:
        assert lookup_html_entity("&nonexistent;") is None

    def test_entities_count(self) -> None:
        assert len(HTML_ENTITIES) == 90

    def test_reverse_mapping(self) -> None:
        assert len(HTML_ENTITY_TO_CHAR) == 90
        assert HTML_ENTITY_TO_CHAR["&euro;"] == "\u20ac"


# =============================================================================
# Search
# =============================================================================
class TestSearch:
    def test_search_returns_results(self) -> None:
        results = search("CHECK MARK")
        assert len(results) > 0
        names = [r.name for r in results]
        assert "CHECK MARK" in names

    def test_search_case_insensitive(self) -> None:
        results = search("check mark")
        assert len(results) > 0

    def test_search_limit(self) -> None:
        results = search("LATIN", limit=5)
        assert len(results) <= 5

    def test_search_no_results(self) -> None:
        results = search("XYZNONEXISTENT")
        assert len(results) == 0

    def test_search_arrows(self) -> None:
        results = search("ARROW")
        assert len(results) > 5
        names = [r.name for r in results]
        assert "RIGHTWARDS ARROW" in names


# =============================================================================
# Data constants
# =============================================================================
class TestConstants:
    def test_general_categories(self) -> None:
        assert len(GENERAL_CATEGORY_NAMES) == 30
        assert "Lu" in GENERAL_CATEGORY_NAMES
        assert "Cs" in GENERAL_CATEGORY_NAMES
        assert "Cn" in GENERAL_CATEGORY_NAMES

    def test_script_code_to_slug(self) -> None:
        assert len(SCRIPT_CODE_TO_SLUG) == 48
        assert SCRIPT_CODE_TO_SLUG["Latn"] == "latin"
        assert SCRIPT_CODE_TO_SLUG["Cyrl"] == "cyrillic"
        assert SCRIPT_CODE_TO_SLUG["Hang"] == "hangul"


# =============================================================================
# Exports
# =============================================================================
class TestExports:
    def test_all_types(self) -> None:
        assert EncodingInfo is not None
        assert CharInfo is not None


# =============================================================================
# Edge cases
# =============================================================================
class TestEdgeCases:
    def test_ascii_encoding(self) -> None:
        enc = get_encodings("A")
        assert enc.unicode == "U+0041"
        assert enc.go == "\\u0041"
        assert enc.rust == "\\u{41}"
        assert enc.url_encoded == "A"

    def test_last_bmp(self) -> None:
        enc = get_encodings("\uffff")
        assert enc.unicode == "U+FFFF"

    def test_first_supplementary(self) -> None:
        enc = get_encodings("\U00010000")
        assert enc.unicode == "U+10000"
        assert "\\u" in enc.java  # surrogate pair

    def test_char_info_invalid_codepoint(self) -> None:
        assert get_char_info(0xFFFE) is None  # noncharacter

    def test_char_info_surrogate(self) -> None:
        assert get_char_info(0xD800) is None  # surrogate

    def test_search_empty_query(self) -> None:
        results = search("", limit=5)
        assert len(results) <= 5

    def test_search_case_insensitive(self) -> None:
        r1 = search("ARROW", limit=5)
        r2 = search("arrow", limit=5)
        assert len(r1) == len(r2)

    def test_category_unknown(self) -> None:
        name = get_category_name("XX")
        assert name == "XX"  # fallback

    def test_entity_not_found(self) -> None:
        result = lookup_html_entity("&nonexistent;")
        assert result is None
