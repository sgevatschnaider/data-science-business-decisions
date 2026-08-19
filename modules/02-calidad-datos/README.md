# Módulo 02: Calidad de datos y valores faltantes

Diagnosticar completitud, validez, consistencia, duplicados y mecanismos de ausencia antes de imputar.

## Pregunta de decisión

¿La evidencia disponible representa el proceso real o sus defectos pueden cambiar la conclusión y perjudicar la decisión?

## Índice interactivo

| Recurso | Acceso |
|---|---|
| Guía principal | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/02-calidad-datos/index.html) |
| Diapositivas 01 · Calidad de datos y decisiones | [Abrir](https://docs.google.com/presentation/d/1CAvqHS1RNvTdth7VzIxJ1fzm82NA8smheyvRh_PerkM/view?usp=sharing) |
| Diapositivas 02 · Missing Data: MCAR, MAR y MNAR | [Abrir](https://docs.google.com/presentation/d/1ejHnIv-QppNEq1mcEKFA_F_euYJFFJFkrbggV6LubM8/view?usp=sharing) |
| Diapositivas 03 · Imputación, pipelines y efecto sobre modelos | [Abrir](https://docs.google.com/presentation/d/1hfBu_-gMoQaNWPyiY41OmWw9Zi3U1IMFmX6eEvpB0KY/view?usp=sharing) |
| Simulación interactiva | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/02-calidad-datos/simulacion.html) |
| Colab 01 · Calidad de datos | [Abrir](https://colab.research.google.com/github/sgevatschnaider/data-science-business-decisions/blob/main/notebooks/02-calidad-datos.ipynb) |
| Colab 02 · Missing Data: marco conceptual | [Abrir](https://colab.research.google.com/drive/1_ldjrvEBsIlo3_GvoKJ3tUXdmjG_Nvq2?usp=sharing) |
| Colab 03 · Missing Data: House Prices | [Abrir](https://colab.research.google.com/drive/1YUFaKt8HslnUmE9_2pyjtxg3Lt5k5HYn?usp=sharing) |
| Cuestionario | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/02-calidad-datos/cuestionario.html) |
| Glosario | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/02-calidad-datos/glosario.html) |

## Presentaciones

### Diapositivas 01 · Calidad de datos y decisiones

Desarrolla la calidad de datos como condición para una decisión defendible: completitud, validez, consistencia, unicidad, oportunidad, trazabilidad, reglas de negocio, severidad, gobernanza y costo estadístico y económico del error.

### Diapositivas 02 · Missing Data: MCAR, MAR y MNAR

Explica ausencia estructural y omisión problemática, mecanismos MCAR, MAR y MNAR, diagnóstico visual, sesgo, hipótesis de ausencia y alternativas de tratamiento según el proceso que generó los faltantes.

### Diapositivas 03 · Imputación, pipelines y efecto sobre modelos

Conecta la imputación con modelado y producción: eliminación, media, mediana, imputación por grupo, indicadores de ausencia, leakage, separación train/test, pipelines reproducibles, House Prices y evaluación sobre distribución, segmentos, métricas y decisión.

## Resultados de aprendizaje

- Definir pruebas de calidad alineadas con reglas de negocio.
- Distinguir ausencia MCAR, MAR y MNAR como hipótesis de trabajo.
- Comparar eliminación, imputación simple y estrategias multivariadas.
- Documentar impacto, trazabilidad e indicadores de ausencia.

## Caso de negocio

En una solicitud de crédito faltan ingresos con mayor frecuencia en trabajadores independientes. Imputar sin segmentar puede ocultar una diferencia estructural.

## Profundización aplicada

- Pruebas de esquema, unicidad, frescura y consistencia entre fuentes.
- Análisis de sensibilidad para mecanismos MCAR, MAR y MNAR.
- Calidad como producto: responsables, alertas, severidad y acuerdos de servicio.

## Errores frecuentes

- Imputar antes de separar entrenamiento y evaluación.
- Tratar todos los faltantes como un mismo fenómeno.
- Corregir datos sin conservar la evidencia original ni la regla aplicada.

## Desafío de transferencia

Definí qué defectos bloquean una decisión, cuáles admiten corrección y cuáles exigen recolectar datos nuevamente.

## Secuencia de práctica

1. Definir clave, rangos y reglas de consistencia.
2. Medir faltantes por variable y por segmento.
3. Crear indicadores de ausencia antes de imputar.
4. Comparar distribución y métrica posterior a cada tratamiento.

## Laboratorios complementarios

### Colab 02 · Missing Data: marco conceptual

Notebook teórico-conceptual que desarrolla los datos faltantes desde una perspectiva estadística, organizacional y económica. Integra ausencia estructural, mecanismos MCAR, MAR y MNAR, calidad y gobernanza de datos, y consecuencias sobre métricas, segmentaciones, modelos predictivos y decisiones de negocio.

### Colab 03 · Missing Data: House Prices

Notebook práctico basado en House Prices para detectar, cuantificar, visualizar e interpretar patrones de ausencia. Compara estrategias de tratamiento e indicadores de faltantes y analiza su efecto sobre pipelines y modelos predictivos como Ridge y Random Forest.

## Entregable

Reporte de calidad con reglas automatizadas, mapa de faltantes, hipótesis del mecanismo y comparación de dos estrategias.

## Autoría

Material elaborado por el profesor Sergio Gevatschnaider.
