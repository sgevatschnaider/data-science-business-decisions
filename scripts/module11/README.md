# Construcción del módulo de redes neuronales

Fuente única de contenido: `decks.json`. De allí se generan `catalog.json`, `data.js`, notas, transcripciones, visores y los PPTX. Editar el JSON de origen y regenerar todos los derivados.

## Regenerar

1. Node con `@oai/artifact-tool`, Python con PyMuPDF y Pillow, y LibreOffice (`soffice`) en PATH.
2. Ejecutar `node scripts/module11/build_decks.mjs`. El entorno Codex usa el paquete y el finalizador de presentaciones del runtime. Fuera de ese entorno hay que proporcionar el mismo paquete y el finalizador señalado en el script.
3. Ejecutar `python scripts/module11/build_web.py`.
4. Ejecutar `python scripts/module11/render_exports.py`. Exporta cada PPTX final en LibreOffice, deriva sus WebP y actualiza hashes. PDF y WebP salen de la misma representación del PPTX.
5. Ejecutar `node scripts/module11/test_math.cjs` y `python scripts/validate_module11.py`.

Las curvas matemáticas de los gráficos tienen datos literales calculados y redondeados a seis decimales. El PPTX incorpora workbooks editables. Las ecuaciones, diagramas y textos son objetos nativos. No se rasteriza una diapositiva dentro del PPTX.

## Prueba de navegador

`node scripts/module11/test_browser.cjs` requiere Playwright y Chromium. Puede definirse `CHROMIUM_PATH` para un ejecutable existente. La prueba arranca un servidor local temporal, comprueba siete laboratorios y dos visores y lo detiene al finalizar. Los resultados se escriben en el directorio temporal de pruebas, no cambian el contenido del sitio.

El generador general del curso conserva `index.html`, `simulacion.html`, `experiencia/`, el notebook y el README de este módulo mediante sus flags `custom_*` en `course_data.py`.

Los seis videos se verificaron con metadatos YouTube oEmbed, sin descargar contenido audiovisual. La reproducción completa y los subtítulos no están certificados.

## Diseño visual y temas desarrollados

La referencia es la página publicada del Módulo 07: fondo #050b14, cian #2bd4e8, violeta #8a70ff y ámbar #f3b94c. El tema claro conserva las familias de color con tonos más oscuros para texto legible. `theme.css` gobierna la web, `scenes.mjs` los diagramas nativos del PPTX y `extras.js` las visualizaciones complementarias de cada laboratorio.

Los nueve temas de `decks.json` generan `temas.html` y se vinculan desde cada slide. Los laboratorios 06 y 07 agregan backpropagation y capacidad/generalización. `python scripts/module11/test_fit.py` contrasta 27 ajustes y sus errores con NumPy, además de las diferencias finitas de `test_math.cjs`.
