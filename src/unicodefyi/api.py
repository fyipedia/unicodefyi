"""HTTP API client for unicodefyi.com REST endpoints.

Requires the ``api`` extra: ``pip install unicodefyi[api]``

Usage::

    from unicodefyi.api import UnicodeFYI

    with UnicodeFYI() as api:
        info = api.char("2713")
        print(info["name"])  # CHECK MARK

        results = api.search("check mark")
        print(results)
"""

from __future__ import annotations

from typing import Any

import httpx


class UnicodeFYI:
    """API client for the unicodefyi.com REST API.

    Args:
        base_url: API base URL. Defaults to ``https://unicodefyi.com/api``.
        timeout: Request timeout in seconds. Defaults to ``10.0``.
    """

    def __init__(
        self,
        base_url: str = "https://unicodefyi.com/api",
        timeout: float = 10.0,
    ) -> None:
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    # -- HTTP helpers ----------------------------------------------------------

    def _get(self, path: str, **params: Any) -> dict[str, Any]:
        resp = self._client.get(path, params={k: v for k, v in params.items() if v is not None})
        resp.raise_for_status()
        result: dict[str, Any] = resp.json()
        return result

    # -- Endpoints -------------------------------------------------------------

    def char(self, hex_value: str) -> dict[str, Any]:
        """Get full character information.

        Args:
            hex_value: Hex codepoint (e.g. ``"2713"`` for CHECK MARK).

        Returns:
            Dict with name, category, block, script, encodings, and more.
        """
        return self._get(f"/char/{hex_value}/")

    def encodings(self, hex_value: str) -> dict[str, Any]:
        """Get all 17 encoding representations for a character.

        Args:
            hex_value: Hex codepoint (e.g. ``"2713"``).

        Returns:
            Dict with unicode, html, css, javascript, python, java, etc.
        """
        return self._get(f"/char/{hex_value}/encodings/")

    def search(self, query: str) -> dict[str, Any]:
        """Search Unicode characters by name.

        Args:
            query: Search term (e.g. ``"check mark"``, ``"arrow"``).
        """
        return self._get("/search/", q=query)

    def blocks(self) -> dict[str, Any]:
        """List all Unicode blocks."""
        return self._get("/blocks/")

    def block(self, slug: str) -> dict[str, Any]:
        """Get characters in a specific Unicode block.

        Args:
            slug: Block slug (e.g. ``"arrows"``, ``"basic-latin"``).
        """
        return self._get(f"/block/{slug}/")

    def scripts(self) -> dict[str, Any]:
        """List all Unicode scripts."""
        return self._get("/scripts/")

    def script(self, slug: str) -> dict[str, Any]:
        """Get characters in a specific Unicode script.

        Args:
            slug: Script slug (e.g. ``"latin"``, ``"cyrillic"``).
        """
        return self._get(f"/script/{slug}/")

    def collections(self) -> dict[str, Any]:
        """List all curated character collections."""
        return self._get("/collections/")

    def collection(self, slug: str) -> dict[str, Any]:
        """Get characters in a curated collection.

        Args:
            slug: Collection slug (e.g. ``"arrows"``, ``"math"``).
        """
        return self._get(f"/collection/{slug}/")

    def confusables(self, char: str) -> dict[str, Any]:
        """Find confusable (visually similar) characters.

        Args:
            char: Character to find confusables for.
        """
        return self._get("/confusables/", char=char)

    def random(self) -> dict[str, Any]:
        """Get a random Unicode character."""
        return self._get("/random/")

    # -- Context manager -------------------------------------------------------

    def close(self) -> None:
        """Close the underlying HTTP connection."""
        self._client.close()

    def __enter__(self) -> UnicodeFYI:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
