# Transformación de variables — recursos interactivos

Material elaborado por el profesor Sergio Gevatschnaider.

## Archivos fuente

- `01_Fundamentos_y_criterio_de_decision.pptx`: presentación original de 14 diapositivas; el sitio enlaza su conversión nativa a Google Slides.
- `simulacion.html`: laboratorio principal y centro de acceso a los doce simuladores.
- `01-distancia-unidades-knn.html`
- `02-comparador-escaladores.html`
- `03-transformaciones-forma.html`
- `04-outliers-centro-escala.html`
- `05-pca-covarianza-correlacion.html`
- `06-arena-algoritmos-escala.html`
- `07-columnas-filas-objetivo.html`
- `08-leakage-validacion.html`
- `09-constructor-pipelines.html`
- `10-transformacion-variable-objetivo.html`
- `11-clustering-documentos.html`
- `12-selector-transformaciones.html`
- `cuestionario.html`: 20 preguntas desarrolladas con modos de estudio y evaluación.
- `glosario.html`: 84 términos con buscador, filtros, favoritos, progreso y comprobación de comprensión.

Son 16 archivos didácticos fuente: una presentación, un laboratorio principal, doce simulaciones, un cuestionario y un glosario. Los HTML incluyen su CSS y JavaScript.

## Integración en el curso

`python scripts/build_course.py` copia los 15 HTML de forma determinística a `docs/modulos/04-transformacion-pipelines/`. Durante la construcción también genera el alias histórico `00-laboratorio-transformacion-variables.html`, requerido por los enlaces de regreso de los simuladores. Luego `python scripts/embed_eda_slides.py` agrega el visor responsive de Google Slides a la guía principal.

El notebook `notebooks/04-transformacion-pipelines.ipynb` se conserva sin cambios.

## Temas

Los recursos cubren escala, forma, robustez, PCA, algoritmos sensibles a escala, objeto transformado, leakage, pipelines, transformación del objetivo, clustering de documentos y selección razonada.
