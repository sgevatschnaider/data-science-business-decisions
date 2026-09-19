"""Extiende la validación general para módulos con páginas docentes personalizadas.

Los módulos 07 y 08 conservan datos mínimos en course_data.py para compatibilidad con
el generador histórico, pero publican experiencias avanzadas después del build general.
"""
from __future__ import annotations
from pathlib import Path
import validate_repo as base

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_CONTENT_COUNTS = base.validate_content_counts
M07 = ROOT / "modules/07-series-tiempo/site"
M08 = ROOT / "modules/08-regresion-logistica/site"

def discard(fragment: str) -> None:
    base.ERRORS[:] = [e for e in base.ERRORS if fragment not in e]

def require(path: Path, label: str) -> str:
    if not path.is_file():
        base.error(f"{label}: falta {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")

def validate_content_counts_with_custom_modules() -> None:
    ORIGINAL_CONTENT_COUNTS()

    # Módulo 07: cuestionario propio de 20 preguntas.
    discard("Módulo 07: cuestionario con 6 preguntas")
    q07 = require(M07 / "cuestionario.html", "Módulo 07")
    if q07 and 'data-question-count="20"' not in q07:
        base.error("Módulo 07: el cuestionario avanzado no declara 20 preguntas")

    # Módulo 08: el index personalizado reemplaza el checklist genérico.
    discard("Módulo 08: total de recursos inconsistente")
    required = {
        "index.html", "presentacion-01.html", "presentacion-02.html",
        "simulacion.html", "guia.html", "cuestionario.html",
        "glosario.html", "styles.css", "site.js",
    }
    missing = sorted(name for name in required if not (M08 / name).is_file())
    if missing:
        base.error("Módulo 08: faltan recursos avanzados: " + ", ".join(missing))
        return

    q08 = (M08 / "cuestionario.html").read_text(encoding="utf-8")
    if 'data-question-count="30"' not in q08:
        base.error("Módulo 08: el cuestionario avanzado no declara 30 preguntas")

    sim = (M08 / "simulacion.html").read_text(encoding="utf-8")
    for i in range(1, 15):
        marker = f'id="s{i}"'
        if marker not in sim:
            base.error(f"Módulo 08: falta simulación integrada {i:02d}")
    if "Predict → Move → Observe → Explain" not in sim:
        base.error("Módulo 08: falta método didáctico de experimentación")

    index = (M08 / "index.html").read_text(encoding="utf-8")
    for resource in ("presentacion-01.html", "presentacion-02.html", "simulacion.html",
                     "guia.html", "cuestionario.html", "glosario.html"):
        if resource not in index:
            base.error(f"Módulo 08: recurso {resource} ausente del portal")

base.validate_content_counts = validate_content_counts_with_custom_modules

if __name__ == "__main__":
    raise SystemExit(base.main())
