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
        ("Laboratorio de la Función Sigmoide · Regresión Logística", 25928),
    "simuladores/simulador_02_probabilidad_odds_logit_odds_ratio.html":
        ("Simulador 02 · Probabilidad, Odds, Logit y Odds Ratio", 25515),
    "simuladores/simulador_03_efectos_marginales_regresion_logistica.html":
        ("Simulador 03 · Efectos Marginales en Regresión Logística", 23633),
    "simuladores/simulador_04_log_loss_maxima_verosimilitud.html":
        ("Simulador 04 · Log-Loss y Máxima Verosimilitud", 23396),
    "simuladores/simulador_05_threshold_matriz_confusion_metricas.html":
        ("Simulador 05 · Threshold Lab — Matriz de Confusión y Métricas", 24893),
    "simuladores/simulador_06_roc_precision_recall_desbalance.html":
        ("Simulador 06 · ROC, Precision–Recall y Desbalance", 28429),
    "simuladores/simulador_07_frontera_decision_2d_regresion_logistica.html":
        ("Simulador 07 · Frontera de Decisión 2D", 25349),
    "simuladores/simulador_08_regularizacion_l1_l2_overfitting.html":
        ("Simulador 08 · Regularización L1/L2 y Overfitting", 30366),
    "simuladores/simulador_09_dummies_interacciones_no_linealidades.html":
        ("Simulador 09 · Dummies, Interacciones y No Linealidades", 26637),
    "simuladores/simulador_10_train_validation_test_kfold_cross_validation.html":
        ("Simulador 10 · Train, Validation, Test y K-Fold Cross-Validation", 30959),
    "simuladores/simulador_11_calibracion_vs_discriminacion.html":
        ("Simulador 11 · Calibración vs Discriminación", 27636),
    "simuladores/simulador_12_decision_lab_credit_scoring_costos.html":
        ("Simulador 12 · Decision Lab — Credit Scoring, Threshold y Costos", 35061),
    "simuladores/simulador_13_softmax_clasificacion_multiclase.html":
        ("Simulador 13 · Softmax y Clasificación Multiclase", 24530),
    "simuladores/simulador_14_model_drift_monitoring.html":
        ("Simulador 14 · Model Drift & Monitoring", 35732),
    "glosario.html":
        ("Glosario avanzado · Regresión Logística y Clasificación", 186615),
    "cuestionario.html":
        ("Cuestionario avanzado · Regresión Logística", 49861),
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

base.validate_visible_content = validate_visible_content_with_original_m08
base.validate_content_counts = validate_content_counts_with_custom_modules

if __name__ == "__main__":
    raise SystemExit(base.main())
