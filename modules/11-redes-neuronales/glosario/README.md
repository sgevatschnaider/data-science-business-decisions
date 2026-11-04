# Glosario y guía de estudio: redes neuronales, secuencias, RNN y LSTM

Guía de Sergio Gevatschnaider para Ciencias de Datos II, UCA. El programa identifica este tema como Módulo 12; se conserva la URL histórica `11-redes-neuronales`.

La versión desarrollada contiene 102 entradas y 102 preguntas con respuesta, distribuidas en fundamentos (20), aprendizaje (21), evaluación y decisiones (14), secuencias (14), RNN (16) y LSTM/GRU y conexiones modernas (17).

Cada entrada desarrolla definición, mecanismo, notación o relación clave, ejemplo, error frecuente y una pregunta con solución orientativa. Los ejemplos son didácticos y no representan estimaciones de impacto comercial real.

## Edición y publicación

- `contenido.txt`: fuente editorial UTF-8. Cada unidad comienza con `## id|número|título|subtítulo|recurso`. Cada entrada usa nueve campos separados por `|`: título, sinónimos, definición, mecanismo, fórmula, ejemplo, error, pregunta, respuesta. En las fórmulas se escribe `abs(x)` para evitar ambigüedad con el separador.
- `plantilla.html`, `estilos.css` e `interacciones.js`: interfaz, temas, impresión y controles.
- `python scripts/build_m11_glossary.py`: regenera `docs/modulos/11-redes-neuronales/glosario.html`, autónomo y sin dependencias externas.
- `python scripts/build_course.py`: también regenera esta guía; `custom_page_files` impide reemplazarla por el glosario breve.
- `python scripts/validate_module11.py`: comprueba los enlaces del módulo y la integridad de los recursos conservados.

El HTML permite lectura completa sin JavaScript. El buscador ignora tildes, combina palabras, filtra unidades y pendientes; el índice A–Z y los enlaces permanentes revelan entradas ocultas. Los temas oscuro, claro y de alto contraste comparten preferencia con la experiencia del módulo. El avance se guarda únicamente en el navegador y degrada a memoria temporal si no hay almacenamiento disponible.

## Accesos

- Guía completa: `glosario.html`.
- Redes neuronales: `glosario.html?recorrido=redes#biblioteca`.
- Secuencias, RNN y LSTM: `glosario.html?recorrido=secuencias#biblioteca`.
- Una unidad: `glosario.html?unidad=rnn#biblioteca` o `?unidad=lstm#biblioteca`.
- Un concepto: `glosario.html#estado-de-celda`.

El botón de impresión muestra todas las unidades, preguntas y respuestas, incluso si se activaron filtros. El diálogo del navegador permite guardar un PDF.

## Controles numéricos

1. Neurona: sigmoide, BCE y gradiente respecto del logit, con etiqueta 1.
2. RNN escalar: seis pasos con entrada `(1,0,0,0,0,0)` y peso recurrente editable.
3. LSTM escalar: conservación y escritura editables; los valores manuales de las compuertas son una simplificación didáctica, no un entrenamiento de LSTM.

Las convenciones de parámetros con uno o dos sesgos, la ruta directa del gradiente LSTM y los límites de los ejemplos de persistencia se explican expresamente.
