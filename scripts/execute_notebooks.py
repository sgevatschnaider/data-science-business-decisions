"""Ejecuta todos los laboratorios en un directorio temporal y falla ante errores."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "notebooks"


def main() -> int:
    paths = sorted(NOTEBOOKS.glob("*.ipynb"))
    if not paths:
        print("No se encontraron notebooks")
        return 1

    os.environ.setdefault("MPLBACKEND", "Agg")
    failures: list[str] = []
    with tempfile.TemporaryDirectory(prefix="course-notebooks-") as directory:
        runtime_dir = Path(directory)
        for path in paths:
            notebook = nbformat.read(path, as_version=4)
            client = NotebookClient(
                notebook,
                timeout=180,
                kernel_name="python3",
                resources={"metadata": {"path": str(runtime_dir)}},
                allow_errors=False,
            )
            try:
                client.execute()
            except (CellExecutionError, TimeoutError, RuntimeError) as exc:
                failures.append(f"{path.name}: {exc}")
                print(f"FALLÓ {path.name}")
            else:
                print(f"OK {path.name}")

    if failures:
        print(f"Fallaron {len(failures)} notebook(s):")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"Ejecución completa: {len(paths)} notebooks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
