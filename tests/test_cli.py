"""Tests for unicodefyi.cli -- command-line interface."""

from __future__ import annotations

from typer.testing import CliRunner

from unicodefyi.cli import app

runner = CliRunner()


class TestCLIInfo:
    def test_info_codepoint(self) -> None:
        result = runner.invoke(app, ["info", "U+2713"])
        assert result.exit_code == 0
        assert "CHECK MARK" in result.output

    def test_info_character(self) -> None:
        result = runner.invoke(app, ["info", "A"])
        assert result.exit_code == 0
        assert "LATIN CAPITAL LETTER A" in result.output

    def test_info_hex_string(self) -> None:
        result = runner.invoke(app, ["info", "2713"])
        assert result.exit_code == 0
        assert "CHECK MARK" in result.output

    def test_info_shows_category(self) -> None:
        result = runner.invoke(app, ["info", "U+2713"])
        assert result.exit_code == 0
        assert "Other Symbol" in result.output

    def test_info_invalid(self) -> None:
        result = runner.invoke(app, ["info", "U+FFFE"])
        assert result.exit_code == 1
        assert "No info" in result.output


class TestCLIEncode:
    def test_encode_codepoint(self) -> None:
        result = runner.invoke(app, ["encode", "U+2713"])
        assert result.exit_code == 0
        assert "U+2713" in result.output
        assert "e2 9c 93" in result.output

    def test_encode_character(self) -> None:
        result = runner.invoke(app, ["encode", "A"])
        assert result.exit_code == 0
        assert "U+0041" in result.output

    def test_encode_shows_all_formats(self) -> None:
        result = runner.invoke(app, ["encode", "U+2713"])
        assert result.exit_code == 0
        assert "HTML Decimal" in result.output
        assert "JavaScript" in result.output
        assert "Python" in result.output
        assert "Rust" in result.output
        assert "UTF-8" in result.output


class TestCLISearch:
    def test_search_results(self) -> None:
        result = runner.invoke(app, ["search", "check mark"])
        assert result.exit_code == 0
        assert "CHECK MARK" in result.output

    def test_search_no_results(self) -> None:
        result = runner.invoke(app, ["search", "XYZNONEXISTENT"])
        assert result.exit_code == 0
        assert "No characters found" in result.output

    def test_search_with_limit(self) -> None:
        result = runner.invoke(app, ["search", "ARROW", "--limit", "3"])
        assert result.exit_code == 0
        assert "ARROW" in result.output


class TestCLIEntity:
    def test_entity_amp(self) -> None:
        result = runner.invoke(app, ["entity", "&amp;"])
        assert result.exit_code == 0
        assert "U+0026" in result.output

    def test_entity_hearts(self) -> None:
        result = runner.invoke(app, ["entity", "&hearts;"])
        assert result.exit_code == 0
        assert "U+2665" in result.output

    def test_entity_not_found(self) -> None:
        result = runner.invoke(app, ["entity", "&nonexistent;"])
        assert result.exit_code == 1
        assert "not found" in result.output


class TestCLINoArgs:
    def test_no_args_shows_help(self) -> None:
        result = runner.invoke(app, [])
        # Typer no_args_is_help=True returns exit code 0 or 2 depending on version
        assert result.exit_code in (0, 2)
        assert "Usage" in result.output or "unicodefyi" in result.output.lower()
