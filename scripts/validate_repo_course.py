"""Validaciones adicionales para módulos docentes personalizados.

El Módulo 08 publica los HTML originales completos provistos por el docente.
No se reescriben para satisfacer reglas editoriales generales: se preservan sus
controles, estilos, iconografía, explicaciones y JavaScript.
"""
from __future__ import annotations

from pathlib import Path
import validate_repo as base

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_CONTENT_COUNTS = base.validate_content_counts
ORIGINAL_VISIBLE_CONTENT = base.validate_visible_content
M07 = ROOT / "modules/07-series-tiempo/site"
M08 = ROOT / "modules/08-regresion-logistica/site"

ORIGINALS = {
    "simuladores/simulador_01_funcion_sigmoide_regresion_logistica.html":
        ("Laboratorio de la Función Sigmoide · Regresión Logística", 25927),
    "simuladores/simulador_02_probabilidad_odds_logit_odds_ratio.html":
        ("Simulador 02 · Probabilidad, Odds, Logit y Odds Ratio", 25514),
    "simuladores/simulador_03_efectos_marginales_regresion_logistica.html":
        ("Simulador 03 · Efectos Marginales en Regresión Logística", 23632),
    "simuladores/simulador_04_log_loss_maxima_verosimilitud.html":
        ("Simulador 04 · Log-Loss y Máxima Verosimilitud", 23395),
    "simuladores/simulador_05_threshold_matriz_confusion_metricas.html":
        ("Simulador 05 · Threshold Lab — Matriz de Confusión y Métricas", 24892),
    "simuladores/simulador_06_roc_precision_recall_desbalance.html":
        ("Simulador 06 · ROC, Precision–Recall y Desbalance", 28428),
    "simuladores/simulador_07_frontera_decision_2d_regresion_logistica.html":
        ("Simulador 07 · Frontera de Decisión 2D", 25348),
    "simuladores/simulador_08_regularizacion_l1_l2_overfitting.html":
        ("Simulador 08 · Regularización L1/L2 y Overfitting", 30365),
    "simuladores/simulador_09_dummies_interacciones_no_linealidades.html":
        ("Simulador 09 · Dummies, Interacciones y No Linealidades", 26636),
    "simuladores/simulador_10_train_validation_test_kfold_cross_validation.html":
        ("Simulador 10 · Train, Validation, Test y K-Fold Cross-Validation", 30958),
    "simuladores/simulador_11_calibracion_vs_discriminacion.html":
        ("Simulador 11 · Calibración vs Discriminación", 27635),
    "simuladores/simulador_12_decision_lab_credit_scoring_costos.html":
        ("Simulador 12 · Decision Lab — Credit Scoring, Threshold y Costos", 35060),
    "simuladores/simulador_13_softmax_clasificacion_multiclase.html":
        ("Simulador 13 · Softmax y Clasificación Multiclase", 24529),
    "simuladores/simulador_14_model_drift_monitoring.html":
        ("Simulador 14 · Model Drift & Monitoring", 35731),
    "glosario.html":
        ("Glosario avanzado · Regresión Logística y Clasificación", 186613),
    "cuestionario.html":
        ("Cuestionario avanzado · Regresión Logística", 49857),
}

def discard(fragment: str) -> None:
    base.ERRORS[:] = [e for e in base.ERRORS if fragment not in e]

def require(path: Path, label: str) -> str:
    if not path.is_file():
        base.error(f"{label}: falta {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")

def validate_visible_content_with_original_m08() -> None:
    ORIGINAL_VISIBLE_CONTENT()
    protected = (
        "modules/09-arboles-ensembles/site/simuladores/",
        "docs/modulos/09-arboles-ensembles/simuladores/",
        "docs/modulos/10-clustering/simuladores/",
        "docs/modulos/10-clustering/visor-integrado.html",
        "docs/modulos/10-clustering/glosario.html",
        "docs/modulos/10-clustering/cuestionario.html",
        "docs/modulos/10-clustering/videos.html",
        "docs/modulos/09-arboles-ensembles/simulacion.html",
        "modules/09-arboles-ensembles/site/simulacion.html",
        "modules/09-arboles-ensembles/site/glosario.html",
        "modules/09-arboles-ensembles/site/cuestionario.html",
        "docs/modulos/09-arboles-ensembles/glosario.html",
        "docs/modulos/09-arboles-ensembles/cuestionario.html",
        "modules/08-regresion-logistica/site/simuladores/",
        "modules/08-regresion-logistica/site/glosario.html",
        "modules/08-regresion-logistica/site/cuestionario.html",
        "docs/modulos/08-regresion-logistica/simuladores/",
        "docs/modulos/08-regresion-logistica/glosario.html",
        "docs/modulos/08-regresion-logistica/cuestionario.html",
    )
    base.ERRORS[:] = [
        e for e in base.ERRORS
        if not (
            e.startswith("Emoji no permitido en ")
            and any(p in e for p in protected)
        )
    ]

def validate_content_counts_with_custom_modules() -> None:
    ORIGINAL_CONTENT_COUNTS()

    # Módulo 07.
    discard("Módulo 07: cuestionario con 6 preguntas")
    q07 = require(M07 / "cuestionario.html", "Módulo 07")
    if q07 and 'data-question-count="20"' not in q07:
        base.error("Módulo 07: el cuestionario avanzado no declara 20 preguntas")

    # Módulo 08: el portal personalizado reemplaza el checklist genérico.
    discard("Módulo 08: total de recursos inconsistente")

    required = {
        "index.html", "presentacion-01.html", "presentacion-02.html",
        "simulacion.html", "guia.html", "cuestionario.html",
        "glosario.html", "styles.css", "site.js",
    }
    missing = sorted(name for name in required if not (M08 / name).is_file())
    if missing:
        base.error("Módulo 08: faltan recursos avanzados: " + ", ".join(missing))

    # Los 16 recursos deben conservar exactamente la versión textual recuperada
    # de los uploads originales, además de sus títulos.
    for relative, (title, expected_chars) in ORIGINALS.items():
        target = M08 / relative
        text = require(target, "Módulo 08")
        if not text:
            continue
        if len(text) != expected_chars:
            base.error(
                f"Módulo 08: {relative} cambió de extensión "
                f"({len(text)} caracteres; esperado {expected_chars})"
            )
        if f"<title>{title}</title>" not in text:
            base.error(f"Módulo 08: título original alterado en {relative}")

    glossary = require(M08 / "glosario.html", "Módulo 08")
    if glossary and glossary.count("<details") != 88:
        base.error(
            f"Módulo 08: el glosario debe conservar 88 entradas; "
            f"se detectaron {glossary.count('<details')}"
        )

    q08 = require(M08 / "cuestionario.html", "Módulo 08")
    if q08:
        import re
        ids = re.findall(r'["\']id["\']\s*:\s*\d+', q08)
        if len(ids) != 30 or not re.search(r'["\']id["\']\s*:\s*30\b', q08):
            base.error("Módulo 08: el cuestionario no conserva sus 30 preguntas originales")

    hub = require(M08 / "simulacion.html", "Módulo 08")
    if hub:
        for i in range(1, 15):
            if f"simulador_{i:02d}_" not in hub:
                base.error(f"Módulo 08: el catálogo no enlaza el simulador original {i:02d}")

    index = require(M08 / "index.html", "Módulo 08")
    if index:
        for resource in (
            "presentacion-01.html", "presentacion-02.html", "simulacion.html",
            "guia.html", "cuestionario.html", "glosario.html"
        ):
            if resource not in index:
                base.error(f"Módulo 08: recurso {resource} ausente del portal")

    # Módulo 09: presentaciones completas y simulaciones originales.
    discard("Módulo 09: total de recursos inconsistente")
    m09 = ROOT / "modules/09-arboles-ensembles/site"
    for resource in ("index.html", "styles.css", "presentaciones.js",
                     "presentacion-01.html", "presentacion-02.html", "presentacion-03.html",
                     "guia.html", "glosario.html", "cuestionario.html",
                     "estudio.js", "estudio.css", "glosario.js", "cuestionario.js",
                     "videos.html", "videos.css", "videos.js", "videos-badge.svg"):
        source = m09 / resource
        require(source, "Módulo 09")
        published = ROOT / "docs/modulos/09-arboles-ensembles" / resource
        if source.is_file() and (not published.is_file() or source.read_bytes() != published.read_bytes()):
            base.error(f"Módulo 09: publicación diferente de la fuente: {resource}")
    import re
    from html import unescape
    glossary = require(m09 / "glosario.html", "Módulo 09")
    quiz = require(m09 / "cuestionario.html", "Módulo 09")
    for content, css_class, expected, marker in (
        (glossary, "term-card", 109, 'data-term-count="109"'),
        (quiz, "qcard", 60, 'data-question-count="60"'),
    ):
        cards = re.findall(r'<article\b[^>]*class="[^"]*\b' + css_class + r'\b[^\"]*"', content)
        if len(cards) != expected or marker not in content:
            base.error(f"Módulo 09: se requieren {expected} fichas completas de {css_class}")
        if content.count("<details") != expected:
            base.error(f"Módulo 09: faltan explicaciones completas de {css_class}")
        ids = set(re.findall(r'\bid="([^\"]+)"', content))
        for fragment in re.findall(r'href="#([^\"]+)"', content):
            if unescape(fragment) not in ids:
                base.error(f"Módulo 09: enlace interno inexistente: #{fragment}")
    pdf = m09 / "guia/guia-simulaciones.pdf"
    published_pdf = ROOT / "docs/modulos/09-arboles-ensembles/guia/guia-simulaciones.pdf"
    if not pdf.is_file() or not published_pdf.is_file() or pdf.read_bytes() != published_pdf.read_bytes():
        base.error("Módulo 09: la guía PDF no está publicada íntegramente")
    guide = require(m09 / "guia.html", "Módulo 09")
    index = require(m09 / "index.html", "Módulo 09")
    for resource in ("guia.html", "glosario.html", "cuestionario.html", "simulacion.html", "videos.html"):
        if f'href="{resource}"' not in index:
            base.error(f"Módulo 09: falta acceso a {resource} en el portal")
    for number, count in ((1, 41), (2, 36), (3, 35)):
        page = require(m09 / f"presentacion-{number:02d}.html", "Módulo 09")
        if page and f'data-slide-count="{count}"' not in page:
            base.error(f"Módulo 09: cantidad de diapositivas incorrecta en PPT {number:02d}")
        for suffix in ("pptx", "pdf"):
            require_path = m09 / "presentaciones" / f"ppt{number:02d}.{suffix}"
            if not require_path.is_file():
                base.error(f"Módulo 09: falta descarga {require_path.name}")

    hub = require(m09 / "simulacion.html", "Módulo 09")
    if 'data-simulation-count="16"' not in hub:
        base.error("Módulo 09: el catálogo no declara las 16 simulaciones")
    simulations = sorted((m09 / "simuladores").glob("simulador_[0-9][0-9]_*.html"))
    if len(simulations) != 16:
        base.error(f"Módulo 09: hay {len(simulations)} simulaciones; se requieren 16")
    for number, simulation in enumerate(simulations, start=1):
        if not simulation.name.startswith(f"simulador_{number:02d}_"):
            base.error("Módulo 09: secuencia incompleta de simulaciones")
        if f"simuladores/{simulation.name}" not in hub:
            base.error(f"Módulo 09: el catálogo no enlaza {simulation.name}")
        if f"simuladores/{simulation.name}" not in guide:
            base.error(f"Módulo 09: la guía no enlaza {simulation.name}")
        content = simulation.read_text(encoding="utf-8")
        if len(content.encode("utf-8")) < 15000 or "<script>" not in content:
            base.error(f"Módulo 09: simulación original incompleta: {simulation.name}")
        published = ROOT / "docs/modulos/09-arboles-ensembles/simuladores" / simulation.name
        if not published.is_file() or published.read_bytes() != simulation.read_bytes():
            base.error(f"Módulo 09: publicación diferente de la fuente: {simulation.name}")

def validate_content_counts_with_m10_laboratories():
    validate_content_counts_with_custom_modules()

    m10 = ROOT / "docs/modulos/10-clustering"
    hub_file = m10 / "simulacion.html"
    index_file = m10 / "index.html"
    guide_file = m10 / "guia.html"
    viewer_file = m10 / "visor-integrado.html"
    if not hub_file.is_file() or not index_file.is_file() or not guide_file.is_file():
        base.error("Módulo 10: falta el catálogo, el índice o la guía de estudio")
        return

    hub = hub_file.read_text(encoding="utf-8")
    index = index_file.read_text(encoding="utf-8")
    guide = guide_file.read_text(encoding="utf-8")
    if 'href="simulacion.html"' not in index or 'id="simulaciones"' not in index:
        base.error("Módulo 10: el índice no permite acceder al laboratorio de 14 simulaciones")
    if 'href="simulacion.html"' not in guide:
        base.error("Módulo 10: la guía no enlaza las 14 simulaciones")
    if not viewer_file.is_file() or "M10" not in viewer_file.read_text(encoding="utf-8"):
        base.error("Módulo 10: falta el visor integrado")
    simulations = sorted((m10 / "simuladores").glob("S[0-9][0-9].html"))
    if len(simulations) != 14:
        base.error(f"Módulo 10: hay {len(simulations)} simulaciones; se requieren 14")
    for number in range(1, 15):
        name = f"S{number:02}.html"
        path = m10 / "simuladores" / name
        if f'href="simuladores/{name}"' not in hub:
            base.error(f"Módulo 10: el catálogo no enlaza {name}")
        if not path.is_file():
            base.error(f"Módulo 10: falta el laboratorio {name}")
            continue
        content = path.read_text(encoding="utf-8")
        for marker in ('id="m10-embedded-css"', "window.M10Lab", 'data-action="theme"'):
            if marker not in content:
                base.error(f"Módulo 10: {name} no conserva el diseño/motor/autonomía ({marker})")
        if "<script src=" in content or '<link rel="stylesheet"' in content:
            base.error(f"Módulo 10: {name} tiene dependencias externas; debe ser autónomo")
        if 'href="../simulacion.html"' not in content:
            base.error(f"Módulo 10: falta el regreso al catálogo desde {name}")


    # Guías ampliadas M10: mayor profundidad que el M09 y HTML autosuficiente.
    for filename, expected, element, marker in (
        ("glosario.html", 132, "article", 'data-term-count="132"'),
        ("cuestionario.html", 128, "article", 'data-question-count="128"'),
    ):
        path = m10 / filename
        if not path.is_file():
            base.error(f"Módulo 10: falta la guía desarrollada {filename}")
            continue
        source = path.read_text(encoding="utf-8")
        import re
        cards = re.findall(r'<article\s+class="card"\b', source)
        # Count cards more robustly regardless of attribute order.
        count = source.count('<article class="card"')
        detailed = source.count("<details>")
        if count != expected or detailed != expected or marker not in source:
            base.error(f"Módulo 10: {filename} debe tener {expected} fichas y respuestas desarrolladas (detectadas {count}/{detailed})")
        if "<style>" not in source or "<script>" not in source:
            base.error(f"Módulo 10: {filename} no contiene CSS y JS autónomos")
        if "Material elaborado por el profesor Sergio Gevatschnaider" not in source:
            base.error(f"Módulo 10: {filename} falta atribución docente")
        if f'href="{filename}"' not in index:
            base.error(f"Módulo 10: índice principal no enlaza {filename}")
        if 'href="guia.html"' not in source or 'href="simulacion.html"' not in source:
            base.error(f"Módulo 10: {filename} carece de navegación al material de clase")
        if not all(token in source for token in ('id="search"', 'id="themeBtn"', 'id="progressbar"')):
            base.error(f"Módulo 10: {filename} no conserva controles de estudio")


    # La tabla visible del README debe mostrar la misma insignia que el Módulo 09.
    readme_file = ROOT / "README.md"
    badge = m10 / "videos-badge.svg"
    if not badge.is_file() or "Videos: 14 videos complementarios del Módulo 10" not in badge.read_text(encoding="utf-8"):
        base.error("Módulo 10: falta el distintivo SVG de 14 videos")
    if readme_file.is_file():
        m10_row = next((line for line in readme_file.read_text(encoding="utf-8").splitlines()
                        if line.startswith("| 10 |")), "")
        if ('docs/modulos/10-clustering/videos-badge.svg' not in m10_row or
            'modulos/10-clustering/videos.html' not in m10_row):
            base.error("Módulo 10: falta el botón Videos · 14 videos en la fila 10 del README")

    # Videoteca M10: 14 piezas independientes, vinculadas a PPT y laboratorios.
    videos_page = m10 / "videos.html"
    videos_css = m10 / "videos.css"
    videos_js = m10 / "videos.js"
    for video_asset in (videos_page, videos_css, videos_js):
        if not video_asset.is_file():
            base.error(f"Módulo 10: falta videoteca {video_asset.name}")
    if videos_page.is_file() and videos_css.is_file() and videos_js.is_file():
        html = videos_page.read_text(encoding="utf-8")
        js = videos_js.read_text(encoding="utf-8")
        import re
        cards = re.findall(r'<article id="video-[PKH]\d{2}" class="video-card\b', html)
        ids = re.findall(r'data-video="([A-Za-z0-9_-]{11})"', html)
        if len(cards) != 14 or len(ids) != 14 or len(set(ids)) != 14:
            base.error(f"Módulo 10: videoteca incompleta (tarjetas={len(cards)}, videos={len(ids)})")
        for name, n in (("pca", 5), ("kmeans", 5), ("jerarquico", 4)):
            if len(re.findall(r'<article id="video-[PKH]\d{2}" class="video-card ' + name + '"', html)) != n:
                base.error(f"Módulo 10: ruta audiovisual {name} debe contener {n} videos")
        for token in ('id="reproductor"', 'id="searchVideos"', 'id="themeToggle"',
                      'id="progressFill"', 'href="guia.html"', 'href="simulacion.html"',
                      'href="presentaciones/M10_01_PCA_Clase_Completa.pdf#',
                      'href="presentaciones/M10_02_KMeans_Clase_Completa.pdf#',
                      'href="presentaciones/M10_03_Jerarquico_Clase_Completa.pdf#'):
            if token not in html:
                base.error(f"Módulo 10: falta control o referencia de video: {token}")
        if "youtube-nocookie.com/embed/" not in js or "playerBox.replaceChildren(frame)" not in js:
            base.error("Módulo 10: no funciona el reproductor diferido")
        if "searchParams.set('end'," in js or 'searchParams.set("end",' in js:
            base.error("Módulo 10: el reproductor no debe cortar los videos antes del final")
        for document_name in ("index.html", "guia.html"):
            if 'href="videos.html"' not in (m10 / document_name).read_text(encoding="utf-8"):
                base.error(f"Módulo 10: {document_name} no enlaza la videoteca")


    # Notebook M10: exigir el laboratorio integral y su protección ante regeneración.
    import json
    notebook_file = ROOT / "notebooks/10-clustering.ipynb"
    if not notebook_file.is_file():
        base.error("Módulo 10: falta notebooks/10-clustering.ipynb")
    else:
        notebook = json.loads(notebook_file.read_text(encoding="utf-8"))
        cells = notebook.get("cells", [])
        code_cells = [cell for cell in cells if cell.get("cell_type") == "code"]
        full_text = "\n".join("".join(cell.get("source", [])) for cell in cells)
        if len(cells) < 76 or len(code_cells) < 32:
            base.error(f"Módulo 10: el Colab integral requiere 76 celdas y 32 de código; contiene {len(cells)} y {len(code_cells)}")
        for concept in (
            "Criterio de éxito", "Registro de decisión", "bootstrap_stability",
            "SVD", "PCA", "KMeans", "linkage", "dendrogram", "fcluster",
            "silhouette_score", "DBSCAN", "make_customers", "panel_experimento",
            "joblib.dump", "assert checks['Aprobada'].all()",
        ):
            if concept not in full_text:
                base.error(f"Módulo 10: falta un bloque indispensable del Colab: {concept}")
        m10 = next((m for m in base.MODULES if m["id"] == "10"), None)
        if not m10 or m10.get("custom_notebook") is not True:
            base.error("Módulo 10: el generador no protege el Colab integral con custom_notebook")
        index = (ROOT / "docs/modulos/10-clustering/index.html").read_text(encoding="utf-8")
        if "Abrir Colab integral · 76 celdas" not in index:
            base.error("Módulo 10: falta acceso destacado al Colab integral en el módulo")
        for cell in code_cells:
            if cell.get("outputs") or cell.get("execution_count") is not None:
                base.error("Módulo 10: el notebook publicado debe estar limpio y ser reproducible")
                break


    # M02: visores sin autorización de Drive para las 30 diapositivas.
    m02_root = ROOT / "docs/modulos/02-calidad-datos"
    index_m02 = m02_root / "index.html"
    guide_m02 = m02_root / "guia-presentaciones.html"
    common_css = m02_root / "presentaciones.css"
    common_js = m02_root / "presentaciones.js"
    expected_pdf = (
        "M02_01_Calidad_Datos.pdf",
        "M02_02_MCAR_MAR_MNAR.pdf",
        "M02_03_Imputacion_Pipelines.pdf",
    )
    for target in (index_m02, guide_m02, common_css, common_js):
        if not target.is_file():
            base.error(f"Módulo 02: falta el archivo de presentación {target.name}")
    if index_m02.is_file():
        html = index_m02.read_text(encoding="utf-8")
        if "docs.google.com/presentation/" in html:
            base.error("Módulo 02: quedan enlaces a Slides que solicitan permisos")
        if 'href="guia-presentaciones.html"' not in html:
            base.error("Módulo 02: falta acceso a la guía de presentaciones")
        for number in range(1, 4):
            if f'href="presentacion-0{number}.html"' not in html:
                base.error(f"Módulo 02: falta enlace al visor {number}")
    if guide_m02.is_file():
        html = guide_m02.read_text(encoding="utf-8")
        if 'id="pdf"' not in html or 'id="theme"' not in html:
            base.error("Módulo 02: la guía no ofrece lector PDF y cambio de tema")
        for filename in expected_pdf:
            if filename not in html:
                base.error(f"Módulo 02: guía sin documento {filename}")
        if "docs.google.com/presentation/" in html:
            base.error("Módulo 02: guía depende de enlaces a Google Slides")
    if common_js.is_file():
        js = common_js.read_text(encoding="utf-8")
        for control in ("M02_DECK", "getDocument", "slideRange", "btnFullscreen", "btnGrid"):
            if control not in js:
                base.error(f"Módulo 02: visor sin control funcional {control}")
    for i, filename in enumerate(expected_pdf, 1):
        page = m02_root / f"presentacion-0{i}.html"
        pdf = m02_root / "presentaciones" / filename
        if not page.is_file():
            base.error(f"Módulo 02: falta visor {i}")
            continue
        html = page.read_text(encoding="utf-8")
        if f"presentaciones/{filename}" not in html or 'slides:10' not in html:
            base.error(f"Módulo 02: visor {i} no apunta al PDF de diez láminas")
        if "docs.google.com/presentation/" in html:
            base.error(f"Módulo 02: visor {i} exige permisos Drive")
        if not pdf.is_file() or pdf.stat().st_size < 300_000 or not pdf.read_bytes().startswith(b"%PDF"):
            base.error(f"Módulo 02: PDF ausente o inválido {filename}")


base.validate_visible_content = validate_visible_content_with_original_m08
base.validate_content_counts = validate_content_counts_with_m10_laboratories

if __name__ == "__main__":
    raise SystemExit(base.main())
