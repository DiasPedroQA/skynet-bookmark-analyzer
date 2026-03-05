"""
Bookmark HTML Parser
====================

Responsável por ler arquivos HTML exportados
de navegadores e extrair bookmarks estruturados.
"""

from pathlib import Path
from typing import Optional, TypedDict

from bs4 import BeautifulSoup
from bs4.element import AttributeValueList, Tag


class Bookmark(TypedDict):
    """
    Estrutura de dados de um bookmark extraído do HTML.
    """

    title: str
    url: Optional[str]
    add_date: Optional[str]
    folder: Optional[str]


class BookmarkParser:
    """
    Parser responsável por extrair bookmarks de um arquivo HTML.
    """

    def __init__(self, file_path: str) -> None:
        """
        Inicializa o parser.

        Args:
            file_path: Caminho para o arquivo HTML.
        """

        self.file_path = Path(file_path)

    def parse(self) -> list[Bookmark]:
        """
        Realiza o parsing do arquivo HTML.

        Returns:
            Lista de bookmarks estruturados.
        """

        html_content: str = self.file_path.read_text(encoding="utf-8")

        soup = BeautifulSoup(html_content, "html.parser")

        bookmarks: list[Bookmark] = []

        for link in soup.find_all("a"):

            url: str | AttributeValueList | None = link.get("href")
            add_date: str | AttributeValueList | None = link.get("add_date")

            bookmark: Bookmark = {
                "title": link.get_text(strip=True),
                "url": str(url) if url else None,
                "add_date": str(add_date) if add_date else None,
                "folder": self._get_folder(link),
            }

            bookmarks.append(bookmark)

        return bookmarks

    def _get_folder(self, element: Tag) -> Optional[str]:
        """
        Tenta descobrir em qual pasta o bookmark está.

        Args:
            element: Tag do link.

        Returns:
            Nome da pasta ou None.
        """

        parent: Tag | None = element.find_parent("dl")

        if parent:
            header: Tag | None = parent.find_previous("h3")
            if header:
                return header.get_text(strip=True)

        return None
