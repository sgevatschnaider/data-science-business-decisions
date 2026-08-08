# Módulo 02: Calidad de datos y valores faltantes

Diagnosticar completitud, validez, consistencia, duplicados y mecanismos de ausencia antes de imputar.

## Pregunta de decisión

¿La evidencia disponible representa el proceso real o sus defectos pueden cambiar la conclusión y perjudicar la decisión?

## Índice interactivo

| Recurso | Acceso |
|---|---|
| Guía principal | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/02-calidad-datos/index.html) |
| Simulación interactiva | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/02-calidad-datos/simulacion.html) |
| Cuestionario | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/02-calidad-datos/cuestionario.html) |
| Glosario | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/02-calidad-datos/glosario.html) |
| Notebook en Colab | [Abrir](https://colab.research.google.com/github/sgevatschnaider/data-science-business-decisions/blob/main/notebooks/02-calidad-datos.ipynb) |

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

## Entregable

Reporte de calidad con reglas automatizadas, mapa de faltantes, hipótesis del mecanismo y comparación de dos estrategias.

## Autoría

Material elaborado por el profesor Sergio Gevatschnaider.
