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
        "modules": len(MODULES),
        "simulations": len(MODULES),
        "questions": sum(len(module["quiz"]) for module in MODULES),
        "glossary_terms": sum(len(module["glossary"]) for module in MODULES),
        "notebooks": len(MODULES),
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
    minimum_pages = 5 + (len(MODULES) * 4)
    if len(pages) < minimum_pages:
        error(
            f"Se esperaban al menos {minimum_pages} páginas HTML y se encontraron "
            f"{len(pages)}"
        )
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
        if len(cells) < 12:
            error(f"Notebook incompleto {path.name}: {len(cells)} celdas")
        code_cells = [cell for cell in cells if cell.get("cell_type") == "code"]
        if len(code_cells) < 4:
            error(f"Notebook sin experimentación suficiente {path.name}")
        if not any("Criterio de éxito" in "".join(cell.get("source", [])) for cell in cells):
            error(f"Notebook sin criterio de éxito explícito {path.name}")
        if not any("Registro de decisión" in "".join(cell.get("source", [])) for cell in cells):
            error(f"Notebook sin registro de decisión {path.name}")
        for index, cell in enumerate(cells):
            if cell.get("cell_type") != "code":
                continue
            source = "".join(cell.get("source", []))
            try:
                ast.parse(source, filename=f"{path.name}:cell-{index}")
            except SyntaxError as exc:
                error(f"Python inválido en {path.name}, celda {index}: {exc}")


def validate_module_markdown() -> None:
    for module in MODULES:
        path = ROOT / "modules" / module["slug"] / "README.md"
        if not path.is_file():
            continue
        fenced = False
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if line.lstrip().startswith("```"):
                fenced = not fenced
                continue
            if not fenced and line.startswith("    ") and line.strip():
                error(
                    f"Sangría Markdown no intencional en "
                    f"{path.relative_to(ROOT)}:{line_number}"
                )
                break


def validate_javascript() -> None:
    node = shutil.which("node")
    scripts = sorted((DOCS / "assets" / "js").glob("*.js"))
    if not node:
        WARNINGS.append("Node no disponible; se omitió la validación sintáctica de JavaScript")
        return
    for script in scripts:
        result = subprocess.run(
            [node, "--check", "-"],
            input=script.read_text(encoding="utf-8"),
            capture_output=True,
            text=True,
            encoding="utf-8",
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
        editorial_text = re.sub(r'url\("data:[^"]+"\)', "", text)
        if forbidden_label.search(editorial_text):
            error(f"Etiqueta editorial no permitida en {path.relative_to(ROOT)}")
        if emoji.search(text):
            error(f"Emoji no permitido en {path.relative_to(ROOT)}")
        if preview_service in text:
            error(f"Servicio de previsualización no permitido en {path.relative_to(ROOT)}")


def validate_content_counts() -> None:
    for module in MODULES:
        if len(module["glossary"]) != 10:
            error(f"Módulo {module['id']}: glosario con {len(module['glossary'])} términos")
        if len(module["quiz"]) < 7:
            error(f"Módulo {module['id']}: cuestionario con {len(module['quiz'])} preguntas")
        if len(module["objectives"]) < 4:
            error(f"Módulo {module['id']}: objetivos insuficientes")
        if len(module["theory"]) < 4:
            error(f"Módulo {module['id']}: desarrollo conceptual insuficiente")
        external_resources = module.get("external_resources", [])
        local_resources = module.get("local_resources", [])
        index = DOCS / "modulos" / module["slug"] / "index.html"
        index_text = index.read_text(encoding="utf-8") if index.is_file() else ""
        notebook_count = len(module.get("notebook_resources") or [None])
        expected_progress_count = (
            4 + notebook_count + len(external_resources) + len(local_resources)
        )
        if f"de {expected_progress_count} recursos" not in index_text:
            error(
                f"Módulo {module['id']}: total de recursos inconsistente "
                f"en {index.relative_to(ROOT)}"
            )
        for resource_index, resource in enumerate(external_resources, start=1):
            if not resource.get("label") or not resource.get("url"):
                error(f"Módulo {module['id']}: recurso externo incompleto")
                continue
            readme = ROOT / "modules" / module["slug"] / "README.md"
            for path in (readme, index):
                if path.is_file() and resource["url"] not in path.read_text(
                    encoding="utf-8"
                ):
                    error(
                        f"Módulo {module['id']}: recurso externo ausente en "
                        f"{path.relative_to(ROOT)}"
                    )
            progress_marker = (
                f'data-progress-item="{module["id"]}:externo-{resource_index}"'
            )
            if progress_marker not in index_text:
                error(
                    f"Módulo {module['id']}: recurso externo sin seguimiento "
                    f"de progreso"
                )
        for resource_index, resource in enumerate(local_resources, start=1):
            if not resource.get("label") or not resource.get("url"):
                error(f"Módulo {module['id']}: recurso local incompleto")
                continue
            target = index.parent / resource["url"]
            if not target.is_file():
                error(
                    f"Módulo {module['id']}: recurso local inexistente "
                    f"{target.relative_to(ROOT)}"
                )
            readme = ROOT / "modules" / module["slug"] / "README.md"
            for path in (readme, index):
                if path.is_file() and resource["url"] not in path.read_text(encoding="utf-8"):
                    error(
                        f"Módulo {module['id']}: recurso local ausente en "
                        f"{path.relative_to(ROOT)}"
                    )
            progress_marker = f'data-progress-item="{module["id"]}:local-{resource_index}"'
            if progress_marker not in index_text:
                error(
                    f"Módulo {module['id']}: recurso local sin seguimiento de progreso"
                )
    simulations = (DOCS / "assets" / "js" / "simulations.js").read_text(encoding="utf-8")
    for module in MODULES:
        marker = f'"{module["id"]}": simulation{module["id"]}'
        if marker not in simulations:
            error(f"Falta registro de simulación para el módulo {module['id']}")
        simulation_page = DOCS / "modulos" / module["slug"] / "simulacion.html"
        if simulation_page.is_file() and (
            "Material elaborado por el profesor Sergio Gevatschnaider"
            not in simulation_page.read_text(encoding="utf-8")
        ):
            error(f"Falta atribución docente en la simulación del módulo {module['id']}")


def main() -> int:
    validate_manifest()
    validate_module_structure()
    validate_html()
    validate_notebooks()
    validate_module_markdown()
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
    print(f"  {len(MODULES)} módulos")
    print(f"  {len(list(DOCS.rglob('*.html')))} páginas HTML")
    print(f"  {len(MODULES)} simulaciones")
    print(f"  {sum(len(module['quiz']) for module in MODULES)} preguntas")
    print(f"  {sum(len(module['glossary']) for module in MODULES)} términos de glosario")
    print(f"  {len(MODULES)} notebooks con sintaxis válida")
    print("  Enlaces internos verificados")
    return 0


if __name__ == "__main__":
    sys.exit(main())
