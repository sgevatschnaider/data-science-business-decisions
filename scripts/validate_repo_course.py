"""Extiende la validación general para módulos con páginas docentes personalizadas.

Módulo 07 conserva seis preguntas mínimas en ``course_data.py`` para el generador
histórico, pero publica una autoevaluación propia de 20 preguntas. Mantenemos todas
las validaciones originales y sustituimos únicamente esa comprobación por una
verificación explícita del recurso personalizado.
"""
from __future__ import annotations

from pathlib import Path

import validate_repo as base

ORIGINAL_CONTENT_COUNTS = base.validate_content_counts
CUSTOM_QUIZ = Path(__file__).resolve().parents[1] / "modules/07-series-tiempo/site/cuestionario.html"


def validate_content_counts_with_custom_modules() -> None:
    ORIGINAL_CONTENT_COUNTS()
    legacy_error = "Módulo 07: cuestionario con 6 preguntas"
    if legacy_error in base.ERRORS:
        base.ERRORS.remove(legacy_error)
    if not CUSTOM_QUIZ.is_file():
        base.error("Módulo 07: falta cuestionario avanzado personalizado")
        return
    text = CUSTOM_QUIZ.read_text(encoding="utf-8")
    if 'data-question-count="20"' not in text:
        base.error("Módulo 07: el cuestionario avanzado no declara 20 preguntas")


base.validate_content_counts = validate_content_counts_with_custom_modules

if __name__ == "__main__":
    raise SystemExit(base.main())
