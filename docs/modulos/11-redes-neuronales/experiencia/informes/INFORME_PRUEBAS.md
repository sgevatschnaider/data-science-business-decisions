# Informe de pruebas

Fecha: 03/11/2026. Clase prevista: 05/11/2026, 9:30–12:00, Buenos Aires.

## Presentaciones y sincronía

- Fundamentos: 51 diapositivas PPTX = 51 páginas PDF = 51 imágenes WebP.
- RNN/LSTM: 34 diapositivas PPTX = 34 páginas PDF = 34 imágenes WebP.
- PPTX reimportados por el motor de presentaciones y validados por integridad, geometría y fuentes. Texto, diagramas y ecuaciones permanecen como objetos nativos. Los gráficos incorporan datos editables en libros de Excel.
- Apertura y exportación de ambos PPTX en LibreOffice. PDF y WebP derivan de esos mismos archivos finales. No se afirma una apertura en Microsoft PowerPoint.
- Renderizadas las 85 páginas. Revisión visual de mosaicos completos y de slides con fórmulas, tabla de confusión y ejemplos LSTM. Se corrigieron desbordes en cifras destacadas, contraste de títulos de ejes y un gráfico de descenso que no correspondía al ejemplo numérico.
- Títulos y orden PDF comprobados contra el catálogo. SHA256 de PPTX/PDF/WebP en `asset-manifest.json`. Todas las slides tienen notas, transcripción, pregunta, respuesta y fuentes.

## Matemática

`node scripts/module11/test_math.cjs`: PASS.

Casos: sigmoide estable con logits extremos, BCE, derivadas de activaciones, diferencias finitas de gradientes w/b, descenso de pérdida, OR/AND, XOR constructivo con dos ReLU, cohorte con semilla fija, matriz y costo de todos los contactos, precision indefinida sin contactos, c/h LSTM y persistencia, estabilidad/divergencia de la parábola.

## Navegador real

Playwright con Chromium headless 131. Cinco laboratorios y dos visores: PASS, sin excepciones JavaScript. Ver `PRUEBAS_NAVEGADOR.json`.

Comprobados: autoplay modifica estado, clics repetidos no acumulan timers, pausa/reanudar, paso, reinicio, tres escenarios por laboratorio, velocidad, exportación CSV real, Fullscreen/exit, temas claro/oscuro/alto contraste y persistencia tras recarga. Viewport móvil de 390×844 sin desbordamiento horizontal. Respeto de movimiento reducido mediante menor frecuencia. Visores: anterior/siguiente, Home/End, búsqueda, selección, ruta esencial de 28 slides, recursos contextuales y retorno al mismo slide/ruta. Portadas, guías y páginas de videos abiertas sin errores.

`python scripts/validate_module11.py`: PASS. Revisa rutas locales de todo el módulo, referencias a laboratorios/videos, igualdad de catálogos con la fuente, 85 notas, cantidad de archivos, títulos PDF y hashes.

No se realizó una auditoría exhaustiva con lector de pantalla ni certificación WCAG. Sí se implementan etiquetas, foco visible, tabla textual del canvas, semántica y navegación por teclado.

## Notebook

Las siete celdas de código se ejecutaron, incluida LSTM CPU con PyTorch 2.15.0+cpu. Fuentes sintéticas y semilla 42. Resultados exactos en `RESULTADOS_NOTEBOOK.json`.

- Churn: logística ROC-AUC 0,8541, AP 0,5119; MLP ROC-AUC 0,8973, AP 0,6306. Utilidad proxy test 515 y 635 UM, con umbrales elegidos en validación. No representa retención real.
- Demanda: MAE del estacional 3,4851, Ridge 2,6955 y LSTM 6,0543 unidades. La LSTM pierde en este ejemplo. No se oculta ese resultado.
- La MLP alcanza el límite de 400 iteraciones y emite ConvergenceWarning. La ejecución termina correctamente. La comparación es una demostración con presupuesto fijado, no una certificación de óptimos de cada arquitectura.

## Repositorio y construcción general

Se ejecutó en una copia aislada el flujo existente: `build_course.py`, `embed_eda_slides.py`, `publish_module07.py`, `publish_module08.py`, `publish_module09.py` y `validate_repo_course.py`: PASS en todos los pasos. La construcción conserva los nuevos recursos y no los reemplaza por el contenido anterior.

La validación directa de la instantánea sin reconstruir muestra dos faltantes de encabezados del notebook 08, exactamente iguales en el commit base. Después del flujo de construcción normal la validación general pasa. `build_course.py --check` también señala diferencias preexistentes fuera del módulo; se documentan y no se editan otros módulos para corregirlas.

## Videos y publicación

Seis URLs, títulos y canales corroborados con YouTube oEmbed. No se descargaron videos. No se verificó reproducción completa, disponibilidad regional, audio alternativo ni subtítulos.

La URL histórica del módulo respondió HTTP 200 antes del cambio. La experiencia nueva está preparada en rama/PR y no se fusiona ni se publica en main sin aprobación. Las URLs nuevas de GitHub Pages son destinos posteriores a la fusión; no se presentan como ya publicadas.
