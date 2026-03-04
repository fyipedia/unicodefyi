"""Tests for unicodefyi.mcp_server -- MCP tools."""

from __future__ import annotations

from unicodefyi.mcp_server import (
    char_encode,
    char_info,
    html_entity_lookup,
    unicode_search,
)


class TestMCPCharInfo:
    def test_returns_markdown_table(self) -> None:
        result = char_info("U+2713")
        assert "CHECK MARK" in result
        assert "U+2713" in result
        assert "Other Symbol" in result

    def test_character_input(self) -> None:
        result = char_info("A")
        assert "LATIN CAPITAL LETTER A" in result
        assert "U+0041" in result

    def test_hex_input(self) -> None:
        result = char_info("2713")
        assert "CHECK MARK" in result

    def test_invalid_codepoint(self) -> None:
        result = char_info("U+FFFE")
        assert "No info" in result


class TestMCPCharEncode:
    def test_returns_all_encodings(self) -> None:
        result = char_encode("U+2713")
        assert "U+2713" in result
        assert "HTML Decimal" in result
        assert "JavaScript" in result
        assert "Python" in result
        assert "Rust" in result
        assert "UTF-8 Bytes" in result
        assert "e2 9c 93" in result

    def test_ascii_character(self) -> None:
        result = char_encode("A")
        assert "U+0041" in result

    def test_html_entity_present(self) -> None:
        result = char_encode("U+2713")
        assert "&check;" in result

    def test_no_entity(self) -> None:
        result = char_encode("A")
        assert "(none)" in result


class TestMCPUnicodeSearch:
    def test_search_results(self) -> None:
        result = unicode_search("check mark")
        assert "CHECK MARK" in result
        assert "U+2713" in result

    def test_search_no_results(self) -> None:
        result = unicode_search("XYZNONEXISTENT")
        assert "No characters found" in result

    def test_search_arrows(self) -> None:
        result = unicode_search("arrow", limit=5)
        assert "ARROW" in result


class TestMCPHTMLEntityLookup:
    def test_amp(self) -> None:
        result = html_entity_lookup("&amp;")
        assert "&" in result
        assert "U+0026" in result

    def test_hearts(self) -> None:
        result = html_entity_lookup("&hearts;")
        assert "U+2665" in result

    def test_not_found(self) -> None:
        result = html_entity_lookup("&nonexistent;")
        assert "not found" in result
