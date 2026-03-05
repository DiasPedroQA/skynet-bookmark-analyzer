"""
SkyNet Bookmark Analyzer - Prototype
====================================

Script principal responsável por executar
o pipeline completo de análise de bookmarks.
"""

from pathlib import Path
import asyncio

from core.analysis.bookmark_analyzer import AnalysisResult, BookmarkAnalyzer
from core.analysis.domain_analyzer import DomainAnalyzer
from core.analysis.domain_classifier import DomainClassifier
from core.exporters.json_exporter import JSONExporter
from core.network.link_checker import LinkChecker, LinkStatus
from core.parser.bookmark_parser import BookmarkParser, Bookmark


# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

INPUT_FILE: Path = Path.home() / "Documents/bookmarks_3_5_26.html"
OUTPUT_JSON: Path = Path("../output/bookmarks_analysis.json")


# ---------------------------------------------------------
# PIPELINE STEPS
# ---------------------------------------------------------


def parse_bookmarks() -> list[Bookmark]:
    """
    Lê e interpreta o arquivo HTML de bookmarks.
    """

    print("📂 Lendo arquivo de bookmarks...")

    parser = BookmarkParser(str(INPUT_FILE))
    bookmarks: list[Bookmark] = parser.parse()

    print(f"✅ {len(bookmarks)} bookmarks carregados")

    return bookmarks


def analyze_bookmarks(bookmarks: list[Bookmark]) -> AnalysisResult:
    """
    Executa análise estrutural dos bookmarks.
    """

    print("🔎 Analisando bookmarks...")

    analyzer = BookmarkAnalyzer()
    analysis = analyzer.analyze(bookmarks)

    print("📊 Estatísticas principais:")

    print("Total bookmarks:", analysis["total_bookmarks"])
    print("Domínios únicos:", analysis["unique_domains"])
    print("Duplicados:", len(analysis["duplicate_urls"]))

    return analysis


def analyze_domains(bookmarks: list[Bookmark]) -> None:
    """
    Mostra ranking dos domínios mais frequentes.
    """

    print("🌐 Analisando domínios...")

    domain_analyzer = DomainAnalyzer()
    top_domains = domain_analyzer.analyze(bookmarks)

    print("\n🏆 TOP DOMÍNIOS\n")

    for item in top_domains[:10]:
        print(f"{item['domain']} → {item['count']}")


def classify_domains(bookmarks: list[Bookmark]) -> dict[str, int]:
    """
    Classifica domínios por categoria.
    """

    print("🧠 Classificando domínios...")

    classifier = DomainClassifier()
    domain_stats = classifier.classify(bookmarks)

    print("📊 Categorias:")

    for category, count in sorted(
        domain_stats.items(),
        key=lambda x: x[1],
        reverse=True,
    ):
        print(f"{category}: {count}")

    return domain_stats


async def check_links(bookmarks: list[Bookmark]) -> list[LinkStatus]:
    """
    Verifica status HTTP dos links.
    """

    print(f"🔗 Verificando {len(bookmarks)} links...")

    checker = LinkChecker(max_connections=20)

    results = await checker.check_links(bookmarks)

    print(f"✅ {len(results)} links verificados")

    return results


def export_results(bookmarks: list[Bookmark]) -> None:
    """
    Exporta resultados da análise.
    """

    print("💾 Exportando JSON...")

    exporter = JSONExporter(str(OUTPUT_JSON))
    exporter.export(bookmarks)

    print(f"✅ JSON salvo em: {OUTPUT_JSON.resolve()}")


# ---------------------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------------------


def main() -> None:
    """
    Executa o pipeline completo de análise.
    """

    bookmarks = parse_bookmarks()

    analyze_bookmarks(bookmarks)

    analyze_domains(bookmarks)

    classify_domains(bookmarks)

    asyncio.run(check_links(bookmarks))

    export_results(bookmarks)


if __name__ == "__main__":
    main()
