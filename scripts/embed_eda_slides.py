"""Integra las presentaciones de Google Slides dentro del módulo EDA.

El sitio principal se genera con ``scripts/build_course.py``. Este paso aplica una
transformación determinística al HTML generado del módulo 01 para conservar los
visores incrustados, los accesos a pantalla completa y el diseño responsive.
"""

from __future__ import annotations

from pathlib import Path


TARGET = Path("docs/modulos/01-eda-negocio/index.html")

SLIDES = [
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
    return f"""                    <details class=\"slides-embed-card\" id=\"{slide['id']}\"{open_attr}>
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


SHOWCASE = """                  <p class="slides-note"><strong>Visor integrado.</strong> Abrí cada bloque para avanzar las diapositivas sin salir de Datos y Decisiones. Si preferís una vista más grande, usá “Abrir a pantalla completa”.</p>

                  <div class="slides-showcase" aria-label="Presentaciones integradas del módulo EDA">
{cards}
                  </div>
""".format(cards="\n\n".join(details_block(slide, opened=index == 0) for index, slide in enumerate(SLIDES)))


def replace_first_after(text: str, anchor: str, old: str, new: str) -> str:
    start = text.find(anchor)
    if start == -1:
        raise RuntimeError(f"No se encontró el ancla esperada: {anchor}")
    position = text.find(old, start)
    if position == -1:
        raise RuntimeError(f"No se encontró {old!r} después de {anchor!r}")
    return text[:position] + new + text[position + len(old):]


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")

    # Idempotencia: si el visor ya está integrado, no lo dupliques.
    if 'class="slides-showcase"' in text:
        print("Google Slides ya está integrado en el módulo EDA.")
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
        '<p>Tres bloques breves para acompañar la secuencia conceptual de la clase.</p>',
        '<p>Tres bloques breves para acompañar la secuencia conceptual de la clase. También podés recorrerlos directamente desde esta página.</p>',
        1,
    )

    # Las tarjetas y los botones del laboratorio abren en modo presentación.
    for slide in SLIDES:
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
        '</a></div>\n\n' + SHOWCASE + '                </section><section class="resource-group" aria-labelledby="resource-2">',
        1,
    )

    TARGET.write_text(text.rstrip() + "\n", encoding="utf-8")
    print(f"Presentaciones integradas en {TARGET}.")


if __name__ == "__main__":
    main()
