"""Command-line interface for unicodefyi.

Requires the ``cli`` extra: ``pip install unicodefyi[cli]``

Usage::

    unicodefyi info U+2713                # Character info (CHECK MARK)
    unicodefyi info A                     # Character info (LATIN CAPITAL LETTER A)
    unicodefyi encode U+2713              # All 17 encodings
    unicodefyi search "check mark"        # Search by name
    unicodefyi entity "&amp;"             # HTML entity reverse lookup
"""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(
    name="unicodefyi",
    help=("Pure Python Unicode toolkit -- 17 encodings, character lookup, and search."),
    no_args_is_help=True,
)
console = Console()


def _resolve_char(value: str) -> tuple[str, int]:
    """Resolve a codepoint string or character to (char, codepoint)."""
    if value.upper().startswith("U+"):
        cp = int(value[2:], 16)
        return chr(cp), cp
    if len(value) == 1:
        return value, ord(value)
    # Try as hex
    try:
        cp = int(value, 16)
        return chr(cp), cp
    except ValueError:
        pass
    # Multi-char string, use first char
    return value[0], ord(value[0])


@app.command()
def info(
    value: str = typer.Argument(help='Codepoint or character (e.g. "U+2713", "A", "2713").'),
) -> None:
    """Show full Unicode character info."""
    from unicodefyi import get_char_info

    _char, cp = _resolve_char(value)
    ci = get_char_info(cp)

    if ci is None:
        console.print(f"[red]No info for U+{cp:04X}[/red]")
        raise typer.Exit(code=1)

    table = Table(title=f"{ci.character}  U+{cp:04X}  {ci.name}")
    table.add_column("Property", style="cyan", no_wrap=True)
    table.add_column("Value")

    table.add_row("Character", ci.character)
    table.add_row("Codepoint", f"U+{cp:04X}")
    table.add_row("Name", ci.name)
    table.add_row("Category", f"{ci.category} ({ci.category_name})")
    if ci.block:
        table.add_row("Block", ci.block)
    if ci.script:
        table.add_row("Script", ci.script)
    table.add_row("Bidirectional", ci.bidirectional)
    table.add_row("Combining", str(ci.combining))
    table.add_row("Mirrored", "Yes" if ci.mirrored else "No")
    if ci.decomposition:
        table.add_row("Decomposition", ci.decomposition)

    console.print(table)


@app.command()
def encode(
    value: str = typer.Argument(help='Codepoint or character (e.g. "U+2713", "A").'),
) -> None:
    """Show all 17 encoding representations for a character."""
    from unicodefyi import get_encodings

    char, cp = _resolve_char(value)
    enc = get_encodings(char)

    table = Table(title=f"Encodings for {char}  (U+{cp:04X})")
    table.add_column("Format", style="cyan", no_wrap=True)
    table.add_column("Value")

    table.add_row("Unicode", enc.unicode)
    table.add_row("Decimal", enc.decimal)
    table.add_row("HTML Decimal", enc.html_decimal)
    table.add_row("HTML Hex", enc.html_hex)
    table.add_row("HTML Entity", enc.html_entity or "(none)")
    table.add_row("CSS", enc.css)
    table.add_row("JavaScript", enc.javascript)
    table.add_row("Python", enc.python)
    table.add_row("Java", enc.java)
    table.add_row("Go", enc.go)
    table.add_row("Ruby", enc.ruby)
    table.add_row("Rust", enc.rust)
    table.add_row("C/C++", enc.c_cpp)
    table.add_row("URL Encoded", enc.url_encoded)
    table.add_row("UTF-8 Bytes", enc.utf8_bytes)
    table.add_row("UTF-16BE Bytes", enc.utf16be_bytes)
    table.add_row("UTF-32BE Bytes", enc.utf32be_bytes)

    console.print(table)


@app.command()
def search(
    query: str = typer.Argument(help="Search characters by name."),
    limit: int = typer.Option(20, help="Maximum number of results."),
) -> None:
    """Search Unicode characters by name substring."""
    from unicodefyi import search as _search

    results = _search(query, limit=limit)

    if not results:
        console.print("[yellow]No characters found.[/yellow]")
        raise typer.Exit()

    table = Table(title=f'Search: "{query}" ({len(results)} results)')
    table.add_column("Char", justify="center")
    table.add_column("Codepoint", style="cyan", no_wrap=True)
    table.add_column("Name")
    table.add_column("Category")

    for r in results:
        table.add_row(
            r.character,
            f"U+{r.codepoint:04X}",
            r.name,
            r.category_name,
        )

    console.print(table)


@app.command()
def entity(
    name: str = typer.Argument(help='HTML entity (e.g. "&amp;", "&hearts;").'),
) -> None:
    """Look up the character for an HTML entity."""
    from unicodefyi import lookup_html_entity

    result = lookup_html_entity(name)
    if result is None:
        console.print(f"[red]Entity not found: {name}[/red]")
        raise typer.Exit(code=1)

    cp = ord(result)
    console.print(f"{name} = {result}  (U+{cp:04X})")
