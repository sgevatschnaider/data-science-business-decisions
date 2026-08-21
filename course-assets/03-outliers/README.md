# Outliers Lab — simulaciones interactivas

Material elaborado por el profesor Sergio Gevatschnaider.

## Archivos
- `simulacion.html`: hub principal del laboratorio.
- `sim-01-iqr-z-mad.html`
- `sim-02-influencia-regresion.html`
- `sim-03-multivariado.html`
- `sim-04-isolation-forest.html`
- `sim-05-lof-ocsvm.html`
- `sim-06-model-arena.html`
- `cuestionario.html`: 30 preguntas desarrolladas con filtros y progreso local.
- `glosario.html`: 62 conceptos con buscador y categorías.

Todos los HTML son autocontenidos: CSS + JavaScript están embebidos y no requieren dependencias externas.

## Integración en el curso

Estos archivos son la fuente de los recursos especiales del Módulo 03. El
comando `python scripts/build_course.py` los copia de forma determinística a
`docs/modulos/03-outliers/`; luego `python scripts/embed_eda_slides.py` agrega
los visores de Google Slides a la guía principal.

## Temas
Cada archivo incluye un botón que rota entre:
Océano → Noche → Papel → Aurora.
