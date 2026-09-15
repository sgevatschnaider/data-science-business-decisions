"""Publica el sitio avanzado del Módulo 07 después del generador general.

El contenido canónico vive en ``modules/07-series-tiempo/site``. El build general
puede regenerar ``docs``; este paso repone de forma determinística la experiencia
completa de Series de Tiempo antes de validar y desplegar GitHub Pages.
"""
from __future__ import annotations

import shutil
from pathlib import Path

SOURCE = Path("modules/07-series-tiempo/site")
TARGET = Path("docs/modulos/07-series-tiempo")


def main() -> None:
    if not SOURCE.is_dir():
        raise SystemExit(f"No existe el sitio fuente: {SOURCE}")
    if TARGET.exists():
        shutil.rmtree(TARGET)
    shutil.copytree(SOURCE, TARGET)
    required = {
        "index.html", "simulacion.html", "cuestionario.html", "glosario.html",
        "presentacion-01.html", "presentacion-02.html", "presentacion-03.html",
    }
    missing = sorted(name for name in required if not (TARGET / name).is_file())
    if missing:
        raise SystemExit("Faltan archivos publicados: " + ", ".join(missing))
    print(f"Módulo 07 publicado desde {SOURCE} en {TARGET}.")


if __name__ == "__main__":
    main()
