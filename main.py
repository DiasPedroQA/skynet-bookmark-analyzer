"""
SkyNet Bookmark Analyzer
Pipeline principal de análise de bookmarks com SQLite incremental e exportação JSON.
"""

from pathlib import Path
import sqlite3
from typing import List

from core.parser.bookmark_parser import BookmarkParser, Bookmark
from core.analysis.bookmark_analyzer import BookmarkAnalyzer, AnalysisResult
from core.exporters.json_exporter import JSONExporter

DB_PATH = Path("data/history.db")
OUTPUT_FILE = Path("output/bookmarks_analysis.json")


def init_db() -> None:
    """Cria as tabelas do banco de dados caso não existam."""
    conn: sqlite3.Connection = sqlite3.connect(DB_PATH)
    c: sqlite3.Cursor = conn.cursor()
    c.executescript(
        """
        CREATE TABLE IF NOT EXISTS bookmarks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url TEXT UNIQUE,
            domain TEXT,
            category TEXT,
            add_date TEXT,
            folder TEXT,
            last_checked TIMESTAMP,
            status TEXT
        );

        CREATE TABLE IF NOT EXISTS domains (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT UNIQUE,
            count INTEGER
        );

        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT UNIQUE,
            count INTEGER
        );

        CREATE TABLE IF NOT EXISTS links_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bookmark_id INTEGER,
            status TEXT,
            response_time REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (bookmark_id) REFERENCES bookmarks(id)
        );

        CREATE TABLE IF NOT EXISTS analysis_summary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total_bookmarks INTEGER,
            unique_domains INTEGER,
            duplicate_count INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """
    )
    conn.commit()
    conn.close()


def save_bookmarks(conn: sqlite3.Connection, bookmarks: List[Bookmark]) -> None:
    """Salva bookmarks no banco, ignorando duplicados por URL."""
    c: sqlite3.Cursor = conn.cursor()
    for bm in bookmarks:
        c.execute(
            """
            INSERT OR IGNORE INTO bookmarks (title, url, domain, category, add_date, folder)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                bm["title"],
                bm["url"],
                bm["domain"],
                bm["category"],
                bm["add_date"],
                bm["folder"],
            ),
        )
    conn.commit()


def save_summary(conn: sqlite3.Connection, analysis: AnalysisResult) -> None:
    """Salva o resumo da análise no banco."""
    c: sqlite3.Cursor = conn.cursor()
    c.execute(
        """
        INSERT INTO analysis_summary (total_bookmarks, unique_domains, duplicate_count)
        VALUES (?, ?, ?)
        """,
        (
            analysis["total_bookmarks"],
            analysis["unique_domains"],
            len(analysis["duplicate_urls"]),
        ),
    )
    conn.commit()


def main() -> None:
    """
    Executa pipeline completo:
    1. Lê bookmarks HTML
    2. Analisa e classifica domínios
    3. Salva histórico incremental no SQLite
    4. Exporta resultado em JSON
    """

    # Inicializa banco
    init_db()

    # Define arquivo de entrada
    input_file: Path = Path.home() / "Documents/bookmarks_3_5_26.html"
    print(f"📂 Lendo arquivo de bookmarks: {input_file}")
    parser = BookmarkParser(str(input_file))
    bookmarks: List[Bookmark] = parser.parse()
    print(f"✅ {len(bookmarks)} bookmarks carregados")

    # -------------------------
    # Análise
    # -------------------------
    analyzer = BookmarkAnalyzer()
    analysis: AnalysisResult = analyzer.analyze(bookmarks)
    print(f"Total bookmarks: {analysis['total_bookmarks']}")
    print(f"Domínios únicos: {analysis['unique_domains']}")
    print(f"Duplicados: {len(analysis['duplicate_urls'])}")

    # -------------------------
    # Salvando no SQLite
    # -------------------------
    conn: sqlite3.Connection = sqlite3.connect(DB_PATH)
    save_bookmarks(conn, bookmarks)
    save_summary(conn, analysis)
    conn.close()

    # -------------------------
    # Exportando JSON
    # -------------------------
    exporter = JSONExporter(str(OUTPUT_FILE))
    exporter.export(bookmarks)
    print(f"✅ JSON salvo em: {OUTPUT_FILE.resolve()}")


if __name__ == "__main__":
    main()
