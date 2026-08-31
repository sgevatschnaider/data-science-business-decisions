# Módulo 04: Transformación de variables y pipelines

Transformar, escalar, codificar y construir variables sin filtrar información ni romper la reproducibilidad.

## Pregunta de decisión

¿Cómo representamos los datos para que un modelo aprenda el patrón correcto y pueda repetirse exactamente en producción?

## Índice interactivo

| Recurso | Acceso |
|---|---|
| Guía principal | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/04-transformacion-pipelines/index.html) |
| Diapositivas · Fundamentos y criterio de decisión | [Abrir](https://docs.google.com/presentation/d/1a5I_FUqCfgHIOlatzfu7B5h2MLku583V-Sp8ls6y6tk/view?usp=sharing) |
| Simulación interactiva | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/04-transformacion-pipelines/simulacion.html) |
| Colab · Transformación y pipelines | [Abrir](https://colab.research.google.com/github/sgevatschnaider/data-science-business-decisions/blob/main/notebooks/04-transformacion-pipelines.ipynb) |
| Cuestionario | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/04-transformacion-pipelines/cuestionario.html) |
| Glosario | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/04-transformacion-pipelines/glosario.html) |
| Simulación 01 · Distancia, unidades y KNN | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/04-transformacion-pipelines/01-distancia-unidades-knn.html) |
| Simulación 02 · Comparador de escaladores | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/04-transformacion-pipelines/02-comparador-escaladores.html) |
| Simulación 03 · Transformaciones de forma | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/04-transformacion-pipelines/03-transformaciones-forma.html) |
| Simulación 04 · Outliers, centro y escala | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/04-transformacion-pipelines/04-outliers-centro-escala.html) |
| Simulación 05 · PCA, covarianza y correlación | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/04-transformacion-pipelines/05-pca-covarianza-correlacion.html) |
| Simulación 06 · Arena de algoritmos y escala | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/04-transformacion-pipelines/06-arena-algoritmos-escala.html) |
| Simulación 07 · Columnas, filas y objetivo | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/04-transformacion-pipelines/07-columnas-filas-objetivo.html) |
| Simulación 08 · Leakage y validación | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/04-transformacion-pipelines/08-leakage-validacion.html) |
| Simulación 09 · Constructor de pipelines | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/04-transformacion-pipelines/09-constructor-pipelines.html) |
| Simulación 10 · Transformación del objetivo | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/04-transformacion-pipelines/10-transformacion-variable-objetivo.html) |
| Simulación 11 · Clustering de documentos | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/04-transformacion-pipelines/11-clustering-documentos.html) |
| Simulación 12 · Selector de transformaciones | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/04-transformacion-pipelines/12-selector-transformaciones.html) |

## Resultados de aprendizaje

- Distinguir escalado, transformación de forma y normalización según el objeto que se modifica.
- Elegir estadísticas de centro y escala según algoritmo, geometría y presencia de outliers.
- Comparar PCA sobre covarianza y correlación sin confundir varianza con relevancia de negocio.
- Transformar features, texto, tiempo y variable objetivo conservando semántica e interpretación.
- Encapsular preparación y estimación dentro de pipelines y validación sin leakage.

## Caso de negocio

Un equipo segmenta clientes con edad, ingreso, antigüedad y reclamos. Sin escalar, el ingreso domina la distancia; si además calcula estadísticas con todo el dataset, la validación aprende indirectamente de casos futuros.

## Profundización aplicada

- Covarianza frente a correlación en PCA y estabilidad de componentes ante cambios de unidad.
- Transformaciones de potencia, cuantiles y objetivo dentro de validación anidada.
- Normalización por fila para texto, codificación cíclica y representación de categorías.
- Disponibilidad temporal y point-in-time correctness en ingeniería de variables.

## Errores frecuentes

- Usar un scaler para intentar resolver asimetría, outliers o errores de dominio.
- Normalizar filas cuando el problema requería escalar columnas, o viceversa.
- Calcular estadísticas de transformación con todo el dataset.
- Elegir una transformación por métrica sin revisar interpretación, estabilidad e inversión.
- Crear variables con datos posteriores al momento de decisión.

## Desafío de transferencia

Defendé un pipeline completo indicando qué se aprende en train, qué se conserva, qué puede distorsionarse y cómo se mide el resultado en unidades de negocio.

## Secuencia de práctica

1. Identificar si se transforma una columna, una fila, el objetivo, una categoría o el tiempo.
2. Diagnosticar dominio, ceros, negativos, forma, outliers, unidades y sensibilidad del algoritmo.
3. Comparar escaladores y transformaciones de forma sobre la misma referencia.
4. Contrastar PCA sobre datos crudos y estandarizados y documentar qué cambia.
5. Construir un ColumnTransformer dentro de un Pipeline y validarlo por fold.
6. Medir el resultado en unidades de negocio y registrar interpretación, riesgo y reversión.

## Entregable

Matriz de decisión por variable, comparación justificada de alternativas y pipeline reproducible con prueba explícita de que cada fit ocurre solo en train.

## Autoría

Material elaborado por el profesor Sergio Gevatschnaider.
