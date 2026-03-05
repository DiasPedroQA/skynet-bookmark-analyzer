"""
PDF Exporter
============

Responsável por gerar um relatório PDF com base
nos dados analisados dos bookmarks.
"""

from pathlib import Path
from typing import Any

from weasyprint import HTML


class PDFExporter:
    """
    Gera relatório PDF da análise de bookmarks.
    """

    def __init__(self, output_path: str = "output/report.pdf") -> None:
        """
        Inicializa o exportador.

        Args:
            output_path: caminho onde o PDF será salvo.
        """

        self.output_path = Path(output_path)

        # garante que a pasta exista
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

    def export(self, analysis: dict[str, Any]) -> Path:
        """
        Gera o relatório PDF.

        Args:
            analysis: dados gerados pelo bookmark_analyzer.

        Returns:
            Caminho do PDF gerado.
        """

        html_content: str = self._build_html(analysis)

        HTML(string=html_content).write_pdf(self.output_path)

        return self.output_path

    def _build_html(self, analysis: dict[str, Any]) -> str:
        """
        Constrói o HTML do relatório.

        Args:
            analysis: dados da análise.

        Returns:
            HTML renderizado.
        """

        total = analysis.get("total_bookmarks", 0)
        domains = analysis.get("top_domains", [])

        domain_rows: str = "".join(
            f"<tr><td>{domain}</td><td>{count}</td></tr>" for domain, count in domains
        )

        html: str = f"""
        <html>
        <head>
            <meta charset="utf-8">
            <style>

                body {{
                    font-family: Arial, sans-serif;
                    margin: 40px;
                }}

                h1 {{
                    color: #333;
                }}

                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}

                th, td {{
                    border: 1px solid #ccc;
                    padding: 8px;
                    text-align: left;
                }}

                th {{
                    background: #f5f5f5;
                }}

                .stats {{
                    margin-top: 20px;
                }}

            </style>
        </head>

        <body>

            <h1>Bookmark Analysis Report</h1>

            <div class="stats">
                <p><strong>Total bookmarks:</strong> {total}</p>
            </div>

            <h2>Top Domains</h2>

            <table>
                <tr>
                    <th>Domain</th>
                    <th>Count</th>
                </tr>

                {domain_rows}

            </table>

        </body>
        </html>
        """

        return html
