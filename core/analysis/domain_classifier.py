"""
Domain Classifier
=================

Responsável por classificar bookmarks
com base no domínio da URL.
"""

from urllib.parse import ParseResult, urlparse
from typing import TypedDict

from core.parser.bookmark_parser import Bookmark


class DomainStats(TypedDict):
    """
    Estatísticas por categoria.
    """

    category: str
    count: int


class DomainClassifier:
    """
    Classifica URLs em categorias.
    """

    CATEGORY_MAP: dict[str, str] = {
        "github.com": "DEV",
        "gitlab.com": "DEV",
        "stackoverflow.com": "DEV",
        "youtube.com": "VIDEO",
        "youtu.be": "VIDEO",
        "vimeo.com": "VIDEO",
        "openai.com": "AI",
        "huggingface.co": "AI",
        "anthropic.com": "AI",
        "twitter.com": "SOCIAL",
        "x.com": "SOCIAL",
        "reddit.com": "SOCIAL",
        "nytimes.com": "NEWS",
        "medium.com": "NEWS",
        "notion.so": "TOOLS",
        "figma.com": "TOOLS",
    }

    def classify(self, bookmarks: list[Bookmark]) -> dict[str, int]:
        """
        Classifica bookmarks por categoria.

        Args:
            bookmarks: lista de bookmarks

        Returns:
            Contagem por categoria
        """

        stats: dict[str, int] = {}

        for bookmark in bookmarks:

            url: str | None = bookmark.get("url")

            if not url:
                continue

            domain: str = self._extract_domain(url)

            category: str = self.CATEGORY_MAP.get(domain, "UNKNOWN")

            stats[category] = stats.get(category, 0) + 1

        return stats

    def _extract_domain(self, url: str) -> str:
        """
        Extrai domínio da URL.
        """

        parsed: ParseResult = urlparse(url)

        domain: str = parsed.netloc.lower()

        if domain.startswith("www."):
            domain = domain[4:]

        return domain
