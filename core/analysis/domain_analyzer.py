"""
Domain Analyzer
===============

Responsável por gerar estatísticas
de domínios presentes nos bookmarks.
"""

from urllib.parse import ParseResult, urlparse
from collections import Counter
from typing import TypedDict

from core.parser.bookmark_parser import Bookmark


class DomainResult(TypedDict):
    """
    Estrutura de estatísticas de domínios.
    """

    domain: str
    count: int


class DomainAnalyzer:
    """
    Analisa domínios de bookmarks.
    """

    def analyze(self, bookmarks: list[Bookmark]) -> list[DomainResult]:
        """
        Conta frequência de domínios.

        Args:
            bookmarks: lista de bookmarks

        Returns:
            lista ordenada de domínios mais frequentes
        """

        domains: list[str] = []

        for bookmark in bookmarks:

            url: str | None = bookmark.get("url")

            if not url:
                continue

            domain: str = self._extract_domain(url)

            domains.append(domain)

        counter: Counter[str] = Counter(domains)

        results: list[DomainResult] = [
            {"domain": domain, "count": count}
            for domain, count in counter.most_common(20)
        ]

        return results

    def _extract_domain(self, url: str) -> str:
        """
        Extrai domínio da URL.
        """

        parsed: ParseResult = urlparse(url)

        domain: str = parsed.netloc.lower()

        if domain.startswith("www."):
            domain = domain[4:]

        return domain
