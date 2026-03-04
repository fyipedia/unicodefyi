"""MCP server for unicodefyi -- Unicode tools for AI assistants.

Requires the ``mcp`` extra: ``pip install unicodefyi[mcp]``

Run as a standalone server::

    python -m unicodefyi.mcp_server

Or configure in ``claude_desktop_config.json``::

    {
        "mcpServers": {
            "unicodefyi": {
                "command": "python",
                "args": ["-m", "unicodefyi.mcp_server"]
            }
        }
    }
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("unicodefyi")


def _resolve_char(value: str) -> tuple[str, int]:
    """Resolve a codepoint string or character to (char, codepoint)."""
    if value.upper().startswith("U+"):
        cp = int(value[2:], 16)
        return chr(cp), cp
    if len(value) == 1:
        return value, ord(value)
    try:
        cp = int(value, 16)
        return chr(cp), cp
    except ValueError:
        pass
    return value[0], ord(value[0])


@mcp.tool()
def char_info(codepoint_or_char: str) -> str:
    """Get full Unicode character info including name, category, block, and script.

    Accepts U+hex notation (e.g. "U+2713"), a raw character, or a hex codepoint.

    Args:
        codepoint_or_char: Codepoint or character (e.g. "U+2713", "A", "2713").
    """
    from unicodefyi import get_char_info

    _char, cp = _resolve_char(codepoint_or_char)
    ci = get_char_info(cp)

    if ci is None:
        return f"No info found for U+{cp:04X}"

    lines = [
        f"## {ci.character}  U+{cp:04X}  {ci.name}",
        "",
        "| Property | Value |",
        "|----------|-------|",
        f"| Character | {ci.character} |",
        f"| Codepoint | `U+{cp:04X}` |",
        f"| Name | {ci.name} |",
        f"| Category | {ci.category} ({ci.category_name}) |",
    ]
    if ci.block:
        lines.append(f"| Block | {ci.block} |")
    if ci.script:
        lines.append(f"| Script | {ci.script} |")
    lines.extend(
        [
            f"| Bidirectional | {ci.bidirectional} |",
            f"| Combining | {ci.combining} |",
            f"| Mirrored | {'Yes' if ci.mirrored else 'No'} |",
        ]
    )
    if ci.decomposition:
        lines.append(f"| Decomposition | `{ci.decomposition}` |")

    return "\n".join(lines)


@mcp.tool()
def char_encode(codepoint_or_char: str) -> str:
    """Get all 17 encoding representations for a Unicode character.

    Returns Unicode, HTML, CSS, JavaScript, Python, Java, Go, Ruby, Rust,
    C/C++, URL, UTF-8, UTF-16, and UTF-32 encodings.

    Args:
        codepoint_or_char: Codepoint or character (e.g. "U+2713", "A").
    """
    from unicodefyi import get_encodings

    char, cp = _resolve_char(codepoint_or_char)
    enc = get_encodings(char)

    return "\n".join(
        [
            f"## Encodings for {char}  (U+{cp:04X})",
            "",
            "| Format | Value |",
            "|--------|-------|",
            f"| Unicode | `{enc.unicode}` |",
            f"| Decimal | `{enc.decimal}` |",
            f"| HTML Decimal | `{enc.html_decimal}` |",
            f"| HTML Hex | `{enc.html_hex}` |",
            f"| HTML Entity | `{enc.html_entity}`{' (none)' if not enc.html_entity else ''} |",
            f"| CSS | `{enc.css}` |",
            f"| JavaScript | `{enc.javascript}` |",
            f"| Python | `{enc.python}` |",
            f"| Java | `{enc.java}` |",
            f"| Go | `{enc.go}` |",
            f"| Ruby | `{enc.ruby}` |",
            f"| Rust | `{enc.rust}` |",
            f"| C/C++ | `{enc.c_cpp}` |",
            f"| URL Encoded | `{enc.url_encoded}` |",
            f"| UTF-8 Bytes | `{enc.utf8_bytes}` |",
            f"| UTF-16BE Bytes | `{enc.utf16be_bytes}` |",
            f"| UTF-32BE Bytes | `{enc.utf32be_bytes}` |",
        ]
    )


@mcp.tool()
def unicode_search(query: str, limit: int = 10) -> str:
    """Search Unicode characters by name substring.

    Args:
        query: Name substring to search for (e.g. "check mark", "arrow").
        limit: Maximum number of results (default 10).
    """
    from unicodefyi import search

    results = search(query, limit=limit)

    if not results:
        return f'No characters found for "{query}".'

    lines = [
        f'## Search: "{query}" ({len(results)} results)',
        "",
        "| Char | Codepoint | Name | Category |",
        "|------|-----------|------|----------|",
    ]
    for r in results:
        lines.append(f"| {r.character} | `U+{r.codepoint:04X}` | {r.name} | {r.category_name} |")

    return "\n".join(lines)


@mcp.tool()
def html_entity_lookup(entity: str) -> str:
    """Look up the character for an HTML named entity.

    Args:
        entity: HTML entity string (e.g. "&amp;", "&hearts;", "&euro;").
    """
    from unicodefyi import lookup_html_entity

    result = lookup_html_entity(entity)
    if result is None:
        return f"Entity not found: {entity}"

    cp = ord(result)
    return f"{entity} = {result}  (U+{cp:04X}, decimal {cp})"


def main() -> None:
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
