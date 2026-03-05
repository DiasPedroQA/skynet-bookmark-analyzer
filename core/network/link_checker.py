"""
Link Checker
============

Responsável por verificar o status HTTP
dos links encontrados nos bookmarks.
"""

import asyncio
from typing import TypedDict

import httpx

from core.parser.bookmark_parser import Bookmark


class LinkStatus(TypedDict):
    """
    Estrutura de resultado da verificação de um link.
    """

    url: str
    status: int | None


class LinkChecker:
    """
    Verifica status HTTP de links.
    """

    def __init__(self, max_connections: int = 20) -> None:
        self.max_connections: int = max_connections

    async def check_links(self, bookmarks: list[Bookmark]) -> list[LinkStatus]:
        """
        Verifica todos os links encontrados.
        """

        urls: list[str] = [
            b["url"]
            for b in bookmarks
            if b["url"] and b["url"].startswith(("http://", "https://"))
        ]

        total: int = len(urls)
        counter: int = 0

        semaphore: asyncio.Semaphore = asyncio.Semaphore(self.max_connections)

        timeout: httpx.Timeout = httpx.Timeout(10.0)

        async with httpx.AsyncClient(
            timeout=timeout,
            follow_redirects=True,
        ) as client:

            async def worker(url: str) -> LinkStatus:
                nonlocal counter

                result: LinkStatus = await self._check_one(client, url, semaphore)

                counter += 1
                print(f"Verificados {counter}/{total}", end="\r")

                return result

            tasks = [worker(url) for url in urls]

            results: list[LinkStatus] = await asyncio.gather(*tasks)

        print()

        return results

    async def _check_one(
        self,
        client: httpx.AsyncClient,
        url: str,
        semaphore: asyncio.Semaphore,
    ) -> LinkStatus:
        """
        Verifica um único link.
        """

        async with semaphore:

            try:

                response: httpx.Response = await client.get(url)

                return {
                    "url": url,
                    "status": response.status_code,
                }

            except httpx.HTTPError:

                return {
                    "url": url,
                    "status": None,
                }
