"""Tests for unicodefyi.api -- HTTP client for unicodefyi.com."""

from __future__ import annotations

from unicodefyi.api import UnicodeFYI


class TestUnicodeFYIClient:
    """Verify the client initializes and has all expected methods."""

    def test_init_default(self) -> None:
        client = UnicodeFYI()
        assert str(client._client.base_url) == "https://unicodefyi.com/api/"
        client.close()

    def test_init_custom_url(self) -> None:
        client = UnicodeFYI(base_url="http://localhost:8000/api", timeout=5.0)
        assert "localhost" in str(client._client.base_url)
        client.close()

    def test_context_manager(self) -> None:
        with UnicodeFYI() as client:
            assert client is not None

    def test_has_all_methods(self) -> None:
        client = UnicodeFYI()
        methods = [
            "char",
            "encodings",
            "search",
            "blocks",
            "block",
            "scripts",
            "script",
            "collections",
            "collection",
            "confusables",
            "random",
        ]
        for method in methods:
            assert hasattr(client, method), f"Missing method: {method}"
            assert callable(getattr(client, method))
        client.close()
