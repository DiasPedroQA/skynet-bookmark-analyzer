"""
JSON Exporter
=============

Responsável por exportar bookmarks estruturados
para um arquivo JSON contendo também estatísticas.
"""

import json
from pathlib import Path
from typing import TypedDict

from core.parser.bookmark_parser import Bookmark


class BookmarkSummary(TypedDict):
    """
    Estrutura do resumo estatístico.
    """

    total_bookmarks: int


class ExportData(TypedDict):
    """
    Estrutura final exportada para JSON.
    """

    summary: BookmarkSummary
    bookmarks: list[Bookmark]


class JSONExporter:
    """
    Exportador responsável por gerar JSON estruturado.
    """

    def __init__(self, output_path: str) -> None:
        """
        Inicializa o exportador.

        Args:
            output_path: Caminho do arquivo JSON de saída.
        """

        self.output_path = Path(output_path)

    def export(self, bookmarks: list[Bookmark]) -> None:
        """
        Exporta bookmarks para JSON.

        Args:
            bookmarks: Lista de bookmarks extraídos.
        """

        data: ExportData = {
            "summary": {
                "total_bookmarks": len(bookmarks),
            },
            "bookmarks": bookmarks,
        }

        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
