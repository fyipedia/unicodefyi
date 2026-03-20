"""HTTP API client for unicodefyi.com REST endpoints.

Requires the ``api`` extra: ``pip install unicodefyi[api]``

Usage::

    from unicodefyi.api import UnicodeFYI

    with UnicodeFYI() as api:
        items = api.list_characters()
        detail = api.get_character("example-slug")
        results = api.search("query")
"""

from __future__ import annotations

from typing import Any

import httpx


class UnicodeFYI:
    """API client for the unicodefyi.com REST API.

    Provides typed access to all unicodefyi.com endpoints including
    list, detail, and search operations.

    Args:
        base_url: API base URL. Defaults to ``https://unicodefyi.com``.
        timeout: Request timeout in seconds. Defaults to ``10.0``.
    """

    def __init__(
        self,
        base_url: str = "https://unicodefyi.com",
        timeout: float = 10.0,
    ) -> None:
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    def _get(self, path: str, **params: Any) -> dict[str, Any]:
        resp = self._client.get(
            path,
            params={k: v for k, v in params.items() if v is not None},
        )
        resp.raise_for_status()
        result: dict[str, Any] = resp.json()
        return result

    # -- Endpoints -----------------------------------------------------------

    def list_characters(self, **params: Any) -> dict[str, Any]:
        """List all characters."""
        return self._get("/api/v1/characters/", **params)

    def get_character(self, slug: str) -> dict[str, Any]:
        """Get character by slug."""
        return self._get(f"/api/v1/characters/" + slug + "/")

    def list_collections(self, **params: Any) -> dict[str, Any]:
        """List all collections."""
        return self._get("/api/v1/collections/", **params)

    def get_collection(self, slug: str) -> dict[str, Any]:
        """Get collection by slug."""
        return self._get(f"/api/v1/collections/" + slug + "/")

    def list_faqs(self, **params: Any) -> dict[str, Any]:
        """List all faqs."""
        return self._get("/api/v1/faqs/", **params)

    def get_faq(self, slug: str) -> dict[str, Any]:
        """Get faq by slug."""
        return self._get(f"/api/v1/faqs/" + slug + "/")

    def search(self, query: str, **params: Any) -> dict[str, Any]:
        """Search across all content."""
        return self._get(f"/api/v1/search/", q=query, **params)

    # -- Lifecycle -----------------------------------------------------------

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()

    def __enter__(self) -> UnicodeFYI:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
