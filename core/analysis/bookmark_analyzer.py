"""
Bookmark Analyzer
=================

Responsável por analisar bookmarks extraídos
e gerar estatísticas úteis.
"""

from collections import Counter
from typing import TypedDict
from urllib.parse import ParseResult, urlparse

from core.parser.bookmark_parser import Bookmark


class AnalysisResult(TypedDict):
    """
    Estrutura do resultado da análise.
    """

    total_bookmarks: int
    unique_domains: int
    top_domains: dict[str, int]
    duplicate_urls: list[str]


class BookmarkAnalyzer:
    """
    Classe responsável por analisar bookmarks.
    """

    def analyze(self, bookmarks: list[Bookmark]) -> AnalysisResult:
        """
        Analisa os bookmarks.

        Args:
            bookmarks: Lista de bookmarks.

        Returns:
            Estatísticas analisadas.
        """

        domains: list[str] = self._extract_domains(bookmarks)

        domain_counter: Counter[str] = Counter(domains)

        duplicate_urls: list[str] = self._find_duplicates(bookmarks)

        return {
            "total_bookmarks": len(bookmarks),
            "unique_domains": len(domain_counter),
            "top_domains": dict(domain_counter.most_common(20)),
            "duplicate_urls": duplicate_urls,
        }

    def _extract_domains(self, bookmarks: list[Bookmark]) -> list[str]:
        """
        Extrai domínios das URLs.
        """

        domains: list[str] = []

        for b in bookmarks:

            if not b["url"]:
                continue

            parsed: ParseResult = urlparse(b["url"])

            if parsed.netloc:
                domains.append(parsed.netloc)

        return domains

    def _find_duplicates(self, bookmarks: list[Bookmark]) -> list[str]:
        """
        Encontra URLs duplicadas.
        """

        urls: list[str] = [b["url"] for b in bookmarks if b["url"] is not None]

        counter: Counter[str] = Counter(urls)

        duplicates: list[str] = [url for url, count in counter.items() if count > 1]

        return duplicates
