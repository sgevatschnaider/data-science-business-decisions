"""Genera el sitio estático, notebooks, datos y guías del curso."""

from __future__ import annotations

import argparse
import csv
import html
import io
import json
import math
import random
import tempfile
from pathlib import Path
from textwrap import dedent

from course_data import COURSE, MODULES, MODULES_BY_ID, UNITS


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PAGES_URL = (
    f"https://{COURSE['owner']}.github.io/{COURSE['repository']}"
)
REPO_URL = (
    f"https://github.com/{COURSE['owner']}/{COURSE['repository']}"
)


def write(relative_path: str, content: str) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def module_url(module: dict, resource: str = "index.html") -> str:
    return f"{PAGES_URL}/modulos/{module['slug']}/{resource}"


def notebook_url(module: dict) -> str:
    return (
        "https://colab.research.google.com/github/"
        f"{COURSE['owner']}/{COURSE['repository']}/blob/main/"
        f"notebooks/{module['slug']}.ipynb"
    )


def head(title: str, description: str, prefix: str = "") -> str:
    return dedent(
        f"""
        <!doctype html>
        <html lang="es">
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <meta name="description" content="{esc(description)}">
          <meta name="author" content="{esc(COURSE['author'])}">
          <meta name="theme-color" content="#082f49">
          <title>{esc(title)} | {esc(COURSE['short_title'])}</title>
          <link rel="stylesheet" href="{prefix}assets/css/course.css">
        </head>
        """
    ).strip()


def site_header(prefix: str = "") -> str:
    return dedent(
        f"""
        <a class="skip-link" href="#contenido">Saltar al contenido</a>
        <header class="site-header">
          <div class="container header-inner">
            <a class="brand" href="{prefix}index.html" aria-label="Inicio del curso">
              <span class="brand-mark" aria-hidden="true">DD</span>
              <span>
                <strong>{esc(COURSE['short_title'])}</strong>
                <small>Ciencia de datos aplicada</small>
              </span>
            </a>
            <button class="nav-toggle" type="button" aria-expanded="false"
                    aria-controls="site-navigation">Menú</button>
            <nav id="site-navigation" class="site-nav" aria-label="Navegación principal">
              <a href="{prefix}index.html">Inicio</a>
              <a href="{prefix}programa.html">Programa</a>
              <a href="{prefix}proyecto-integrador.html">Proyecto</a>
              <a href="{prefix}profundizaciones.html">Profundizaciones</a>
              <a href="{REPO_URL}">Código</a>
              <button class="theme-toggle" type="button" aria-label="Cambiar tema">
                Tema
              </button>
            </nav>
          </div>
        </header>
        """
    ).strip()


def site_footer(prefix: str = "") -> str:
    return dedent(
        f"""
        <footer class="site-footer">
          <div class="container footer-grid">
            <div>
              <strong>{esc(COURSE['title'])}</strong>
              <p>Material elaborado por el profesor {esc(COURSE['author'])}.</p>
            </div>
            <div>
              <a href="{prefix}programa.html">Programa</a>
              <a href="{prefix}accesibilidad.html">Accesibilidad</a>
              <a href="{REPO_URL}">Repositorio</a>
            </div>
          </div>
        </footer>
        <script src="{prefix}assets/js/course-data.js"></script>
        <script src="{prefix}assets/js/site.js"></script>
        """
    ).strip()


def shell(
    title: str,
    description: str,
    body: str,
    *,
    prefix: str = "",
    body_class: str = "",
    extra_scripts: list[str] | None = None,
    data_attrs: str = "",
) -> str:
    scripts = "\n".join(
        f'<script src="{prefix}assets/js/{name}"></script>'
        for name in (extra_scripts or [])
    )
    return dedent(
        f"""
        {head(title, description, prefix)}
        <body class="{body_class}" {data_attrs}>
          {site_header(prefix)}
          <main id="contenido">
            {body}
          </main>
          {site_footer(prefix)}
          {scripts}
        </body>
        </html>
        """
    ).strip()


def resource_table(module: dict, relative: bool = True) -> str:
    if relative:
        links = {
            "Guía del módulo": "index.html",
            "Simulación interactiva": "simulacion.html",
            "Cuestionario": "cuestionario.html",
            "Glosario": "glosario.html",
            "Notebook en Colab": notebook_url(module),
        }
    else:
        links = {
            "Guía del módulo": module_url(module),
            "Simulación interactiva": module_url(module, "simulacion.html"),
            "Cuestionario": module_url(module, "cuestionario.html"),
            "Glosario": module_url(module, "glosario.html"),
            "Notebook en Colab": notebook_url(module),
        }
    for resource in module.get("external_resources", []):
        links[resource["label"]] = resource["url"]
    for resource in module.get("local_resources", []):
        links[resource["label"]] = (
            resource["url"] if relative else module_url(module, resource["url"])
        )
    rows = "\n".join(
        (
            f"<tr><th scope=\"row\">{esc(label)}</th>"
            f"<td><a class=\"table-link\" href=\"{esc(url)}\">Abrir recurso</a></td></tr>"
        )
        for label, url in links.items()
    )
    return dedent(
        f"""
        <div class="table-wrap">
          <table class="resource-table">
            <caption>Índice interactivo del módulo</caption>
            <thead><tr><th>Recurso</th><th>Acceso</th></tr></thead>
            <tbody>{rows}</tbody>
          </table>
        </div>
        """
    ).strip()


def module_card(module: dict, prefix: str = "") -> str:
    return dedent(
        f"""
        <article class="module-card" data-module-card
                 data-search="{esc((module['id'] + ' ' + module['title'] + ' ' + module['summary']).lower())}">
          <div class="module-card-top">
            <span class="module-number">Módulo {module['id']}</span>
            <span class="module-unit">Unidad {module['unit']}</span>
          </div>
          <h3><a href="{prefix}modulos/{module['slug']}/index.html">{esc(module['title'])}</a></h3>
          <p>{esc(module['summary'])}</p>
          <div class="module-card-meta">
            <span>Simulación</span><span>Cuestionario</span><span>Glosario</span>
          </div>
          <a class="text-link" href="{prefix}modulos/{module['slug']}/index.html">
            Abrir módulo <span aria-hidden="true">-&gt;</span>
          </a>
        </article>
        """
    ).strip()


def home_page() -> str:
    unit_sections = []
    for unit in UNITS:
        cards = "\n".join(
            module_card(MODULES_BY_ID[module_id])
            for module_id in unit["modules"]
        )
        unit_sections.append(
            dedent(
                f"""
                <section class="course-unit" id="{unit['id']}">
                  <div class="section-heading split-heading">
                    <div>
                      <p class="eyebrow">Unidad {unit['number']}</p>
                      <h2>{esc(unit['title'])}</h2>
                    </div>
                    <p>{esc(unit['question'])}</p>
                  </div>
                  <div class="module-grid">{cards}</div>
                </section>
                """
            ).strip()
        )
    body = dedent(
        f"""
        <section class="hero">
          <div class="container hero-grid">
            <div class="hero-copy">
              <p class="eyebrow">Curso abierto e interactivo</p>
              <h1>{esc(COURSE['title'])}</h1>
              <p class="hero-lead">{esc(COURSE['description'])}</p>
              <div class="button-row">
                <a class="button primary" href="#recorrido">Comenzar el recorrido</a>
                <a class="button secondary" href="programa.html">Ver programa</a>
              </div>
              <p class="hero-note">Sin instalación para las simulaciones. Notebooks listos para Colab.</p>
            </div>
            <div class="decision-loop" aria-label="Ciclo del curso">
              <div class="loop-center">Decisión</div>
              <div class="loop-item item-1"><span>1</span>Problema</div>
              <div class="loop-item item-2"><span>2</span>Datos</div>
              <div class="loop-item item-3"><span>3</span>Modelo</div>
              <div class="loop-item item-4"><span>4</span>Valor</div>
            </div>
          </div>
        </section>
        <section class="stats-band" aria-label="Alcance del curso">
          <div class="container stats-grid">
            <div><strong>15</strong><span>módulos</span></div>
            <div><strong>15</strong><span>simulaciones</span></div>
            <div><strong>{sum(len(module['quiz']) for module in MODULES)}</strong><span>preguntas</span></div>
            <div><strong>150</strong><span>términos</span></div>
            <div><strong>15</strong><span>notebooks</span></div>
          </div>
        </section>
        <section class="container start-panel">
          <div>
            <p class="eyebrow">Continuidad local</p>
            <h2>Tu avance queda guardado en este navegador</h2>
            <p>Marcá recursos completados, resolvé cuestionarios y retomá desde el tablero general.</p>
          </div>
          <div class="overall-progress">
            <div class="progress-label"><span>Progreso global</span><strong data-global-progress>0%</strong></div>
            <div class="progress-track"><span data-global-progress-bar></span></div>
            <button class="button tertiary" type="button" data-resume>Ir al próximo recurso</button>
          </div>
        </section>
        <section id="recorrido" class="container course-index">
          <div class="section-heading">
            <p class="eyebrow">Mapa de aprendizaje</p>
            <h2>Índice general</h2>
            <p>Buscá por concepto o recorré las unidades en orden.</p>
          </div>
          <label class="search-control">
            <span>Buscar módulos</span>
            <input type="search" data-module-search placeholder="Ejemplo: faltantes, árboles, optimización">
          </label>
          <p class="search-status" role="status" aria-live="polite" data-module-count>15 módulos disponibles</p>
          {''.join(unit_sections)}
        </section>
        <section class="container callout-panel">
          <div>
            <p class="eyebrow">Proyecto transversal</p>
            <h2>De una pregunta a una recomendación defendible</h2>
            <p>El proyecto integrador acompaña el curso con hitos de formulación, evidencia, modelado, valor y comunicación.</p>
          </div>
          <a class="button primary" href="proyecto-integrador.html">Abrir proyecto integrador</a>
        </section>
        """
    ).strip()
    return shell(
        COURSE["title"],
        COURSE["description"],
        body,
        body_class="home",
    )


def program_page() -> str:
    unit_blocks = []
    for unit in UNITS:
        module_rows = []
        for module_id in unit["modules"]:
            module = MODULES_BY_ID[module_id]
            module_rows.append(
                dedent(
                    f"""
                    <tr>
                      <td><span class="module-number">Módulo {module['id']}</span></td>
                      <td><strong>{esc(module['title'])}</strong><br><small>{esc(module['summary'])}</small></td>
                      <td>{esc(module['duration'])}</td>
                      <td><a class="table-link" href="modulos/{module['slug']}/index.html">Abrir</a></td>
                    </tr>
                    """
                ).strip()
            )
        unit_blocks.append(
            dedent(
                f"""
                <section class="content-section" id="{unit['id']}">
                  <p class="eyebrow">Unidad {unit['number']}</p>
                  <h2>{esc(unit['title'])}</h2>
                  <p>{esc(unit['question'])}</p>
                  <div class="table-wrap">
                    <table>
                      <thead><tr><th>Módulo</th><th>Contenido</th><th>Dedicación orientativa</th><th>Acceso</th></tr></thead>
                      <tbody>{''.join(module_rows)}</tbody>
                    </table>
                  </div>
                </section>
                """
            ).strip()
        )
    body = dedent(
        f"""
        <section class="page-hero compact">
          <div class="container narrow">
            <p class="breadcrumbs"><a href="index.html">Inicio</a> / Programa</p>
            <p class="eyebrow">Recorrido académico</p>
            <h1>Programa por capacidades</h1>
            <p class="hero-lead">La secuencia conserva los temas mínimos del curso y suma las capacidades necesarias para diseñar decisiones confiables.</p>
          </div>
        </section>
        <div class="container content-layout">
          <aside class="toc">
            <strong>En esta página</strong>
            <a href="#resultados">Resultados</a>
            {''.join(f'<a href="#{u["id"]}">Unidad {u["number"]}</a>' for u in UNITS)}
            <a href="#incorporaciones">Contenidos incorporados</a>
          </aside>
          <div class="content-column">
            <section id="resultados" class="content-section">
              <p class="eyebrow">Resultados de aprendizaje</p>
              <h2>Al finalizar el recorrido</h2>
              <div class="outcome-grid">
                <article><span>01</span><h3>Formular</h3><p>Convertir necesidades en decisiones, unidades, horizontes y métricas.</p></article>
                <article><span>02</span><h3>Construir evidencia</h3><p>Auditar y preparar datos con trazabilidad y sin leakage.</p></article>
                <article><span>03</span><h3>Modelar</h3><p>Seleccionar y validar métodos predictivos, descriptivos y prescriptivos.</p></article>
                <article><span>04</span><h3>Decidir</h3><p>Traducir métricas a costos, capacidad, riesgo y valor esperado.</p></article>
                <article><span>05</span><h3>Gobernar</h3><p>Explicar, documentar y monitorear impacto y desempeño.</p></article>
                <article><span>06</span><h3>Comunicar</h3><p>Defender una recomendación con límites y próximos pasos.</p></article>
              </div>
            </section>
            {''.join(unit_blocks)}
            <section id="incorporaciones" class="content-section">
              <p class="eyebrow">Cobertura ampliada</p>
              <h2>Temas necesarios para completar el ciclo</h2>
              <div class="comparison-grid">
                <article><h3>Antes de modelar</h3><p>Decisión, unidad de análisis, calidad, leakage, encoding, pipelines y baselines.</p></article>
                <article><h3>Al evaluar</h3><p>Particiones por grupo o tiempo, calibración, costos de error, estabilidad e incertidumbre.</p></article>
                <article><h3>Al decidir</h3><p>Optimización, restricciones, valor esperado, experimentación y análisis de sensibilidad.</p></article>
                <article><h3>Al operar</h3><p>Interpretabilidad, equidad, documentación, monitoreo, drift y supervisión humana.</p></article>
              </div>
            </section>
          </div>
        </div>
        """
    ).strip()
    return shell(
        "Programa",
        "Programa completo organizado por capacidades y módulos.",
        body,
    )


def capstone_page() -> str:
    body = dedent(
        f"""
        <section class="page-hero compact">
          <div class="container narrow">
            <p class="breadcrumbs"><a href="index.html">Inicio</a> / Proyecto integrador</p>
            <p class="eyebrow">Trabajo transversal</p>
            <h1>Proyecto integrador de decisión</h1>
            <p class="hero-lead">Un producto analítico no termina en una métrica: culmina en una recomendación reproducible, evaluable y responsable.</p>
            <div class="button-row">
              <a class="button primary" href="modulos/14-proyecto-integrador/index.html">Abrir módulo</a>
              <a class="button secondary" href="{REPO_URL}/blob/main/projects/capstone/README.md">Ver consignas</a>
            </div>
          </div>
        </section>
        <section class="container content-section">
          <div class="section-heading"><p class="eyebrow">Hitos</p><h2>Cuatro decisiones de proyecto</h2></div>
          <div class="timeline">
            <article><span>01</span><div><h3>Encuadre</h3><p>Decisión, stakeholder, unidad de análisis, horizonte, acción, métrica y riesgo.</p><strong>Salida: canvas y contrato de datos.</strong></div></article>
            <article><span>02</span><div><h3>Evidencia</h3><p>Calidad, EDA, faltantes, extremos, baseline y protocolo de validación.</p><strong>Salida: entrega parcial reproducible.</strong></div></article>
            <article><span>03</span><div><h3>Alternativas</h3><p>Pipeline, modelos, evaluación, umbral o política, valor y análisis de sensibilidad.</p><strong>Salida: entrega final y ficha de modelo.</strong></div></article>
            <article><span>04</span><div><h3>Defensa</h3><p>Recomendación, incertidumbre, límites, impacto, monitoreo y próximos pasos.</p><strong>Salida: exposición ejecutiva.</strong></div></article>
          </div>
        </section>
        <section class="container content-section">
          <div class="section-heading"><p class="eyebrow">Evaluación</p><h2>Rúbrica de cien puntos</h2></div>
          <div class="rubric-grid">
            <article><strong>15</strong><h3>Problema y decisión</h3><p>Encuadre, unidad, horizonte, acción y éxito.</p></article>
            <article><strong>15</strong><h3>Datos y calidad</h3><p>Trazabilidad, diccionario, sesgos y controles.</p></article>
            <article><strong>15</strong><h3>EDA y baseline</h3><p>Hallazgos relevantes y referencia defendible.</p></article>
            <article><strong>20</strong><h3>Modelado</h3><p>Pipeline, alternativas y justificación técnica.</p></article>
            <article><strong>15</strong><h3>Evaluación y valor</h3><p>Validación honesta, costos y sensibilidad.</p></article>
            <article><strong>10</strong><h3>Responsabilidad</h3><p>Límites, equidad, explicación y monitoreo.</p></article>
            <article><strong>10</strong><h3>Comunicación</h3><p>Narrativa, visualización, repositorio y defensa.</p></article>
          </div>
          <p class="rubric-total">Total: 100 puntos</p>
        </section>
        <section class="container callout-panel">
          <div><p class="eyebrow">Plantillas</p><h2>Empezar con una estructura verificable</h2><p>El repositorio incluye canvas, checklist, rúbrica e informe final para que todos los equipos documenten con el mismo estándar.</p></div>
          <a class="button primary" href="{REPO_URL}/tree/main/projects/capstone/templates">Abrir plantillas</a>
        </section>
        """
    ).strip()
    return shell(
        "Proyecto integrador",
        "Hitos, entregables y rúbrica del proyecto integrador.",
        body,
    )


def deepening_page() -> str:
    tracks = [
        (
            "Experimentación y causalidad",
            "A/B testing, efectos heterogéneos, supuestos causales y diferencia entre riesgo y efecto de tratamiento.",
            "Módulo 13",
        ),
        (
            "Gradient boosting",
            "Ensambles secuenciales, regularización, early stopping y comparación con bosques.",
            "Módulo 09",
        ),
        (
            "Secuencias y atención",
            "RNN, LSTM, GRU y Transformers para series, texto y datos secuenciales.",
            "Módulo 11",
        ),
        (
            "Representaciones",
            "PCA, embeddings y autoencoders para compresión, visualización y anomalías.",
            "Módulos 10 y 11",
        ),
        (
            "IA generativa",
            "Evaluación de respuestas, recuperación de información, seguridad, costo y supervisión.",
            "Módulos 11 y 13",
        ),
        (
            "MLOps y monitoreo",
            "Registro de experimentos, pruebas de datos, drift, observabilidad y respuesta a incidentes.",
            "Módulo 13",
        ),
    ]
    cards = "\n".join(
        dedent(
            f"""
            <article class="track-card">
              <span>{index:02d}</span>
              <h2>{esc(title)}</h2>
              <p>{esc(text)}</p>
              <strong>{esc(where)}</strong>
            </article>
            """
        ).strip()
        for index, (title, text, where) in enumerate(tracks, start=1)
    )
    body = dedent(
        f"""
        <section class="page-hero compact">
          <div class="container narrow">
            <p class="breadcrumbs"><a href="index.html">Inicio</a> / Profundizaciones</p>
            <p class="eyebrow">Rutas posteriores y temas transversales</p>
            <h1>Profundizaciones con criterio de uso</h1>
            <p class="hero-lead">Cada ruta parte de una capacidad ya construida y explicita qué problema resuelve, qué exige y cómo debe evaluarse.</p>
          </div>
        </section>
        <section class="container content-section">
          <div class="track-grid">{cards}</div>
        </section>
        <section class="container note-panel">
          <h2>Regla de selección</h2>
          <p>Una técnica avanzada se incorpora cuando mejora una decisión bajo evidencia fuera de muestra y su costo, riesgo y mantenimiento son aceptables. Complejidad no es sinónimo de valor.</p>
        </section>
        """
    ).strip()
    return shell(
        "Profundizaciones",
        "Rutas de profundización en machine learning, causalidad e inteligencia artificial.",
        body,
    )


def accessibility_page() -> str:
    body = dedent(
        """
        <section class="page-hero compact">
          <div class="container narrow">
            <p class="breadcrumbs"><a href="index.html">Inicio</a> / Accesibilidad</p>
            <p class="eyebrow">Uso inclusivo</p>
            <h1>Accesibilidad y funcionamiento</h1>
            <p class="hero-lead">El sitio está diseñado para teclado, lectores de pantalla, contraste alto, dispositivos móviles y reducción de movimiento.</p>
          </div>
        </section>
        <section class="container prose content-section">
          <h2>Características</h2>
          <ul>
            <li>Jerarquía semántica, enlace para saltar contenido y regiones con nombres.</li>
            <li>Controles con etiquetas visibles, foco claro y resultados anunciados.</li>
            <li>Gráficos SVG acompañados por métricas y explicaciones textuales.</li>
            <li>Tema claro u oscuro según preferencia local.</li>
            <li>Movimiento reducido cuando el sistema lo solicita.</li>
            <li>Simulaciones sin dependencias externas y utilizables sin conexión luego de descargar el repositorio.</li>
          </ul>
          <h2>Atajos de estudio</h2>
          <p>La tecla Tab recorre enlaces y controles. Enter o Espacio activa botones. En cuestionarios, las opciones son controles de formulario estándar.</p>
          <h2>Reportar una barrera</h2>
          <p>Describí la página, el navegador, la tecnología de asistencia y el resultado esperado en un issue del repositorio.</p>
        </section>
        """
    ).strip()
    return shell(
        "Accesibilidad",
        "Características de accesibilidad y uso del curso.",
        body,
    )


def module_index(module: dict) -> str:
    theory_cards = "\n".join(
        dedent(
            f"""
            <article class="theory-card">
              <span>{index:02d}</span>
              <div><h3>{esc(section['title'])}</h3><p>{esc(section['text'])}</p></div>
            </article>
            """
        ).strip()
        for index, section in enumerate(module["theory"], start=1)
    )
    outcomes = "\n".join(f"<li>{esc(item)}</li>" for item in module["objectives"])
    lab_steps = "\n".join(
        f"<li><span>{index:02d}</span>{esc(item)}</li>"
        for index, item in enumerate(module["lab_steps"], start=1)
    )
    advanced_cards = "\n".join(
        dedent(
            f"""
            <article class="advanced-card">
              <span>{index:02d}</span>
              <p>{esc(topic)}</p>
            </article>
            """
        ).strip()
        for index, topic in enumerate(module["advanced_topics"], start=1)
    )
    failure_items = "\n".join(
        f"<li>{esc(item)}</li>" for item in module["common_failures"]
    )
    external_buttons = "".join(
        (
            f'\n                <a class="button tertiary" href="{esc(resource["url"])}">'
            f'{esc(resource["label"])}</a>'
        )
        for resource in module.get("external_resources", [])
    )
    current_index = MODULES.index(module)
    previous_link = (
        f'<a class="module-nav-link previous" href="../{MODULES[current_index - 1]["slug"]}/index.html">'
        f'<small>Módulo anterior</small><strong>{esc(MODULES[current_index - 1]["short_title"])}</strong></a>'
        if current_index > 0
        else '<a class="module-nav-link previous" href="../../index.html"><small>Volver</small><strong>Índice general</strong></a>'
    )
    next_link = (
        f'<a class="module-nav-link next" href="../{MODULES[current_index + 1]["slug"]}/index.html">'
        f'<small>Módulo siguiente</small><strong>{esc(MODULES[current_index + 1]["short_title"])}</strong></a>'
        if current_index < len(MODULES) - 1
        else '<a class="module-nav-link next" href="../../proyecto-integrador.html"><small>Cierre</small><strong>Proyecto integrador</strong></a>'
    )
    progress_resources = [
        ("guia", "Guía conceptual", "Comprender propósito y conceptos"),
        ("simulacion", "Simulación", "Explorar parámetros y resultados"),
        ("notebook", "Notebook", "Aplicar con Python"),
        ("cuestionario", "Cuestionario", "Comprobar comprensión"),
        ("glosario", "Glosario", "Consolidar vocabulario"),
    ]
    progress_resources.extend(
        (
            f"externo-{index}",
            resource["label"],
            "Completar laboratorio complementario",
        )
        for index, resource in enumerate(
            module.get("external_resources", []), start=1
        )
    )
    progress_resources.extend(
        (
            f"local-{index}",
            resource["label"],
            "Completar profundización interactiva",
        )
        for index, resource in enumerate(
            module.get("local_resources", []), start=1
        )
    )
    checklist = "\n".join(
        dedent(
            f"""
            <label class="progress-item">
              <input type="checkbox" data-progress-item="{module['id']}:{key}">
              <span><strong>{label}</strong><small>{detail}</small></span>
            </label>
            """
        ).strip()
        for key, label, detail in progress_resources
    )
    body = dedent(
        f"""
        <section class="module-hero">
          <div class="container">
            <p class="breadcrumbs"><a href="../../index.html">Inicio</a> / <a href="../../programa.html">Programa</a> / Módulo {module['id']}</p>
            <div class="module-hero-grid">
              <div>
                <p class="eyebrow">Módulo {module['id']} · Unidad {module['unit']}</p>
                <h1>{esc(module['title'])}</h1>
                <p class="hero-lead">{esc(module['summary'])}</p>
                <div class="module-facts">
                  <span><strong>Dedicación</strong>{esc(module['duration'])}</span>
                  <span><strong>Requisitos</strong>{esc(module['prerequisites'])}</span>
                </div>
              </div>
              <aside class="question-card">
                <span>Pregunta de decisión</span>
                <p>{esc(module['business_question'])}</p>
              </aside>
            </div>
          </div>
        </section>
        <div class="container module-layout">
          <aside class="module-sidebar">
            <div class="sidebar-block">
              <strong>Progreso del módulo</strong>
              <div class="mini-progress"><span data-module-progress-bar></span></div>
              <p><span data-module-progress>0</span> de {len(progress_resources)} recursos</p>
            </div>
            <nav aria-label="Secciones del módulo">
              <a href="#indice">Índice interactivo</a>
              <a href="#resultados">Resultados</a>
              <a href="#conceptos">Conceptos</a>
              <a href="#profundizacion">Profundización</a>
              <a href="#caso">Caso de negocio</a>
              <a href="#laboratorio">Laboratorio</a>
              <a href="#desafio">Desafío</a>
              <a href="#entregable">Entregable</a>
            </nav>
          </aside>
          <div class="module-content">
            <section id="indice" class="content-section first">
              <div class="section-heading">
                <p class="eyebrow">Centro del módulo</p>
                <h2>Índice interactivo</h2>
                <p>Abrí cada recurso y marcá el avance. El estado se conserva en tu navegador.</p>
              </div>
              {resource_table(module)}
              <div class="progress-checklist">{checklist}</div>
            </section>
            <section id="resultados" class="content-section">
              <p class="eyebrow">Al completar el módulo</p>
              <h2>Resultados de aprendizaje</h2>
              <ul class="check-list">{outcomes}</ul>
            </section>
            <section id="conceptos" class="content-section">
              <p class="eyebrow">Marco conceptual</p>
              <h2>Ideas que organizan la práctica</h2>
              <div class="theory-list">{theory_cards}</div>
            </section>
            <section id="profundizacion" class="content-section">
              <p class="eyebrow">Nivel profesional</p>
              <h2>Profundización aplicada</h2>
              <p class="section-intro">Estos temas conectan el fundamento con decisiones modernas, evaluación rigurosa y operación real.</p>
              <div class="advanced-grid">{advanced_cards}</div>
              <div class="failure-panel">
                <div>
                  <p class="eyebrow">Control de calidad</p>
                  <h3>Errores frecuentes que invalidan la conclusión</h3>
                </div>
                <ul>{failure_items}</ul>
              </div>
            </section>
            <section id="caso" class="content-section">
              <div class="case-panel">
                <p class="eyebrow">Caso de negocio</p>
                <h2>Decidir con contexto</h2>
                <p>{esc(module['case'])}</p>
                <a class="text-link" href="simulacion.html">Explorar en la simulación <span aria-hidden="true">-&gt;</span></a>
              </div>
            </section>
            <section id="laboratorio" class="content-section">
              <p class="eyebrow">Práctica guiada</p>
              <h2>Secuencia de laboratorio</h2>
              <ol class="step-list">{lab_steps}</ol>
              <div class="button-row">
                <a class="button primary" href="{notebook_url(module)}">Abrir notebook en Colab</a>
                <a class="button secondary" href="cuestionario.html">Resolver cuestionario</a>{external_buttons}
              </div>
            </section>
            <section id="desafio" class="content-section">
              <div class="challenge-panel">
                <span>Desafío de transferencia</span>
                <h2>Tomar una decisión defendible</h2>
                <p>{esc(module['decision_challenge'])}</p>
                <ol>
                  <li>Escribí una hipótesis antes de calcular.</li>
                  <li>Definí la evidencia que podría refutarla.</li>
                  <li>Compará al menos dos escenarios.</li>
                  <li>Terminá con acción, límite y responsable.</li>
                </ol>
              </div>
            </section>
            <section id="entregable" class="content-section">
              <div class="deliverable-panel">
                <span>Producto del módulo</span>
                <h2>Entregable esperado</h2>
                <p>{esc(module['deliverable'])}</p>
              </div>
            </section>
            <nav class="module-pagination" aria-label="Navegación entre módulos">
              {previous_link}{next_link}
            </nav>
          </div>
        </div>
        """
    ).strip()
    return shell(
        module["title"],
        module["summary"],
        body,
        prefix="../../",
        body_class="module-page",
        extra_scripts=["module.js"],
        data_attrs=f'data-module-id="{module["id"]}" data-page-kind="index"',
    )


def simulation_page(module: dict) -> str:
    body = dedent(
        f"""
        <section class="page-hero simulation-hero compact">
          <div class="container narrow">
            <p class="breadcrumbs"><a href="../../index.html">Inicio</a> / <a href="index.html">Módulo {module['id']}</a> / Simulación</p>
            <p class="eyebrow">Laboratorio interactivo · Módulo {module['id']}</p>
            <h1>{esc(module['simulation_title'])}</h1>
            <p class="hero-lead">{esc(module['simulation_instruction'])}</p>
          </div>
        </section>
        <section class="container simulation-section">
          <noscript><p class="alert">Esta simulación necesita JavaScript habilitado.</p></noscript>
          <div id="simulation-root" class="simulation-root" data-simulation="{module['id']}"
               data-challenge="{esc(module['decision_challenge'])}" aria-live="polite"></div>
          <div class="reflection-panel">
            <p class="eyebrow">Método de trabajo</p>
            <h2>Lectura de resultados</h2>
            <ol>
              <li>Formulá una hipótesis antes de mover un control.</li>
              <li>Guardá un escenario A y un escenario B para comparar evidencia.</li>
              <li>Interpretá la métrica en costo, capacidad, riesgo o valor.</li>
              <li>Registrá una recomendación, una limitación y el próximo dato necesario.</li>
            </ol>
          </div>
          <p class="simulation-author">Material elaborado por el profesor {esc(COURSE['author'])}.</p>
          <div class="button-row centered">
            <a class="button secondary" href="index.html">Volver a la guía</a>
            <a class="button primary" href="cuestionario.html">Continuar al cuestionario</a>
          </div>
        </section>
        """
    ).strip()
    return shell(
        module["simulation_title"],
        module["simulation_instruction"],
        body,
        prefix="../../",
        body_class="simulation-page",
        extra_scripts=["simulations.js", "module.js"],
        data_attrs=f'data-module-id="{module["id"]}" data-page-kind="simulacion"',
    )


def glossary_page(module: dict) -> str:
    entries = "\n".join(
        dedent(
            f"""
            <article class="glossary-entry" data-glossary-entry
                     data-search="{esc((term + ' ' + definition).lower())}">
              <h2>{esc(term)}</h2>
              <p>{esc(definition)}</p>
            </article>
            """
        ).strip()
        for term, definition in module["glossary"]
    )
    body = dedent(
        f"""
        <section class="page-hero compact">
          <div class="container narrow">
            <p class="breadcrumbs"><a href="../../index.html">Inicio</a> / <a href="index.html">Módulo {module['id']}</a> / Glosario</p>
            <p class="eyebrow">Referencia interactiva · Módulo {module['id']}</p>
            <h1>Glosario: {esc(module['short_title'])}</h1>
            <p class="hero-lead">Diez conceptos esenciales con definiciones breves y contextualizadas.</p>
          </div>
        </section>
        <section class="container glossary-section">
          <label class="search-control">
            <span>Buscar término o definición</span>
            <input type="search" data-glossary-search placeholder="Escribí para filtrar">
          </label>
          <p class="search-status" role="status" aria-live="polite" data-glossary-count>10 términos</p>
          <div class="glossary-grid">{entries}</div>
          <div class="button-row centered">
            <a class="button secondary" href="index.html">Volver a la guía</a>
            <a class="button primary" href="cuestionario.html">Resolver cuestionario</a>
          </div>
        </section>
        """
    ).strip()
    return shell(
        f"Glosario: {module['short_title']}",
        f"Glosario interactivo del módulo {module['title']}.",
        body,
        prefix="../../",
        body_class="glossary-page",
        extra_scripts=["module.js"],
        data_attrs=f'data-module-id="{module["id"]}" data-page-kind="glosario"',
    )


def quiz_page(module: dict) -> str:
    questions = []
    for index, item in enumerate(module["quiz"], start=1):
        options = []
        for option_index, option in enumerate(item["options"]):
            options.append(
                dedent(
                    f"""
                    <label class="quiz-option">
                      <input type="radio" name="question-{index}" value="{option_index}">
                      <span><b>{chr(64 + option_index + 1)}</b>{esc(option)}</span>
                    </label>
                    """
                ).strip()
            )
        questions.append(
            dedent(
                f"""
                <fieldset class="quiz-question" data-question data-answer="{item['answer']}"
                          data-explanation="{esc(item['explanation'])}">
                  <legend><span>{index:02d}</span>{esc(item['question'])}</legend>
                  <div class="quiz-options">{''.join(options)}</div>
                  <p class="question-feedback" data-question-feedback aria-live="polite"></p>
                </fieldset>
                """
            ).strip()
        )
    body = dedent(
        f"""
        <section class="page-hero compact">
          <div class="container narrow">
            <p class="breadcrumbs"><a href="../../index.html">Inicio</a> / <a href="index.html">Módulo {module['id']}</a> / Cuestionario</p>
            <p class="eyebrow">Autoevaluación · Módulo {module['id']}</p>
            <h1>Cuestionario: {esc(module['short_title'])}</h1>
            <p class="hero-lead">{len(module['quiz'])} preguntas conceptuales y situacionales con corrección inmediata, explicación y segundo intento.</p>
          </div>
        </section>
        <section class="container quiz-section">
          <form class="quiz-form" data-quiz novalidate>
            {''.join(questions)}
            <div class="quiz-actions">
              <button class="button primary" type="submit">Corregir respuestas</button>
              <button class="button secondary" type="reset">Reiniciar</button>
            </div>
          </form>
          <div class="quiz-result" data-quiz-result hidden tabindex="-1">
            <span>Resultado</span>
            <strong data-quiz-score>0 / {len(module['quiz'])}</strong>
            <p data-quiz-message></p>
            <a class="button primary" href="glosario.html">Revisar glosario</a>
          </div>
          <div class="button-row centered">
            <a class="button secondary" href="simulacion.html">Volver a la simulación</a>
            <a class="button tertiary" href="index.html">Índice del módulo</a>
          </div>
        </section>
        """
    ).strip()
    return shell(
        f"Cuestionario: {module['short_title']}",
        f"Cuestionario interactivo del módulo {module['title']}.",
        body,
        prefix="../../",
        body_class="quiz-page",
        extra_scripts=["module.js"],
        data_attrs=f'data-module-id="{module["id"]}" data-page-kind="cuestionario"',
    )


def module_readme(module: dict) -> str:
    objective_lines = "\n        ".join(f"- {item}" for item in module["objectives"])
    advanced_lines = "\n        ".join(
        f"- {item}" for item in module["advanced_topics"]
    )
    failure_lines = "\n        ".join(
        f"- {item}" for item in module["common_failures"]
    )
    steps = "\n        ".join(
        f"{index}. {item}" for index, item in enumerate(module["lab_steps"], start=1)
    )
    resources = [
        ("Guía principal", module_url(module)),
        ("Simulación interactiva", module_url(module, "simulacion.html")),
        ("Cuestionario", module_url(module, "cuestionario.html")),
        ("Glosario", module_url(module, "glosario.html")),
        ("Notebook en Colab", notebook_url(module)),
    ]
    resources.extend(
        (resource["label"], resource["url"])
        for resource in module.get("external_resources", [])
    )
    resources.extend(
        (resource["label"], module_url(module, resource["url"]))
        for resource in module.get("local_resources", [])
    )
    rows = "\n        ".join(
        f"| {label} | [Abrir]({url}) |" for label, url in resources
    )
    return dedent(
        f"""
        # Módulo {module['id']}: {module['title']}

        {module['summary']}

        ## Pregunta de decisión

        {module['business_question']}

        ## Índice interactivo

        | Recurso | Acceso |
        |---|---|
        {rows}

        ## Resultados de aprendizaje

        {objective_lines}

        ## Caso de negocio

        {module['case']}

        ## Profundización aplicada

        {advanced_lines}

        ## Errores frecuentes

        {failure_lines}

        ## Desafío de transferencia

        {module['decision_challenge']}

        ## Secuencia de práctica

        {steps}

        ## Entregable

        {module['deliverable']}

        ## Autoría

        Material elaborado por el profesor {COURSE['author']}.
        """
    ).strip()


NOTEBOOK_CODE = {
    "00": """
import random
import numpy as np
import pandas as pd

SEED = 42
random.seed(SEED)
np.random.seed(SEED)

clientes = pd.DataFrame({
    "cliente_id": range(1, 11),
    "antiguedad_meses": np.random.randint(1, 60, 10),
    "compras_90d": np.random.poisson(4, 10),
})
clientes.assign(
    compras_por_mes=lambda df: df["compras_90d"] / 3
).head()
""",
    "01": """
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)
ventas = pd.DataFrame({
    "canal": rng.choice(["Tienda", "Web", "Marketplace"], 300, p=[0.45, 0.35, 0.20]),
    "ticket": rng.lognormal(mean=3.8, sigma=0.55, size=300),
    "frecuencia": rng.poisson(3, 300),
})
display(ventas.describe(include="all"))
ventas.groupby("canal")["ticket"].agg(["count", "median", "mean"])
""",
    "02": """
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer

rng = np.random.default_rng(42)
datos = pd.DataFrame({
    "ocupacion": rng.choice(["Dependiente", "Independiente"], 200),
    "ingreso": rng.lognormal(11, 0.4, 200),
})
mask = (datos["ocupacion"].eq("Independiente") & (rng.random(200) < 0.35)) | (rng.random(200) < 0.05)
datos.loc[mask, "ingreso"] = np.nan
datos["ingreso_faltante"] = datos["ingreso"].isna().astype(int)
datos.groupby("ocupacion")["ingreso_faltante"].mean()
""",
    "03": """
import numpy as np
import pandas as pd

ventas = pd.Series([82, 91, 95, 97, 101, 104, 108, 110, 118, 540], name="ticket")
q1, q3 = ventas.quantile([0.25, 0.75])
iqr = q3 - q1
limite_inferior, limite_superior = q1 - 1.5 * iqr, q3 + 1.5 * iqr
diagnostico = pd.DataFrame({
    "ticket": ventas,
    "outlier_iqr": ~ventas.between(limite_inferior, limite_superior),
})
display(diagnostico)
print({"media": ventas.mean(), "mediana": ventas.median()})
""",
    "04": """
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

numeric = ["antiguedad", "ingreso"]
categorical = ["canal"]
preprocess = ColumnTransformer([
    ("num", Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ]), numeric),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
])
preprocess
""",
    "05": """
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(42)
x = rng.uniform(0, 20, 120)
y = 35 + 4.2 * x + rng.normal(0, 10, 120)
X_train, X_test, y_train, y_test = train_test_split(
    x.reshape(-1, 1), y, test_size=0.25, random_state=42
)
model = LinearRegression().fit(X_train, y_train)
pred = model.predict(X_test)
pd.Series({
    "intercepto": model.intercept_,
    "pendiente": model.coef_[0],
    "MAE_test": mean_absolute_error(y_test, pred),
    "RMSE_test": mean_squared_error(y_test, pred) ** 0.5,
    "R2_test": r2_score(y_test, pred),
})
""",
    "06": """
import numpy as np
from sklearn.datasets import make_regression
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold, cross_validate

X, y = make_regression(n_samples=300, n_features=8, noise=20, random_state=42)
cv = KFold(n_splits=5, shuffle=True, random_state=42)
for name, model in {"baseline": DummyRegressor(), "ridge": Ridge(alpha=1)}.items():
    scores = cross_validate(model, X, y, cv=cv, scoring="neg_mean_absolute_error")
    mae = -scores["test_score"]
    print(name, {"media": mae.mean().round(2), "desvio": mae.std().round(2)})
""",
    "07": """
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
fecha = pd.date_range("2021-01-01", periods=72, freq="MS")
t = np.arange(len(fecha))
serie = pd.Series(100 + 1.2*t + 18*np.sin(2*np.pi*t/12) + rng.normal(0, 5, len(t)), index=fecha)
tabla = pd.DataFrame({"real": serie})
tabla["naive"] = tabla["real"].shift(1)
tabla["estacional"] = tabla["real"].shift(12)
tabla["error_naive"] = (tabla["real"] - tabla["naive"]).abs()
tabla["error_estacional"] = (tabla["real"] - tabla["estacional"]).abs()
tabla.tail(18)
""",
    "08": """
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=600, weights=[0.8, 0.2], random_state=42)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, stratify=y, random_state=42
)
model = LogisticRegression(max_iter=1000).fit(X_train, y_train)
prob = model.predict_proba(X_test)[:, 1]
rows = []
for threshold in [0.2, 0.4, 0.6, 0.8]:
    pred = (prob >= threshold).astype(int)
    rows.append({
        "umbral": threshold,
        "precision": precision_score(y_test, pred, zero_division=0),
        "recall": recall_score(y_test, pred),
        "positivos_seleccionados": pred.sum(),
    })
display(pd.DataFrame(rows))
print({"ROC_AUC_test": roc_auc_score(y_test, prob), "Brier_test": brier_score_loss(y_test, prob)})
""",
    "09": """
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.model_selection import cross_validate, StratifiedKFold
from sklearn.tree import DecisionTreeClassifier

X, y = make_classification(n_samples=800, n_features=12, n_informative=6, random_state=42)
models = {
    "arbol": DecisionTreeClassifier(max_depth=4, random_state=42),
    "bosque": RandomForestClassifier(n_estimators=200, random_state=42),
    "boosting": GradientBoostingClassifier(random_state=42),
}
cv = StratifiedKFold(5, shuffle=True, random_state=42)
pd.DataFrame({
    name: cross_validate(model, X, y, cv=cv, scoring="roc_auc")["test_score"]
    for name, model in models.items()
}).agg(["mean", "std"])
""",
}


NOTEBOOK_VISUALIZATION = {
    "00": """
import matplotlib.pyplot as plt

ax = clientes.set_index("cliente_id")["compras_90d"].plot.bar(
    figsize=(8, 3), color="#0f766e", title="Compras por cliente"
)
ax.set(xlabel="Cliente", ylabel="Compras en 90 días")
plt.tight_layout()
""",
    "01": """
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(10, 3.5))
ventas["ticket"].plot.hist(bins=24, ax=axes[0], color="#0f766e", edgecolor="white")
axes[0].axvline(ventas["ticket"].median(), color="#b45309", label="Mediana")
axes[0].set(title="Distribución de ticket", xlabel="Ticket", ylabel="Frecuencia")
axes[0].legend()
ventas.boxplot(column="ticket", by="canal", ax=axes[1], grid=False)
axes[1].set(title="Ticket por canal", xlabel="Canal", ylabel="Ticket")
fig.suptitle("")
plt.tight_layout()
""",
    "02": """
import matplotlib.pyplot as plt

faltantes = datos.groupby("ocupacion")["ingreso_faltante"].mean().sort_values()
ax = faltantes.mul(100).plot.barh(figsize=(7, 3), color="#b45309")
ax.set(xlabel="Ingreso faltante (%)", ylabel="Ocupación", title="Ausencia condicionada por ocupación")
plt.tight_layout()
""",
    "03": """
import matplotlib.pyplot as plt

colors = diagnostico["outlier_iqr"].map({True: "#be123c", False: "#0f766e"})
fig, ax = plt.subplots(figsize=(8, 3))
ax.scatter(diagnostico.index, diagnostico["ticket"], c=colors, s=70)
ax.axhline(limite_superior, color="#b45309", linestyle="--", label="Límite IQR")
ax.set(xlabel="Observación", ylabel="Ticket", title="Extremos con contexto")
ax.legend()
plt.tight_layout()
""",
    "04": """
import matplotlib.pyplot as plt

demo = pd.DataFrame({
    "antiguedad": [3, 12, np.nan, 42],
    "ingreso": [450, 820, 610, 1300],
    "canal": ["Web", "Tienda", "Web", "Marketplace"],
})
matrix = preprocess.fit_transform(demo)
matrix = matrix.toarray() if hasattr(matrix, "toarray") else matrix
fig, ax = plt.subplots(figsize=(8, 3))
image = ax.imshow(matrix, aspect="auto", cmap="viridis")
ax.set(xlabel="Características transformadas", ylabel="Filas", title="Salida del pipeline")
fig.colorbar(image, ax=ax, shrink=.75)
plt.tight_layout()
""",
    "05": """
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(10, 3.5))
axes[0].scatter(y_test, pred, color="#0f766e")
limits = [min(y_test.min(), pred.min()), max(y_test.max(), pred.max())]
axes[0].plot(limits, limits, "--", color="#b45309")
axes[0].set(xlabel="Real", ylabel="Predicción", title="Generalización fuera de muestra")
residuos = y_test - pred
axes[1].scatter(pred, residuos, color="#1d4ed8")
axes[1].axhline(0, color="#b45309", linestyle="--")
axes[1].set(xlabel="Predicción", ylabel="Residuo", title="Diagnóstico de residuos")
plt.tight_layout()
""",
    "06": """
import matplotlib.pyplot as plt

scores = cross_validate(Ridge(alpha=1), X, y, cv=cv, scoring="neg_mean_absolute_error")
mae_folds = -scores["test_score"]
fig, ax = plt.subplots(figsize=(7, 3))
ax.bar(range(1, len(mae_folds) + 1), mae_folds, color="#0f766e")
ax.axhline(mae_folds.mean(), color="#b45309", linestyle="--", label="Media")
ax.set(xlabel="Fold", ylabel="MAE", title="Variabilidad de la evaluación")
ax.legend()
plt.tight_layout()
""",
    "07": """
import matplotlib.pyplot as plt

ax = tabla[["real", "naive", "estacional"]].tail(30).plot(figsize=(10, 4))
ax.set(xlabel="Mes", ylabel="Ventas", title="Pronóstico contra baselines")
plt.tight_layout()
""",
    "08": """
import matplotlib.pyplot as plt
from sklearn.calibration import CalibrationDisplay
from sklearn.metrics import PrecisionRecallDisplay

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
CalibrationDisplay.from_predictions(y_test, prob, n_bins=8, ax=axes[0])
axes[0].set_title("Confiabilidad de probabilidades")
PrecisionRecallDisplay.from_predictions(y_test, prob, ax=axes[1])
axes[1].set_title("Ranking con clase minoritaria")
plt.tight_layout()
""",
    "09": """
import matplotlib.pyplot as plt

cv_scores = pd.DataFrame({
    name: cross_validate(model, X, y, cv=cv, scoring="roc_auc")["test_score"]
    for name, model in models.items()
})
ax = cv_scores.plot.box(figsize=(8, 3.5), color={"boxes": "#0f766e", "medians": "#b45309"})
ax.set(ylabel="ROC-AUC", title="Desempeño y estabilidad por modelo")
plt.tight_layout()
""",
    "10": """
import matplotlib.pyplot as plt

score_table = pd.DataFrame(rows)
labels_4 = KMeans(n_clusters=4, n_init=20, random_state=42).fit_predict(X_scaled)
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].plot(score_table["k"], score_table["silhouette"], marker="o", color="#0f766e")
axes[0].set(xlabel="K", ylabel="Silhouette", title="Selección de K")
axes[1].scatter(X_scaled[:, 0], X_scaled[:, 1], c=labels_4, cmap="viridis", s=16)
axes[1].set(title="Solución K=4", xlabel="Variable escalada 1", ylabel="Variable escalada 2")
plt.tight_layout()
""",
    "11": """
import matplotlib.pyplot as plt

z = np.linspace(-7, 7, 300)
fig, ax = plt.subplots(figsize=(8, 3))
ax.plot(z, sigmoid(z), color="#0f766e", linewidth=3)
ax.axhline(.5, color="#b45309", linestyle="--")
ax.set(xlabel="Entrada ponderada", ylabel="Activación", title="Función sigmoide")
plt.tight_layout()
""",
    "12": """
import matplotlib.pyplot as plt

a = np.linspace(0, 60, 250)
b1 = 100 - 2 * a
b2 = (80 - a) / 2
fig, ax = plt.subplots(figsize=(7, 4))
ax.fill_between(a, 0, np.maximum(0, np.minimum(b1, b2)), color="#0f766e", alpha=.25)
ax.plot(a, b1, label="2A + B ≤ 100")
ax.plot(a, b2, label="A + 2B ≤ 80")
ax.scatter(resultado.x[0], resultado.x[1], color="#be123c", s=80, label="Óptimo")
ax.set(xlabel="Producto A", ylabel="Producto B", title="Región factible y solución")
ax.set_ylim(0, 60)
ax.legend()
plt.tight_layout()
""",
    "13": """
import matplotlib.pyplot as plt

group_metrics = pd.DataFrame([metricas("A"), metricas("B")]).set_index("grupo")
ax = group_metrics[["fpr", "fnr"]].plot.bar(figsize=(8, 3.5), color=["#1d4ed8", "#be123c"])
ax.set(ylabel="Tasa", title="Errores por grupo")
ax.set_ylim(0, 1)
plt.tight_layout()
""",
    "14": """
import matplotlib.pyplot as plt
import pandas as pd

scorecard = pd.Series({"Valor": 4, "Evidencia": 3, "Riesgo controlado": 2, "Factibilidad": 4})
ax = scorecard.sort_values().plot.barh(figsize=(8, 3), color="#0f766e")
ax.set(xlabel="Nivel (1-5)", title="Scorecard de preparación de la decisión", xlim=(0, 5))
plt.tight_layout()
""",
}


NOTEBOOK_DECISION = {
    "00": "pd.DataFrame({'control': ['pregunta', 'datos', 'dependencias', 'semilla', 'ejecución limpia'], 'estado': ['definido', 'validado', 'declarado', 'fijada', 'pendiente']})",
    "01": "ventas.groupby('canal').agg(ticket_mediano=('ticket', 'median'), frecuencia_media=('frecuencia', 'mean')).assign(prioridad=lambda x: x['ticket_mediano'] * x['frecuencia_media']).sort_values('prioridad', ascending=False)",
    "02": "pd.DataFrame({'estrategia': ['eliminar', 'mediana global', 'mediana por ocupación'], 'riesgo': ['sesgo por selección', 'oculta heterogeneidad', 'requiere validar estabilidad'], 'uso': ['solo baja ausencia', 'baseline', 'comparación recomendada']})",
    "03": "pd.DataFrame({'escenario': ['todos', 'sin extremo'], 'media': [ventas.mean(), ventas[~diagnostico['outlier_iqr']].mean()], 'mediana': [ventas.median(), ventas[~diagnostico['outlier_iqr']].median()]})",
    "04": "pd.DataFrame({'variable': ['antiguedad', 'ingreso', 'canal'], 'disponible_al_decidir': [True, True, True], 'transformación_aprendida_solo_en_train': [True, True, True]})",
    "05": "pd.DataFrame({'escenario': ['error medio', 'error adverso'], 'unidades_error': [np.abs(residuos).mean(), np.quantile(np.abs(residuos), .9)], 'costo_por_unidad': [8, 8]}).assign(costo=lambda x: x.unidades_error * x.costo_por_unidad)",
    "06": "pd.DataFrame({'criterio': ['MAE medio', 'desvío entre folds', 'latencia', 'valor'], 'ridge': [mae_folds.mean(), mae_folds.std(), 1, 4], 'baseline': [float(np.std(y)), 0, 1, 1]})",
    "07": "tabla[['error_naive', 'error_estacional']].tail(24).agg(['mean', lambda s: s.quantile(.9)]).rename(index={'<lambda>': 'p90'})",
    "08": "pd.DataFrame(rows).assign(valor_estimado=lambda d: d.recall * 30 - (1 - d.precision.fillna(0)) * 4).sort_values('valor_estimado', ascending=False)",
    "09": "pd.DataFrame({'modelo': ['árbol', 'bosque', 'boosting'], 'auc_media': cv_scores.mean().values, 'latencia_relativa': [1, 4, 6], 'explicabilidad': [5, 3, 3]}).sort_values('auc_media', ascending=False)",
    "10": "pd.DataFrame({'criterio': ['silhouette', 'estabilidad', 'alcanzabilidad', 'acción diferenciada'], 'evidencia_requerida': ['fuera de muestra', 'remuestreo', 'reglas de asignación', 'prueba de tratamiento']})",
    "11": "pd.DataFrame({'arquitectura': ['baseline lineal', 'RNN/GRU', 'Transformer/RAG'], 'calidad': [2, 3, 4], 'latencia': [5, 3, 2], 'trazabilidad': [5, 3, 4], 'costo': [5, 3, 2]})",
    "12": "pd.DataFrame([{'capacidad_A': cap, 'producto_A': linprog(c=[-40, -30], A_ub=[[2, 1], [1, 2]], b_ub=[cap, 80], bounds=[(0, None), (0, None)], method='highs').x[0]} for cap in [90, 100, 110]])",
    "13": "pd.concat([pd.DataFrame([metricas('A', u), metricas('B', u)]).assign(umbral=u) for u in [.4, .5, .6]], ignore_index=True)",
    "14": "pd.DataFrame({'dimensión': ['decisión', 'evidencia', 'valor', 'riesgo', 'operación'], 'pregunta_de_control': ['¿qué acción cambia?', '¿generaliza?', '¿supera la política actual?', '¿qué daño puede causar?', '¿quién responde?']})",
}


NOTEBOOK_CODE.update({
    "10": """
import pandas as pd
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.datasets import make_blobs
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

X, _ = make_blobs(n_samples=360, centers=4, cluster_std=[1.0, 1.8, 0.8, 1.3], random_state=42)
X_scaled = StandardScaler().fit_transform(X)
rows = []
for k in range(2, 7):
    labels = KMeans(n_clusters=k, n_init=20, random_state=42).fit_predict(X_scaled)
    rows.append({"k": k, "silhouette": silhouette_score(X_scaled, labels)})
pd.DataFrame(rows)
""",
    "11": """
import numpy as np
import pandas as pd

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

entradas = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
pesos = np.array([1.5, 1.5])
sesgo = -2.0
salida = sigmoid(entradas @ pesos + sesgo)
pd.DataFrame({
    "x1": entradas[:, 0],
    "x2": entradas[:, 1],
    "activacion": salida,
    "clase": (salida >= 0.5).astype(int),
})
""",
    "12": """
import numpy as np
import pandas as pd
from scipy.optimize import linprog

# Maximizar 40*A + 30*B equivale a minimizar el negativo.
resultado = linprog(
    c=[-40, -30],
    A_ub=[[2, 1], [1, 2]],
    b_ub=[100, 80],
    bounds=[(0, None), (0, None)],
    method="highs",
)
pd.Series({
    "producto_A": resultado.x[0],
    "producto_B": resultado.x[1],
    "beneficio": -resultado.fun,
    "factible": resultado.success,
})
""",
    "13": """
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix

rng = np.random.default_rng(42)
tabla = pd.DataFrame({
    "grupo": np.repeat(["A", "B"], 300),
    "real": np.r_[rng.binomial(1, 0.30, 300), rng.binomial(1, 0.45, 300)],
})
tabla["score"] = np.clip(0.15 + 0.62*tabla["real"] + rng.normal(0, 0.22, 600), 0, 1)

def metricas(grupo, umbral=0.5):
    subset = tabla.query("grupo == @grupo")
    pred = (subset["score"] >= umbral).astype(int)
    tn, fp, fn, tp = confusion_matrix(subset["real"], pred, labels=[0, 1]).ravel()
    return {"grupo": grupo, "seleccion": pred.mean(), "fpr": fp/(fp+tn), "fnr": fn/(fn+tp)}

pd.DataFrame([metricas("A"), metricas("B")])
""",
    "14": """
from dataclasses import dataclass

@dataclass
class CanvasDecision:
    decision: str
    unidad: str
    horizonte: str
    accion: str
    metrica: str
    baseline: str

canvas = CanvasDecision(
    decision="Priorizar contactos de retención",
    unidad="Cliente activo al cierre de mes",
    horizonte="Cancelación en 30 días",
    accion="Oferta o llamada",
    metrica="Valor neto incremental",
    baseline="Política actual",
)
canvas
""",
})


def notebook(module: dict) -> dict:
    colab_badge = (
        f"[Abrir en Colab]({notebook_url(module)})"
    )
    objectives_source = [
        "## Objetivos\n",
        "\n",
        *[f"- {item}\n" for item in module["objectives"]],
    ]
    if module.get("external_resources"):
        objectives_source.extend(
            [
                "\n",
                "## Laboratorio complementario\n",
                "\n",
                *[
                    f"- [{resource['label']}]({resource['url']})\n"
                    for resource in module["external_resources"]
                ],
            ]
        )
    setup_source = dedent(
        """
        import platform
        import sys

        import matplotlib
        import numpy as np
        import pandas as pd
        import sklearn

        SEED = 42
        np.random.seed(SEED)
        print({
            "python": platform.python_version(),
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "scikit_learn": sklearn.__version__,
            "matplotlib": matplotlib.__version__,
            "seed": SEED,
        })
        """
    ).strip().splitlines(True)
    decision_record_source = dedent(
        f"""
        decision_record = {{
            "pregunta": {module['business_question']!r},
            "hipotesis": "Completar antes del análisis",
            "evidencia": "Registrar la tabla o visualización que cambia la decisión",
            "recomendacion": "Expresar acción, población y horizonte",
            "limitacion": "Indicar qué podría invalidar la conclusión",
            "responsable": "Asignar dueño y fecha de revisión",
        }}
        pd.Series(decision_record, name="registro_de_decision")
        """
    ).strip().splitlines(True)
    cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                f"# Módulo {module['id']}: {module['title']}\n",
                "\n",
                f"{colab_badge}\n",
                "\n",
                f"**Pregunta de decisión:** {module['business_question']}\n",
                "\n",
                f"**Autor:** {COURSE['author']}\n",
            ],
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": objectives_source
            + [
                "\n",
                "**Criterio de éxito:** el resultado debe cambiar o sostener una acción concreta, superar una referencia y declarar límites.\n",
            ],
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 1. Entorno reproducible\n",
                "\n",
                "Registramos versiones y semilla antes de producir evidencia. Ejecutá siempre **Runtime → Run all** en Colab.\n",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": setup_source,
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. Experimento base\n",
                "\n",
                "El bloque siguiente construye una referencia mínima y verificable. No representa todavía la recomendación final.\n",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": dedent(NOTEBOOK_CODE[module["id"]]).strip().splitlines(True),
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3. Evidencia visual\n",
                "\n",
                "Una visualización útil permite comparar, muestra unidades y deja visible la incertidumbre o variación relevante.\n",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": dedent(NOTEBOOK_VISUALIZATION[module["id"]]).strip().splitlines(True),
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 4. Comparación para decidir\n",
                "\n",
                f"{module['case']}\n",
                "\n",
                "La tabla fuerza una comparación entre alternativas, costos o criterios. Adaptala a las unidades del caso.\n",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": dedent(NOTEBOOK_DECISION[module["id"]]).strip().splitlines(True),
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 5. Desafío de transferencia\n",
                "\n",
                f"**{module['decision_challenge']}**\n",
                "\n",
                *[
                    f"{index}. {item}\n"
                    for index, item in enumerate(module["lab_steps"], start=1)
                ],
                "\n",
                "Antes de continuar, escribí una hipótesis, una condición que la refutaría y el costo de una decisión equivocada.\n",
                "\n",
                "### Registro de decisión\n",
                "\n",
                "Completá la celda siguiente como evidencia de cierre del laboratorio.\n",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": decision_record_source,
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 6. Cierre verificable\n",
                "\n",
                f"**Entregable:** {module['deliverable']}\n",
                "\n",
                "- Hallazgo principal:\n",
                "- Evidencia que lo respalda:\n",
                "- Comparación contra baseline o escenario alternativo:\n",
                "- Limitación:\n",
                "- Acción, responsable y fecha de revisión:\n",
                "\n",
                f"Material elaborado por el profesor {COURSE['author']}.\n",
            ],
        },
    ]
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
            "colab": {"name": f"{module['slug']}.ipynb", "provenance": []},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def root_readme() -> str:
    module_rows = "\n        ".join(
        (
            f"| {module['id']} | {module['title']} | "
            f"[Guía]({module_url(module)}) · "
            f"[Simulación]({module_url(module, 'simulacion.html')}) · "
            f"[Cuestionario]({module_url(module, 'cuestionario.html')}) · "
            f"[Glosario]({module_url(module, 'glosario.html')}) · "
            f"[Colab]({notebook_url(module)}) |"
        )
        for module in MODULES
    )
    return dedent(
        f"""
        # {COURSE['title']}

        Curso abierto de ciencia de datos, machine learning e inteligencia artificial orientado a decisiones de negocio.

        [![Abrir curso](https://img.shields.io/badge/Abrir%20curso-GitHub%20Pages-0f766e?style=for-the-badge)]({PAGES_URL}/)
        [![Calidad](https://img.shields.io/github/actions/workflow/status/{COURSE['owner']}/{COURSE['repository']}/quality.yml?branch=main&label=Calidad&style=for-the-badge)]({REPO_URL}/actions/workflows/quality.yml)
        [![Licencia de contenidos](https://img.shields.io/badge/Contenido-CC%20BY--NC%204.0-1d4ed8?style=for-the-badge)](LICENSE.md)

        ## Propósito

        El recorrido conecta cinco preguntas:

        1. ¿Qué decisión debe mejorar?
        2. ¿Los datos representan el proceso con calidad suficiente?
        3. ¿El modelo generaliza y supera una referencia útil?
        4. ¿Qué acción crea valor bajo costos y restricciones?
        5. ¿Cómo se explica, controla y monitorea su impacto?

        ## Acceso directo

        Cada módulo contiene una guía principal, una simulación sin instalación, un cuestionario con corrección inmediata, un glosario con buscador y un notebook ejecutable en Google Colab.

        ## Experiencia de aprendizaje

        - **Decisión antes que algoritmo:** cada tema parte de una pregunta, un costo de error y una acción posible.
        - **Laboratorios comparables:** las simulaciones permiten guardar escenarios A/B, registrar una hipótesis y exportar evidencia.
        - **Evaluación con transferencia:** 105 preguntas combinan comprensión conceptual con situaciones profesionales.
        - **Notebooks verificables:** los 15 laboratorios registran entorno, visualizan evidencia, comparan alternativas y cierran con una recomendación auditable.
        - **Datos para experimentar:** cuatro datasets sintéticos cubren calidad, predicción, series temporales, optimización y experimentación causal.

        | Módulo | Contenido | Recursos |
        |---:|---|---|
        {module_rows}

        ## Organización del repositorio

        ```text
        .
        ├── docs/                 Sitio publicado en GitHub Pages
        │   ├── modulos/          Guías, simulaciones, cuestionarios y glosarios
        │   └── assets/           Diseño y lógica compartida
        ├── modules/              Índices académicos por módulo
        ├── notebooks/            Laboratorios canónicos para Colab o Jupyter
        ├── datasets/             Datos didácticos y diccionarios
        ├── projects/capstone/    Consigna, rúbrica y plantillas
        ├── assessments/          Criterios de evaluación
        ├── references/           Guías rápidas
        └── scripts/              Generación y validación
        ```

        ## Uso local

        El sitio no necesita compilación:

        ```bash
        python -m http.server 8000 --directory docs
        ```

        Luego abrí `http://localhost:8000`.

        Para los notebooks:

        ```bash
        python -m venv .venv
        source .venv/bin/activate
        pip install -r requirements.txt
        jupyter lab
        ```

        ## Calidad

        ```bash
        python scripts/build_course.py --check
        python scripts/validate_repo.py
        python scripts/execute_notebooks.py
        ```

        La validación comprueba estructura, enlaces internos, HTML básico, JavaScript, cobertura de recursos, consistencia de contenidos y ejecución real de los 15 notebooks.

        ## Autoría

        Material elaborado por el profesor {COURSE['author']}.

        Para uso académico, consultá los metadatos de [CITATION.cff](CITATION.cff).

        ## Licencias

        Los materiales educativos se distribuyen bajo Creative Commons Attribution-NonCommercial 4.0 International. El código fuente se distribuye bajo licencia MIT. Consultá [LICENSE.md](LICENSE.md).
        """
    ).strip()


def supporting_files() -> None:
    write(
        "requirements.txt",
        dedent(
            """
            jupyterlab>=4.4,<5
            matplotlib>=3.10,<4
            nbclient>=0.10,<1
            nbformat>=5.10,<6
            numpy>=2.1,<3
            pandas>=2.3,<4
            scikit-learn>=1.7,<2
            scipy>=1.15,<2
            seaborn>=0.13,<1
            statsmodels>=0.14,<1
            """
        ),
    )
    write(
        ".gitignore",
        dedent(
            """
            .DS_Store
            .idea/
            .ipynb_checkpoints/
            .pytest_cache/
            .venv/
            __pycache__/
            *.py[cod]
            build/
            dist/
            """
        ),
    )
    write("docs/.nojekyll", "")
    write(
        "LICENSE.md",
        dedent(
            f"""
            # Licencias

            ## Material educativo

            Salvo indicación contraria, los textos, guías, consignas, gráficos y materiales didácticos de este repositorio se distribuyen bajo la licencia Creative Commons Attribution-NonCommercial 4.0 International.

            Podés compartir y adaptar el material para fines no comerciales siempre que atribuyas a {COURSE['author']}, enlaces esta licencia e indiques los cambios realizados.

            Texto oficial: https://creativecommons.org/licenses/by-nc/4.0/legalcode

            ## Código

            Copyright (c) 2026 {COURSE['author']}

            Se concede permiso, de forma gratuita, a cualquier persona que obtenga una copia del software y de los archivos de documentación asociados, para usar, copiar, modificar, fusionar, publicar, distribuir, sublicenciar y vender copias del software, sujeto a incluir este aviso.

            EL SOFTWARE SE ENTREGA SIN GARANTÍAS DE NINGÚN TIPO, EXPRESAS O IMPLÍCITAS, INCLUIDAS LAS DE COMERCIABILIDAD, ADECUACIÓN A UN PROPÓSITO PARTICULAR Y NO INFRACCIÓN. EN NINGÚN CASO LOS AUTORES SERÁN RESPONSABLES POR RECLAMOS, DAÑOS U OTRAS RESPONSABILIDADES DERIVADAS DEL SOFTWARE O SU USO.
            """
        ),
    )
    write(
        "CONTRIBUTING.md",
        dedent(
            """
            # Contribuir

            ## Flujo recomendado

            1. Abrí un issue con el problema didáctico o técnico.
            2. Creá una rama breve y enfocada.
            3. Editá la fuente en `scripts/course_data.py` cuando cambie contenido.
            4. Ejecutá `python scripts/build_course.py`.
            5. Ejecutá `python scripts/validate_repo.py`.
            6. Abrí un pull request con evidencia visual y de validación.

            ## Criterios

            - Español claro, preciso y orientado a decisiones.
            - Sin enlaces rotos ni recursos que dependan exclusivamente de servicios externos.
            - Gráficos acompañados por una lectura textual.
            - Controles accesibles por teclado y con etiquetas.
            - Notebooks ejecutables de principio a fin.
            - Datos sin información personal ni credenciales.
            """
        ),
    )
    write(
        "SECURITY.md",
        dedent(
            """
            # Seguridad

            No publiques credenciales, datos personales ni información confidencial en issues, notebooks, datasets o commits.

            Para reportar una vulnerabilidad del material interactivo, abrí un aviso privado mediante las herramientas de seguridad del repositorio. Incluí la página afectada, impacto, pasos de reproducción y una mitigación sugerida.
            """
        ),
    )
    write(
        "CODE_OF_CONDUCT.md",
        dedent(
            """
            # Código de conducta

            Este espacio de aprendizaje requiere respeto, precisión y colaboración.

            - Criticá ideas y evidencia, no personas.
            - Reconocé fuentes y contribuciones.
            - Evitá compartir datos sensibles.
            - Reportá errores de manera reproducible y constructiva.
            - Considerá el impacto de los sistemas analíticos sobre grupos y personas.

            Conductas de hostigamiento, discriminación o exposición de información privada no serán aceptadas.
            """
        ),
    )
    write(
        "assessments/README.md",
        dedent(
            """
            # Evaluación

            La evaluación combina comprensión conceptual, práctica reproducible y capacidad de decisión.

            | Componente | Evidencia |
            |---|---|
            | Cuestionarios | Comprensión y corrección explicada por módulo |
            | Laboratorios | Notebook ejecutable e interpretación |
            | Análisis breves | Supuestos, hallazgos y límites |
            | Proyecto integrador | Repositorio, informe, ficha y defensa |

            Los cuestionarios son formativos. La rúbrica del proyecto está en `projects/capstone/rubric.md`.
            """
        ),
    )
    write(
        "references/model-selection-checklist.md",
        dedent(
            """
            # Lista de control para seleccionar un modelo

            ## Problema

            - La unidad de análisis y el horizonte están definidos.
            - La predicción cambia una acción concreta.
            - Existe una métrica conectada con costo o valor.

            ## Evidencia

            - La partición imita el uso futuro.
            - Preparación y selección ocurren dentro del entrenamiento.
            - Existe un baseline.
            - Se reportan promedio, dispersión y segmentos relevantes.

            ## Operación

            - Latencia, capacidad y mantenimiento son aceptables.
            - Se documentan usos previstos, límites y responsables.
            - Hay indicadores de calidad, drift, desempeño y daño.
            """
        ),
    )
    write(
        "projects/capstone/README.md",
        dedent(
            """
            # Proyecto integrador de decisión

            ## Propósito

            Construir una recomendación analítica que conecte una decisión real con datos, evaluación fuera de muestra, valor esperado, riesgos y un plan de monitoreo.

            ## Entrega parcial

            - Canvas de decisión.
            - Contrato y diccionario de datos.
            - Controles de calidad y EDA.
            - Baseline.
            - Protocolo de validación.
            - Registro de riesgos iniciales.

            ## Entrega final

            - Pipeline reproducible.
            - Comparación de alternativas.
            - Evaluación técnica y económica.
            - Análisis de sensibilidad.
            - Ficha de modelo o sistema.
            - Informe ejecutivo y presentación.

            ## Exposición

            La defensa comienza por contexto, decisión y recomendación. La técnica se presenta como evidencia, seguida por impacto, incertidumbre, límites y próximos pasos.
            """
        ),
    )
    write(
        "projects/capstone/rubric.md",
        dedent(
            """
            # Rúbrica del proyecto integrador

            | Dimensión | Puntos | Evidencia esperada |
            |---|---:|---|
            | Problema y decisión | 15 | Stakeholder, unidad, horizonte, acción, éxito |
            | Datos y calidad | 15 | Origen, diccionario, controles, sesgos |
            | EDA y baseline | 15 | Hallazgos relevantes y referencia |
            | Modelado | 20 | Pipeline, alternativas y justificación |
            | Evaluación y valor | 15 | Validación, costos, sensibilidad |
            | Responsabilidad | 10 | Límites, equidad, explicación, monitoreo |
            | Comunicación | 10 | Narrativa, visualización, repositorio, defensa |
            | **Total** | **100** | |

            ## Condiciones de integridad

            Un resultado no reproducible, una evaluación contaminada o el uso de datos sin autorización requieren corrección antes de asignar puntaje al producto final.
            """
        ),
    )
    write(
        "projects/capstone/templates/decision-canvas.md",
        dedent(
            """
            # Canvas de decisión

            ## Contexto

            - Organización o proceso:
            - Stakeholder que decide:
            - Situación actual:

            ## Decisión

            - Unidad de análisis:
            - Momento de decisión:
            - Horizonte:
            - Acción disponible:
            - Capacidad o restricción:

            ## Evidencia

            - Variable objetivo:
            - Datos disponibles en ese momento:
            - Baseline:
            - Métrica técnica:
            - Métrica de valor:

            ## Riesgos

            - Error más costoso:
            - Grupo potencialmente afectado:
            - Supuesto crítico:
            - Criterio para no desplegar:
            """
        ),
    )
    write(
        "projects/capstone/templates/final-report.md",
        dedent(
            """
            # Informe final

            ## Resumen ejecutivo

            Decisión, recomendación, valor esperado y condición principal.

            ## Problema y alcance

            Unidad, población, horizonte, acción, métrica y exclusiones.

            ## Datos

            Origen, cobertura, calidad, sesgos y diccionario.

            ## Evidencia exploratoria

            Hallazgos que modificaron el enfoque.

            ## Método

            Baseline, pipeline, modelos y protocolo de validación.

            ## Resultados

            Métricas, incertidumbre, segmentos y análisis de sensibilidad.

            ## Decisión recomendada

            Política, umbral o asignación y valor esperado.

            ## Responsabilidad y límites

            Interpretación, equidad, privacidad, riesgos y supervisión.

            ## Monitoreo

            Indicadores, umbrales, frecuencia, responsables y respuesta.
            """
        ),
    )
    write(
        "projects/capstone/templates/review-checklist.md",
        dedent(
            """
            # Revisión antes de entregar

            - [ ] La recomendación responde a una decisión concreta.
            - [ ] Todas las figuras tienen título, unidades y lectura.
            - [ ] El notebook ejecuta de principio a fin.
            - [ ] No hay rutas locales, credenciales ni datos personales.
            - [ ] El pipeline evita leakage.
            - [ ] Test no se usó para seleccionar.
            - [ ] Se compara contra un baseline.
            - [ ] Se reportan incertidumbre y segmentos relevantes.
            - [ ] Costos, capacidad y valor están cuantificados.
            - [ ] Límites y criterio de no uso son explícitos.
            - [ ] El plan de monitoreo tiene responsables.
            - [ ] Todas las fuentes están citadas.
            """
        ),
    )


def datasets() -> None:
    rng = random.Random(42)
    output = io.StringIO()
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(
        [
            "cliente_id",
            "segmento",
            "zona_operativa",
            "canal_preferido",
            "antiguedad_meses",
            "compras_90d",
            "ticket_promedio",
            "reclamos_180d",
            "costo_contacto",
            "valor_cliente_12m",
            "abandono_30d",
        ]
    )
    for client_id in range(1, 1201):
        segment = rng.choice(["Inicial", "Frecuente", "Premium"])
        zone = rng.choice(["Centro", "Norte", "Sur", "Remota"])
        channel = rng.choices(
            ["Digital", "Sucursal", "Telefónico"], weights=[0.55, 0.27, 0.18]
        )[0]
        tenure = rng.randint(1, 84)
        purchases = max(0, int(rng.gauss({"Inicial": 2, "Frecuente": 6, "Premium": 9}[segment], 2)))
        ticket = max(8, rng.gauss({"Inicial": 45, "Frecuente": 72, "Premium": 135}[segment], 24))
        complaints = max(0, int(rng.gauss(0.7 if segment != "Premium" else 0.4, 0.8)))
        contact_cost = {"Digital": 1.8, "Sucursal": 8.5, "Telefónico": 4.2}[channel]
        customer_value = max(20, purchases * ticket * rng.uniform(2.2, 4.8))
        logit = (
            -1.7
            - 0.035 * tenure
            - 0.18 * purchases
            + 0.75 * complaints
            + (0.25 if zone == "Remota" else 0)
            + (0.18 if channel == "Telefónico" else 0)
        )
        probability = 1 / (1 + math.exp(-logit))
        churn = int(rng.random() < probability)
        ticket_value = "" if rng.random() < 0.035 else f"{ticket:.2f}"
        writer.writerow(
            [
                client_id,
                segment,
                zone,
                channel,
                tenure,
                purchases,
                ticket_value,
                complaints,
                f"{contact_cost:.2f}",
                f"{customer_value:.2f}",
                churn,
            ]
        )
    write("datasets/clientes.csv", output.getvalue())

    output = io.StringIO()
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(["fecha", "ventas", "promocion", "feriado", "inversion_marketing", "indice_precio"])
    for month in range(96):
        year = 2018 + month // 12
        month_number = month % 12 + 1
        seasonal = 22 * math.sin(2 * math.pi * month / 12)
        promo = int(month_number in (5, 11))
        holiday = int(month_number == 12)
        marketing = 18 + 5 * promo + rng.uniform(-2.5, 2.5)
        price_index = 100 + 0.45 * month + rng.gauss(0, 1.2)
        sales = 120 + 1.4 * month + seasonal + 18 * promo + 28 * holiday + 0.8 * marketing + rng.gauss(0, 7)
        writer.writerow(
            [
                f"{year:04d}-{month_number:02d}-01",
                f"{sales:.1f}",
                promo,
                holiday,
                f"{marketing:.2f}",
                f"{price_index:.2f}",
            ]
        )
    write("datasets/ventas-mensuales.csv", output.getvalue())

    output = io.StringIO()
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(["orden_id", "producto", "turno", "horas_maquina", "materia_prima", "margen", "demanda", "retraso_horas"])
    for order_id in range(1, 601):
        product = rng.choice(["A", "B", "C"])
        shift = rng.choice(["Mañana", "Tarde", "Noche"])
        hours = {"A": 2.0, "B": 1.2, "C": 2.8}[product] + rng.uniform(-0.15, 0.15)
        material = {"A": 1.0, "B": 2.0, "C": 1.6}[product] + rng.uniform(-0.1, 0.1)
        margin = {"A": 40, "B": 30, "C": 52}[product] + rng.uniform(-3, 3)
        demand = max(1, int(rng.gauss({"A": 34, "B": 48, "C": 25}[product], 8)))
        delay = max(0, rng.gauss(1.0 if shift != "Noche" else 2.1, 1.5))
        writer.writerow([order_id, product, shift, f"{hours:.2f}", f"{material:.2f}", f"{margin:.2f}", demand, f"{delay:.2f}"])
    write("datasets/operaciones.csv", output.getvalue())

    output = io.StringIO()
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(["observacion_id", "variante", "segmento", "conversion", "margen", "tiempo_respuesta_ms"])
    for observation_id in range(1, 2401):
        variant = "B" if rng.random() < 0.5 else "A"
        segment = rng.choice(["Nuevo", "Recurrente", "Alto valor"])
        baseline = {"Nuevo": 0.10, "Recurrente": 0.17, "Alto valor": 0.23}[segment]
        treatment_effect = {"Nuevo": 0.035, "Recurrente": 0.012, "Alto valor": -0.008}[segment]
        probability = baseline + (treatment_effect if variant == "B" else 0)
        conversion = int(rng.random() < probability)
        margin = conversion * max(5, rng.gauss({"Nuevo": 28, "Recurrente": 46, "Alto valor": 82}[segment], 12))
        latency = max(120, rng.gauss(430 + (65 if variant == "B" else 0), 75))
        writer.writerow([observation_id, variant, segment, conversion, f"{margin:.2f}", f"{latency:.0f}"])
    write("datasets/experimentos.csv", output.getvalue())

    write(
        "datasets/README.md",
        dedent(
            """
            # Datos didácticos

            Los archivos son sintéticos, reproducibles y no contienen información personal.

            | Archivo | Unidad de análisis | Uso principal |
            |---|---|---|
            | `clientes.csv` | Cliente al cierre de período | EDA, faltantes, regresión, clasificación, árboles, clustering |
            | `ventas-mensuales.csv` | Mes | Series de tiempo y backtesting |
            | `operaciones.csv` | Orden | EDA, regresión y optimización |
            | `experimentos.csv` | Exposición a una variante | Experimentación, heterogeneidad y decisión causal |

            ## Reglas

            - No interpretar relaciones sintéticas como hechos de una industria real.
            - Documentar cualquier modificación.
            - Mantener la semilla del generador cuando se necesite reproducibilidad.
            """
        ),
    )
    write(
        "datasets/data-dictionary.md",
        dedent(
            """
            # Diccionario de datos

            ## clientes.csv

            | Variable | Tipo | Descripción |
            |---|---|---|
            | cliente_id | entero | Identificador sintético único |
            | segmento | categoría | Perfil comercial inicial |
            | zona_operativa | categoría | Zona sintética para análisis de segmentos y cobertura |
            | canal_preferido | categoría | Canal principal de interacción |
            | antiguedad_meses | entero | Meses desde el alta |
            | compras_90d | entero | Compras en los últimos noventa días |
            | ticket_promedio | decimal anulable | Importe medio por compra; incluye faltantes didácticos |
            | reclamos_180d | entero | Reclamos en los últimos ciento ochenta días |
            | costo_contacto | decimal | Costo sintético de intervenir por el canal elegido |
            | valor_cliente_12m | decimal | Valor sintético observado en doce meses |
            | abandono_30d | binaria | Evento sintético en los treinta días siguientes |

            ## ventas-mensuales.csv

            | Variable | Tipo | Descripción |
            |---|---|---|
            | fecha | fecha | Primer día del mes |
            | ventas | decimal | Nivel sintético mensual |
            | promocion | binaria | Mes con promoción planificada |
            | feriado | binaria | Indicador de período festivo |
            | inversion_marketing | decimal | Inversión sintética mensual |
            | indice_precio | decimal | Índice sintético de precio |

            ## operaciones.csv

            | Variable | Tipo | Descripción |
            |---|---|---|
            | orden_id | entero | Identificador sintético |
            | producto | categoría | Familia A, B o C |
            | turno | categoría | Franja operativa sintética |
            | horas_maquina | decimal | Consumo estimado de capacidad |
            | materia_prima | decimal | Consumo estimado de insumo |
            | margen | decimal | Contribución sintética |
            | demanda | entero | Unidades solicitadas en la orden |
            | retraso_horas | decimal | Demora operativa sintética |

            ## experimentos.csv

            | Variable | Tipo | Descripción |
            |---|---|---|
            | observacion_id | entero | Identificador sintético de exposición |
            | variante | categoría | Asignación aleatoria A o B |
            | segmento | categoría | Segmento previo al tratamiento |
            | conversion | binaria | Resultado principal observado |
            | margen | decimal | Contribución observada después de la exposición |
            | tiempo_respuesta_ms | decimal | Latencia del flujo asignado |
            """
        ),
    )


def generate() -> None:
    write("README.md", root_readme())
    write("docs/index.html", home_page())
    write("docs/programa.html", program_page())
    write("docs/proyecto-integrador.html", capstone_page())
    write("docs/profundizaciones.html", deepening_page())
    write("docs/accesibilidad.html", accessibility_page())
    js_data = {
        "course": COURSE,
        "units": UNITS,
        "modules": [
            {
                "id": module["id"],
                "slug": module["slug"],
                "title": module["title"],
                "shortTitle": module["short_title"],
                "summary": module["summary"],
            }
            for module in MODULES
        ],
    }
    write(
        "docs/assets/js/course-data.js",
        "window.COURSE_DATA = "
        + json.dumps(js_data, ensure_ascii=False, separators=(",", ":"))
        + ";",
    )
    for module in MODULES:
        base = f"docs/modulos/{module['slug']}"
        write(f"{base}/index.html", module_index(module))
        write(f"{base}/simulacion.html", simulation_page(module))
        write(f"{base}/cuestionario.html", quiz_page(module))
        write(f"{base}/glosario.html", glossary_page(module))
        write(f"modules/{module['slug']}/README.md", module_readme(module))
        write(
            f"notebooks/{module['slug']}.ipynb",
            json.dumps(notebook(module), ensure_ascii=False, indent=1),
        )
    supporting_files()
    datasets()
    manifest = {
        "course": COURSE["title"],
        "modules": len(MODULES),
        "simulations": len(MODULES),
        "questions": sum(len(module["quiz"]) for module in MODULES),
        "glossary_terms": sum(len(module["glossary"]) for module in MODULES),
        "notebooks": len(MODULES),
        "module_slugs": [module["slug"] for module in MODULES],
    }
    write(
        "course-manifest.json",
        json.dumps(manifest, ensure_ascii=False, indent=2),
    )


def check_generated() -> list[str]:
    global ROOT, DOCS
    current_root = ROOT
    mismatches: list[str] = []
    with tempfile.TemporaryDirectory(prefix="course-check-") as directory:
        ROOT = Path(directory)
        DOCS = ROOT / "docs"
        generate()
        temporary_root = ROOT
        for generated in temporary_root.rglob("*"):
            if not generated.is_file():
                continue
            relative = generated.relative_to(temporary_root)
            current = current_root / relative
            if not current.is_file():
                mismatches.append(f"falta {relative}")
            elif current.read_bytes() != generated.read_bytes():
                mismatches.append(f"desactualizado {relative}")
    ROOT = current_root
    DOCS = ROOT / "docs"
    return mismatches


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Comprueba que los archivos generados coincidan con las fuentes.",
    )
    arguments = parser.parse_args()
    if arguments.check:
        differences = check_generated()
        if differences:
            print("Los archivos generados no coinciden:")
            for difference in differences:
                print(f"  - {difference}")
            raise SystemExit(1)
        print("Archivos generados sincronizados")
    else:
        generate()
        print(
            f"Curso generado: {len(MODULES)} módulos, "
            f"{sum(len(module['quiz']) for module in MODULES)} preguntas y "
            f"{sum(len(module['glossary']) for module in MODULES)} términos."
        )
