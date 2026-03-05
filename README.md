# SkyNet Bookmark Analyzer

Ferramenta Python para análise de bookmarks exportados de navegadores.

## Funcionalidades

- Parsing de arquivos HTML de bookmarks
- Análise de domínios e detecção de duplicados
- Armazenamento incremental em SQLite
- Exportação de resultados para JSON

## Estrutura do projeto

```text

skynet-bookmark-analyzer/
├─ core/
│  ├─ parser/
│  ├─ analysis/
│  └─ exporters/
├─ data/         # Banco SQLite
├─ output/       # Arquivos JSON exportados
├─ main.py       # Pipeline principal
├─ .gitignore
└─ README.md

````

## Requisitos

- Python 3.11+
- Bibliotecas:
  - `beautifulsoup4`
  - `lxml` (opcional para parsing mais rápido)

Instale as dependências:

```bash
pip install -r requirements.txt
````

## Como rodar

```bash
python main.py
```
