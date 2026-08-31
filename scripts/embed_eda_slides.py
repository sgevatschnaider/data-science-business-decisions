"""Integra presentaciones de Google Slides en los módulos ampliados.

El sitio principal se genera con ``scripts/build_course.py``. Este paso aplica una
transformación determinística al HTML generado para conservar los visores
incrustados, los accesos a pantalla completa y el diseño responsive.
"""

from __future__ import annotations

from pathlib import Path


PRESENTATION_MODULES = [
    {
        "target": Path("docs/modulos/01-eda-negocio/index.html"),
        "label": "módulo 01",
        "aria_label": "Presentaciones integradas del módulo EDA",
        "intro_source": (
            "Tres bloques breves para acompañar la secuencia conceptual de la clase."
        ),
        "intro_target": (
            "Tres bloques breves para acompañar la secuencia conceptual de la clase. "
            "También podés recorrerlos directamente desde esta página."
        ),
        "slides": [
            {
                "title": "Diapositivas 01 · Fundamentos y calidad",
                "subtitle": "Paradigma EDA, proceso exploratorio y calidad de datos",
                "view": "https://docs.google.com/presentation/d/1qQKwxrOYNadm72ohKrm9YZG-MyuyTj5khwwJSe_fJU8/view?usp=sharing",
                "present": "https://docs.google.com/presentation/d/1qQKwxrOYNadm72ohKrm9YZG-MyuyTj5khwwJSe_fJU8/present?slide=id.p1",
                "embed": "https://docs.google.com/presentation/d/1qQKwxrOYNadm72ohKrm9YZG-MyuyTj5khwwJSe_fJU8/embed?start=false&amp;loop=false&amp;delayms=3000",
                "id": "slides-01",
            },
            {
                "title": "Diapositivas 02 · Análisis univariado",
                "subtitle": "Distribuciones, estadísticos descriptivos y visualización",
                "view": "https://docs.google.com/presentation/d/1q4Zd4GJ2XnlhKZSNX5yoWhbrDG_26i0x6FQJZDoL_Zo/view?usp=sharing",
                "present": "https://docs.google.com/presentation/d/1q4Zd4GJ2XnlhKZSNX5yoWhbrDG_26i0x6FQJZDoL_Zo/present?slide=id.p1",
                "embed": "https://docs.google.com/presentation/d/1q4Zd4GJ2XnlhKZSNX5yoWhbrDG_26i0x6FQJZDoL_Zo/embed?start=false&amp;loop=false&amp;delayms=3000",
                "id": "slides-02",
            },
            {
                "title": "Diapositivas 03 · Relaciones y outliers",
                "subtitle": "Relaciones, valores atípicos y lectura multivariada",
                "view": "https://docs.google.com/presentation/d/1ch7ZOInyminmAwtZwcqnuqnjP9aa6vE6kdews_2YKfk/view?usp=sharing",
                "present": "https://docs.google.com/presentation/d/1ch7ZOInyminmAwtZwcqnuqnjP9aa6vE6kdews_2YKfk/present?slide=id.p1",
                "embed": "https://docs.google.com/presentation/d/1ch7ZOInyminmAwtZwcqnuqnjP9aa6vE6kdews_2YKfk/embed?start=false&amp;loop=false&amp;delayms=3000",
                "id": "slides-03",
            },
        ],
    },
    {
        "target": Path("docs/modulos/02-calidad-datos/index.html"),
        "label": "módulo 02",
        "aria_label": "Presentaciones integradas del módulo de calidad de datos",
        "intro_source": (
            "Tres bloques para construir el diagnóstico antes de modificar los datos."
        ),
        "intro_target": (
            "Tres bloques para construir el diagnóstico antes de modificar los datos. "
            "También podés recorrerlos directamente desde esta página."
        ),
        "slides": [
            {
                "title": "Diapositivas 01 · Calidad de datos y decisiones",
                "subtitle": "Dimensiones, reglas, gobernanza y costo del error",
                "view": "https://docs.google.com/presentation/d/1CAvqHS1RNvTdth7VzIxJ1fzm82NA8smheyvRh_PerkM/view?usp=sharing",
                "present": "https://docs.google.com/presentation/d/1CAvqHS1RNvTdth7VzIxJ1fzm82NA8smheyvRh_PerkM/present?slide=id.p1",
                "embed": "https://docs.google.com/presentation/d/1CAvqHS1RNvTdth7VzIxJ1fzm82NA8smheyvRh_PerkM/embed?start=false&amp;loop=false&amp;delayms=3000",
                "id": "m02-slides-01",
            },
            {
                "title": "Diapositivas 02 · Missing Data: MCAR, MAR y MNAR",
                "subtitle": "Mecanismos de ausencia, patrones, hipótesis y sesgo",
                "view": "https://docs.google.com/presentation/d/1ejHnIv-QppNEq1mcEKFA_F_euYJFFJFkrbggV6LubM8/view?usp=sharing",
                "present": "https://docs.google.com/presentation/d/1ejHnIv-QppNEq1mcEKFA_F_euYJFFJFkrbggV6LubM8/present?slide=id.p1",
                "embed": "https://docs.google.com/presentation/d/1ejHnIv-QppNEq1mcEKFA_F_euYJFFJFkrbggV6LubM8/embed?start=false&amp;loop=false&amp;delayms=3000",
                "id": "m02-slides-02",
            },
            {
                "title": "Diapositivas 03 · Imputación, pipelines y modelos",
                "subtitle": "Tratamiento reproducible, leakage y evaluación de impacto",
                "view": "https://docs.google.com/presentation/d/1hfBu_-gMoQaNWPyiY41OmWw9Zi3U1IMFmX6eEvpB0KY/view?usp=sharing",
                "present": "https://docs.google.com/presentation/d/1hfBu_-gMoQaNWPyiY41OmWw9Zi3U1IMFmX6eEvpB0KY/present?slide=id.p1",
                "embed": "https://docs.google.com/presentation/d/1hfBu_-gMoQaNWPyiY41OmWw9Zi3U1IMFmX6eEvpB0KY/embed?start=false&amp;loop=false&amp;delayms=3000",
                "id": "m02-slides-03",
            },
        ],
    },
    {
        "target": Path("docs/modulos/03-outliers/index.html"),
        "label": "módulo 03",
        "aria_label": "Presentaciones integradas del módulo de outliers",
        "intro_source": (
            "Dos recorridos complementarios: primero diagnóstico, robustez e "
            "influencia; después métodos modernos de detección con Machine "
            "Learning. También podés recorrerlos directamente desde esta página."
        ),
        "intro_target": (
            "Dos recorridos complementarios: primero diagnóstico, robustez e "
            "influencia; después métodos modernos de detección con Machine "
            "Learning. También podés recorrerlos directamente desde esta página."
        ),
        "slides": [
            {
                "title": "Diapositivas 01 · Diagnóstico, robustez y tratamiento",
                "subtitle": (
                    "Reglas clásicas, influencia, decisiones de tratamiento y leakage"
                ),
                "view": "https://docs.google.com/presentation/d/15nnL4qm_aKb3G2-G0xbna0MiUtl05-9Ic3NIHF0FwKk/view?usp=sharing",
                "present": "https://docs.google.com/presentation/d/15nnL4qm_aKb3G2-G0xbna0MiUtl05-9Ic3NIHF0FwKk/present?slide=id.p1",
                "embed": "https://docs.google.com/presentation/d/15nnL4qm_aKb3G2-G0xbna0MiUtl05-9Ic3NIHF0FwKk/embed?start=false&amp;loop=false&amp;delayms=3000",
                "id": "m03-slides-01",
            },
            {
                "title": "Diapositivas 02 · Métodos de detección con ML",
                "subtitle": (
                    "Aislamiento, densidad, fronteras, clustering y reconstrucción"
                ),
                "view": "https://docs.google.com/presentation/d/1I-jQOc8mkt1WVhGZffWr6p9EWAYg13SBjryxTvYUAtc/view?usp=sharing",
                "present": "https://docs.google.com/presentation/d/1I-jQOc8mkt1WVhGZffWr6p9EWAYg13SBjryxTvYUAtc/present?slide=id.p1",
                "embed": "https://docs.google.com/presentation/d/1I-jQOc8mkt1WVhGZffWr6p9EWAYg13SBjryxTvYUAtc/embed?start=false&amp;loop=false&amp;delayms=3000",
                "id": "m03-slides-02",
            },
        ],
    },
    {
        "target": Path("docs/modulos/04-transformacion-pipelines/index.html"),
        "label": "módulo 04",
        "aria_label": "Presentación integrada del módulo de transformación de variables",
        "intro_source": (
            "Una presentación de 14 diapositivas para distinguir escala, forma, "
            "objeto transformado, geometría, robustez, PCA y prevención de leakage. "
            "También podés recorrerla directamente desde esta página."
        ),
        "intro_target": (
            "Una presentación de 14 diapositivas para distinguir escala, forma, "
            "objeto transformado, geometría, robustez, PCA y prevención de leakage. "
            "También podés recorrerla directamente desde esta página."
        ),
        "slides": [
            {
                "title": "Diapositivas · Fundamentos y criterio de decisión",
                "subtitle": (
                    "Unidades, geometría, robustez, PCA, diagnóstico y prevención de leakage"
                ),
                "view": "https://docs.google.com/presentation/d/1a5I_FUqCfgHIOlatzfu7B5h2MLku583V-Sp8ls6y6tk/view?usp=sharing",
                "present": "https://docs.google.com/presentation/d/1a5I_FUqCfgHIOlatzfu7B5h2MLku583V-Sp8ls6y6tk/present?slide=id.p1",
                "embed": "https://docs.google.com/presentation/d/1a5I_FUqCfgHIOlatzfu7B5h2MLku583V-Sp8ls6y6tk/embed?start=false&amp;loop=false&amp;delayms=3000",
                "id": "m04-slides-01",
            },
        ],
    },
]

STYLE = """  <style>
    .slides-note {
      margin: 1.25rem 0 0;
      padding: .9rem 1rem;
      border: 1px solid rgba(14, 116, 144, .18);
      border-radius: 12px;
      background: rgba(14, 116, 144, .06);
    }

    .slides-showcase {
      display: grid;
      gap: 1rem;
      margin-top: 1rem;
    }

    .slides-embed-card {
      overflow: hidden;
      border: 1px solid rgba(100, 116, 139, .24);
      border-radius: 16px;
      background: rgba(255, 255, 255, .02);
    }

    .slides-embed-card summary {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      padding: 1rem 1.1rem;
      cursor: pointer;
      list-style: none;
      font-weight: 700;
    }

    .slides-embed-card summary::-webkit-details-marker {
      display: none;
    }

    .slides-embed-card summary::after {
      content: "+";
      flex: 0 0 auto;
      width: 1.75rem;
      height: 1.75rem;
      display: grid;
      place-items: center;
      border-radius: 999px;
      background: rgba(14, 116, 144, .10);
      font-size: 1.2rem;
      line-height: 1;
    }

    .slides-embed-card[open] summary::after {
      content: "−";
    }

    .slides-embed-card summary:focus-visible {
      outline: 3px solid rgba(14, 116, 144, .35);
      outline-offset: -3px;
    }

    .slides-summary-copy {
      display: grid;
      gap: .2rem;
    }

    .slides-summary-copy small {
      font-weight: 500;
      opacity: .72;
    }

    .slides-embed-body {
      padding: 0 1rem 1rem;
    }

    .slides-frame {
      position: relative;
      width: 100%;
      aspect-ratio: 16 / 9;
      overflow: hidden;
      border-radius: 12px;
      background: #0b172a;
      box-shadow: 0 12px 30px rgba(15, 23, 42, .16);
    }

    .slides-frame iframe {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      border: 0;
      display: block;
    }

    .slides-actions {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: .8rem 1rem;
      margin-top: .9rem;
    }

    @media (max-width: 720px) {
      .slides-embed-card summary {
        align-items: flex-start;
      }

      .slides-actions {
        align-items: stretch;
      }

      .slides-actions .button,
      .slides-actions .text-link {
        width: 100%;
        justify-content: center;
      }
    }
  </style>
"""


def details_block(slide: dict[str, str], *, opened: bool = False) -> str:
    open_attr = " open" if opened else ""
    return f"""                    <details class=\"slides-embed-card\" id=\"{slide['id']}\" name=\"slides-viewer\"{open_attr}>
                      <summary>
                        <span class=\"slides-summary-copy\">
                          <span>{slide['title']}</span>
                          <small>{slide['subtitle']}</small>
                        </span>
                      </summary>
                      <div class=\"slides-embed-body\">
                        <div class=\"slides-frame\">
                          <iframe
                            src=\"{slide['embed']}\"
                            title=\"{slide['title']}\"
                            loading=\"lazy\"
                            allowfullscreen>
                          </iframe>
                        </div>
                        <div class=\"slides-actions\">
                          <a class=\"button secondary\" href=\"{slide['present']}\" target=\"_blank\" rel=\"noopener noreferrer\">Abrir a pantalla completa</a>
                          <a class=\"text-link\" href=\"{slide['view']}\" target=\"_blank\" rel=\"noopener noreferrer\">Abrir en Google Slides <span aria-hidden=\"true\">→</span></a>
                        </div>
                      </div>
                    </details>"""


def showcase(module: dict) -> str:
    cards = "\n\n".join(
        details_block(slide, opened=index == 0)
        for index, slide in enumerate(module["slides"])
    )
    return f"""                  <p class="slides-note"><strong>Visor integrado.</strong> Abrí cada bloque para avanzar las diapositivas sin salir de Datos y Decisiones. Si preferís una vista más grande, usá “Abrir a pantalla completa”. Si Google solicita acceso, iniciá sesión desde “Abrir en Google Slides”.</p>

                  <div class="slides-showcase" aria-label="{module['aria_label']}">
{cards}
                  </div>
"""


def replace_first_after(text: str, anchor: str, old: str, new: str) -> str:
    start = text.find(anchor)
    if start == -1:
        raise RuntimeError(f"No se encontró el ancla esperada: {anchor}")
    position = text.find(old, start)
    if position == -1:
        raise RuntimeError(f"No se encontró {old!r} después de {anchor!r}")
    return text[:position] + new + text[position + len(old):]


def integrate_module(module: dict) -> None:
    target = module["target"]
    text = target.read_text(encoding="utf-8")

    # Idempotencia por módulo: un visor existente no impide procesar el siguiente.
    if 'class="slides-showcase"' in text:
        print(f"Google Slides ya está integrado en el {module['label']}.")
        return

    head_anchor = '  <link rel="stylesheet" href="../../assets/css/course.css">\n</head>'
    if head_anchor not in text:
        raise RuntimeError("No se encontró el cierre esperado del <head>.")
    text = text.replace(
        head_anchor,
        '  <link rel="stylesheet" href="../../assets/css/course.css">\n' + STYLE + '</head>',
        1,
    )

    nav_anchor = '            <nav aria-label="Secciones del módulo">\n              <a href="#indice">Índice interactivo</a>'
    text = text.replace(
        nav_anchor,
        '            <nav aria-label="Secciones del módulo">\n              <a href="#presentaciones">Presentaciones</a>\n              <a href="#indice">Índice interactivo</a>',
        1,
    )

    text = text.replace(
        '<section class="resource-group" aria-labelledby="resource-1">',
        '<section class="resource-group" id="presentaciones" aria-labelledby="resource-1">',
        1,
    )
    text = text.replace(
        f'<p>{module["intro_source"]}</p>',
        f'<p>{module["intro_target"]}</p>',
        1,
    )

    # Las tarjetas y los botones del laboratorio abren en modo presentación.
    for slide in module["slides"]:
        text = text.replace(f'href="{slide["view"]}"', f'href="{slide["present"]}"')
        text = replace_first_after(
            text,
            f'href="{slide["present"]}"',
            'Abrir ahora',
            'Abrir pantalla completa',
        )

    marker = '</a></div>\n                </section><section class="resource-group" aria-labelledby="resource-2">'
    if marker not in text:
        raise RuntimeError("No se encontró el final del bloque de presentaciones.")
    text = text.replace(
        marker,
        '</a></div>\n\n'
        + showcase(module)
        + '                </section><section class="resource-group" aria-labelledby="resource-2">',
        1,
    )

    target.write_text(text.rstrip() + "\n", encoding="utf-8")
    print(f"Presentaciones integradas en {target}.")


def main() -> None:
    for module in PRESENTATION_MODULES:
        integrate_module(module)


if __name__ == "__main__":
    main()
