"""Publica el sitio avanzado del Módulo 08 después del generador general."""
from __future__ import annotations
import shutil
from pathlib import Path

SOURCE = Path("modules/08-regresion-logistica/site")
TARGET = Path("docs/modulos/08-regresion-logistica")

def main() -> None:
    if not SOURCE.is_dir():
        raise SystemExit(f"No existe el sitio fuente: {SOURCE}")
    if TARGET.exists():
        shutil.rmtree(TARGET)
    shutil.copytree(SOURCE, TARGET)
    required = {"index.html","presentacion-01.html","presentacion-02.html","simulacion.html","guia.html","cuestionario.html","glosario.html","styles.css","site.js"}
    missing = sorted(name for name in required if not (TARGET / name).is_file())
    if missing:
        raise SystemExit("Faltan archivos publicados: " + ", ".join(missing))
    print(f"Módulo 08 publicado desde {SOURCE} en {TARGET}.")

if __name__ == "__main__":
    main()
