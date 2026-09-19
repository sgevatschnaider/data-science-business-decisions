"""Extiende la validación general para módulos con páginas docentes personalizadas.

Los módulos 07 y 08 conservan datos mínimos en course_data.py para compatibilidad con
el generador histórico. El Módulo 08 publica además los HTML docentes originales
completos y verifica su integridad mediante SHA-256 para impedir simplificaciones
accidentales en builds futuros.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import validate_repo as base

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_CONTENT_COUNTS = base.validate_content_counts
M07 = ROOT / "modules/07-series-tiempo/site"
M08 = ROOT / "modules/08-regresion-logistica/site"

M08_ORIGINAL_SHA256 = {
    "simuladores/simulador_01_funcion_sigmoide_regresion_logistica.html": "f3b7e6c8196c28c6570c16db7693da4845be4cb790c971c3fe9a014c192640ff",
    "simuladores/simulador_02_probabilidad_odds_logit_odds_ratio.html": "ad0779932ca7c150ef922656db7cd2c88ceb14dddcafd12e743b73f94bbfd982",
    "simuladores/simulador_03_efectos_marginales_regresion_logistica.html": "c543060d3557af93c7863f5abf47eb2851ba20a63c1234b923feb6ce0c627fc8",
    "simuladores/simulador_04_log_loss_maxima_verosimilitud.html": "087f5daaa0901d3d3361fe388aae1511301c6bdfd786d11d18c323f13a99f3b6",
    "simuladores/simulador_05_threshold_matriz_confusion_metricas.html": "95cc137e2738d40aafc2a5c3cd7cf3a4249e3e40c9cdb2f3badee2db7e644ee1",
    "simuladores/simulador_06_roc_precision_recall_desbalance.html": "a1ece83d2504e8a7f6eb12102ff65fbc7ab935e261e169e71f3a3b4bca227e76",
    "simuladores/simulador_07_frontera_decision_2d_regresion_logistica.html": "6ec41675f8ab2773b0db5b5b7cd25237e463b71fd879cbe631108e8d8d3d9a3a",
    "simuladores/simulador_08_regularizacion_l1_l2_overfitting.html": "8630f659d342a200b421a0497af60c17d16bb0e98f9996c99c92ecf3cf68c988",
    "simuladores/simulador_09_dummies_interacciones_no_linealidades.html": "afec1fb923187fcafdaf8a6a554ddc0682cd16d856fbbe20cf18bc7b180f0da8",
    "simuladores/simulador_10_train_validation_test_kfold_cross_validation.html": "2f318e21a5f182270000a3d22092656ccba1e117745ef8ec433be1b88a9e2a9e",
    "simuladores/simulador_11_calibracion_vs_discriminacion.html": "86f9ad34282f8d5381bbeb1b32d4807d98b7ac0e20623b1d447fc51bc490edb1",
    "simuladores/simulador_12_decision_lab_credit_scoring_costos.html": "ce89bd6daa32cb2ca3f3c114aa6aeaf3be749e5d4896cecd96a2aca65e9ea9d8",
    "simuladores/simulador_13_softmax_clasificacion_multiclase.html": "b79ed2ca164c5161718dd14ee8b3b17d7a6101fc597e53dcc365ae3410a4d03f",
    "simuladores/simulador_14_model_drift_monitoring.html": "737639ce961eb79603b050e84dec71738f6c046d3041ab6f00aa93d60feaeaf8",
    "glosario.html": "ac5f3d507d409a6e6cc4dfee87ae7b84e21c7c93a19f6e29fc17812ee3afad0b",
    "cuestionario.html": "649d2efc9e703bf6aa53656c1266713d051f1cad9ddf04226304b03ecc6385c9",
}

def discard(fragment: str) -> None:
    base.ERRORS[:] = [e for e in base.ERRORS if fragment not in e]

def require(path: Path, label: str) -> str:
    if not path.is_file():
        base.error(f"{label}: falta {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def validate_content_counts_with_custom_modules() -> None:
    ORIGINAL_CONTENT_COUNTS()

    # Módulo 07: cuestionario propio de 20 preguntas.
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

    # Integridad exacta de los HTML originales provistos por el docente.
    for relative, expected in M08_ORIGINAL_SHA256.items():
        target = M08 / relative
        if not target.is_file():
            base.error(f"Módulo 08: falta original {relative}")
            continue
        actual = sha256(target)
        if actual != expected:
            base.error(
                f"Módulo 08: {relative} fue modificado o simplificado "
                f"(SHA-256 {actual}, esperado {expected})"
            )

    # Comprobaciones pedagógicas mínimas sobre los originales.
    q08 = require(M08 / "cuestionario.html", "Módulo 08")
    if q08:
        if "30 preguntas para comprender, calcular y decidir" not in q08:
            base.error("Módulo 08: el cuestionario original no declara su recorrido de 30 preguntas")
        if '"id": 30' not in q08:
            base.error("Módulo 08: no se detecta la pregunta 30 del cuestionario original")

    glossary = require(M08 / "glosario.html", "Módulo 08")
    if glossary and glossary.count("<details") < 88:
        base.error("Módulo 08: el glosario original no conserva sus 88 entradas")

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

base.validate_content_counts = validate_content_counts_with_custom_modules

if __name__ == "__main__":
    raise SystemExit(base.main())
