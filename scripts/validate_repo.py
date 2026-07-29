"""Validaciones estructurales y de contenido sin dependencias externas."""

from __future__ import annotations

import ast
import json
import re
import shutil
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

from course_data import MODULES


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ERRORS: list[str] = []
WARNINGS: list[str] = []


class DocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.ids: list[str] = []
        self.lang = ""
        self.title = ""
        self.h1_count = 0
        self.main_count = 0
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "html":
            self.lang = values.get("lang", "") or ""
        if tag == "title":
            self._in_title = True
        if tag == "h1":
            self.h1_count += 1
        if tag == "main":
            self.main_count += 1
        if values.get("id"):
            self.ids.append(values["id"] or "")
        for attribute in ("href", "src"):
            value = values.get(attribute)
            if value:
                self.links.append(value)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data


def error(message: str) -> None:
    ERRORS.append(message)


def validate_manifest() -> None:
    path = ROOT / "course-manifest.json"
    if not path.exists():
        error("Falta course-manifest.json")
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    expected = {
        "modules": 15,
        "simulations": 15,
        "questions": 90,
        "glossary_terms": 150,
        "notebooks": 15,
    }
    for key, value in expected.items():
        if data.get(key) != value:
            error(f"Manifest: {key}={data.get(key)!r}; se esperaba {value}")


def validate_module_structure() -> None:
    required_pages = ["index.html", "simulacion.html", "cuestionario.html", "glosario.html"]
    for module in MODULES:
        docs_dir = DOCS / "modulos" / module["slug"]
        for filename in required_pages:
            if not (docs_dir / filename).is_file():
                error(f"Falta {docs_dir.relative_to(ROOT) / filename}")
        if not (ROOT / "modules" / module["slug"] / "README.md").is_file():
            error(f"Falta README del módulo {module['id']}")
        notebook = ROOT / "notebooks" / f"{module['slug']}.ipynb"
        if not notebook.is_file():
            error(f"Falta notebook del módulo {module['id']}")


def local_target(page: Path, raw_link: str) -> Path | None:
    parsed = urlparse(raw_link)
    if parsed.scheme or raw_link.startswith("//") or raw_link.startswith("#"):
        return None
    path_part = unquote(parsed.path)
    if not path_part:
        return None
    target = (page.parent / path_part).resolve()
    if path_part.endswith("/"):
        target = target / "index.html"
    return target


def validate_html() -> None:
    pages = sorted(DOCS.rglob("*.html"))
    if len(pages) != 65:
        error(f"Se esperaban 65 páginas HTML y se encontraron {len(pages)}")
    for page in pages:
        parser = DocumentParser()
        text = page.read_text(encoding="utf-8")
        try:
            parser.feed(text)
        except Exception as exc:
            error(f"HTML no analizable en {page.relative_to(ROOT)}: {exc}")
            continue
        if parser.lang != "es":
            error(f"Falta lang=es en {page.relative_to(ROOT)}")
        if not parser.title.strip():
            error(f"Falta title en {page.relative_to(ROOT)}")
        if parser.h1_count != 1:
            error(f"{page.relative_to(ROOT)} tiene {parser.h1_count} elementos h1")
        if parser.main_count != 1:
            error(f"{page.relative_to(ROOT)} tiene {parser.main_count} elementos main")
        duplicate_ids = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
        if duplicate_ids:
            error(f"IDs duplicados en {page.relative_to(ROOT)}: {duplicate_ids}")
        for raw_link in parser.links:
            target = local_target(page, raw_link)
            if target is None:
                continue
            try:
                target.relative_to(ROOT)
            except ValueError:
                error(f"Enlace sale del repositorio en {page.relative_to(ROOT)}: {raw_link}")
                continue
            if not target.exists():
                error(
                    f"Enlace roto en {page.relative_to(ROOT)}: "
                    f"{raw_link} -> {target.relative_to(ROOT)}"
                )


def validate_notebooks() -> None:
    notebooks = sorted((ROOT / "notebooks").glob("*.ipynb"))
    if len(notebooks) != 15:
        error(f"Se esperaban 15 notebooks y se encontraron {len(notebooks)}")
    for path in notebooks:
        try:
            notebook = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            error(f"Notebook inválido {path.name}: {exc}")
            continue
        if notebook.get("nbformat") != 4:
            error(f"Formato inesperado en {path.name}")
        cells = notebook.get("cells", [])
        if len(cells) < 5:
            error(f"Notebook incompleto {path.name}: {len(cells)} celdas")
        for index, cell in enumerate(cells):
            if cell.get("cell_type") != "code":
                continue
            source = "".join(cell.get("source", []))
            try:
                ast.parse(source, filename=f"{path.name}:cell-{index}")
            except SyntaxError as exc:
                error(f"Python inválido en {path.name}, celda {index}: {exc}")


def validate_javascript() -> None:
    node = shutil.which("node")
    scripts = sorted((DOCS / "assets" / "js").glob("*.js"))
    if not node:
        WARNINGS.append("Node no disponible; se omitió la validación sintáctica de JavaScript")
        return
    for script in scripts:
        result = subprocess.run(
            [node, "--check", str(script)],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode:
            error(f"JavaScript inválido en {script.relative_to(ROOT)}: {result.stderr.strip()}")


def validate_visible_content() -> None:
    forbidden_label = re.compile(r"(?:versi[oó]n\s*2|v\s*2(?:[.]0)?)", re.IGNORECASE)
    preview_service = "htmlpreview" + ".github.io"
    emoji = re.compile(
        "["
        "\U0001F1E6-\U0001F1FF"
        "\U0001F300-\U0001FAFF"
        "\U00002702-\U000027B0"
        "]"
    )
    extensions = {".html", ".md"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in extensions:
            continue
        text = path.read_text(encoding="utf-8")
        if forbidden_label.search(text):
            error(f"Etiqueta editorial no permitida en {path.relative_to(ROOT)}")
        if emoji.search(text):
            error(f"Emoji no permitido en {path.relative_to(ROOT)}")
        if preview_service in text:
            error(f"Servicio de previsualización no permitido en {path.relative_to(ROOT)}")


def validate_content_counts() -> None:
    for module in MODULES:
        if len(module["glossary"]) != 10:
            error(f"Módulo {module['id']}: glosario con {len(module['glossary'])} términos")
        if len(module["quiz"]) != 6:
            error(f"Módulo {module['id']}: cuestionario con {len(module['quiz'])} preguntas")
        if len(module["objectives"]) < 4:
            error(f"Módulo {module['id']}: objetivos insuficientes")
        if len(module["theory"]) < 4:
            error(f"Módulo {module['id']}: desarrollo conceptual insuficiente")
    simulations = (DOCS / "assets" / "js" / "simulations.js").read_text(encoding="utf-8")
    for module in MODULES:
        marker = f'"{module["id"]}": simulation{module["id"]}'
        if marker not in simulations:
            error(f"Falta registro de simulación para el módulo {module['id']}")


def main() -> int:
    validate_manifest()
    validate_module_structure()
    validate_html()
    validate_notebooks()
    validate_javascript()
    validate_visible_content()
    validate_content_counts()
    if WARNINGS:
        print("Advertencias:")
        for message in WARNINGS:
            print(f"  - {message}")
    if ERRORS:
        print(f"Validación fallida con {len(ERRORS)} error(es):")
        for message in ERRORS:
            print(f"  - {message}")
        return 1
    print("Validación completa")
    print("  15 módulos")
    print("  65 páginas HTML")
    print("  15 simulaciones")
    print("  90 preguntas")
    print("  150 términos de glosario")
    print("  15 notebooks con sintaxis válida")
    print("  Enlaces internos verificados")
    return 0


if __name__ == "__main__":
    sys.exit(main())
