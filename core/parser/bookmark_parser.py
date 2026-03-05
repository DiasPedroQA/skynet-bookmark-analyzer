"""
Bookmark HTML Parser
====================

Responsável por ler arquivos HTML exportados
de navegadores e extrair bookmarks estruturados.
"""

from pathlib import Path
from typing import Optional, TypedDict, List

from typing import cast
from bs4 import BeautifulSoup
from bs4.element import Tag


class Bookmark(TypedDict):
    """
    Estrutura de dados de um bookmark extraído do HTML.
    """

    title: str
    url: Optional[str]
    domain: Optional[str]
    category: Optional[str]
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

    def parse(self) -> List[Bookmark]:
        """
        Realiza o parsing do arquivo HTML.

        Returns:
            Lista de bookmarks estruturados.
        """
        html_content: str = self.file_path.read_text(encoding="utf-8")
        soup = BeautifulSoup(html_content, "html.parser")
        bookmarks: List[Bookmark] = []

        for link in soup.find_all("a"):
            # Pega valores usando get() e garante que sejam strings ou None

            title: str = str(link.get_text(strip=True))  # sempre string
            url: Optional[str] = cast(Optional[str], link.get("href"))
            add_date: Optional[str] = cast(Optional[str], link.get("add_date"))
            # title: str = link.get_text(strip=True) or ""
            # url: Optional[str] = link.get("href")
            # add_date: Optional[str] = link.get("add_date")
            folder: Optional[str] = self._get_folder(link)

            # domain e category podem ser definidos aqui se quiser classificar
            domain: Optional[str] = None
            category: Optional[str] = None

            bookmark: Bookmark = {
                "title": title,
                "url": url,
                "domain": domain,
                "category": category,
                "add_date": add_date,
                "folder": folder,
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
        parent: Optional[Tag] = element.find_parent("dl")
        if parent:
            header: Optional[Tag] = parent.find_previous("h3")
            if header:
                return header.get_text(strip=True)
        return None
