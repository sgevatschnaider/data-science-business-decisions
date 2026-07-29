# Módulo 04: Transformación de variables y pipelines

Transformar, escalar, codificar y construir variables sin filtrar información ni romper la reproducibilidad.

## Pregunta de decisión

¿Cómo representamos los datos para que un modelo aprenda el patrón correcto y pueda repetirse exactamente en producción?

## Índice interactivo

| Recurso | Acceso |
|---|---|
| Guía principal | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/04-transformacion-pipelines/index.html) |
| Simulación interactiva | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/04-transformacion-pipelines/simulacion.html) |
| Cuestionario | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/04-transformacion-pipelines/cuestionario.html) |
| Glosario | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/04-transformacion-pipelines/glosario.html) |
| Notebook en Colab | [Abrir](https://colab.research.google.com/github/sgevatschnaider/data-science-business-decisions/blob/main/notebooks/04-transformacion-pipelines.ipynb) |

## Resultados de aprendizaje

- Elegir transformaciones según distribución, relación y algoritmo.
- Codificar categorías y escalar variables de forma segura.
- Crear variables con disponibilidad temporal explícita.
- Encapsular preparación y estimación en pipelines.

## Caso de negocio

Un modelo de demanda combina precios, categorías y recencia. Calcular promedios usando meses futuros produce métricas excelentes e inútiles.

## Secuencia de práctica

1. Clasificar variables por tipo y tratamiento.
2. Comparar escala original, logarítmica y estandarizada.
3. Construir un ColumnTransformer dentro de un Pipeline.
4. Verificar disponibilidad temporal de cada feature.

## Entregable

Pipeline reproducible con columnas numéricas y categóricas, variables derivadas documentadas y prueba explícita de no leakage.

## Autoría

Material elaborado por el profesor Sergio Gevatschnaider.
