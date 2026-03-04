---
name: unicode-tools
description: Look up Unicode characters, encode into 17 formats (UTF-8, UTF-16, UTF-32, HTML, CSS, JS, Python, Java, Go, Ruby, Rust, C++), search by name.
---

# Unicode Tools

Unicode character lookup, encoding, and search powered by [unicodefyi](https://unicodefyi.com/) -- a pure Python Unicode toolkit supporting 17 encoding formats with zero dependencies.

## Setup

Install the MCP server:

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

## Available Tools

| Tool | Description |
|------|-------------|
| `char_info` | Full character info (name, category, block, script) + encodings |
| `char_encode` | Encode any character into 17 formats (UTF-8/16/32, HTML, CSS, JS, Python, Java, Go, Ruby, Rust, C/C++, URL) |
| `unicode_search` | Search Unicode characters by name |
| `html_entity_lookup` | Reverse lookup for HTML entities |

## When to Use

- Looking up Unicode character properties and codepoints
- Encoding characters for any programming language (Python, JS, Java, Go, Ruby, Rust, C++)
- Finding characters by name (e.g., "check mark", "arrow", "Greek")
- Getting HTML/CSS/URL-encoded representations
- Resolving HTML entity names to characters

## Links

- [Unicode Search](https://unicodefyi.com/search/)
- [Unicode Blocks](https://unicodefyi.com/blocks/)
- [API Documentation](https://unicodefyi.com/developers/)
- [PyPI Package](https://pypi.org/project/unicodefyi/)
