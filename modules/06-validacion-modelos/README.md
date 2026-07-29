# Módulo 06: Validación, selección y generalización

Diseñar particiones, baselines y validación cruzada que estimen el desempeño futuro sin contaminar la evaluación.

## Pregunta de decisión

¿El desempeño observado representa casos futuros o es una consecuencia del azar, el sobreajuste o una partición incorrecta?

## Índice interactivo

| Recurso | Acceso |
|---|---|
| Guía principal | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/06-validacion-modelos/index.html) |
| Simulación interactiva | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/06-validacion-modelos/simulacion.html) |
| Cuestionario | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/06-validacion-modelos/cuestionario.html) |
| Glosario | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/06-validacion-modelos/glosario.html) |
| Notebook en Colab | [Abrir](https://colab.research.google.com/github/sgevatschnaider/data-science-business-decisions/blob/main/notebooks/06-validacion-modelos.ipynb) |

## Resultados de aprendizaje

- Separar entrenamiento, validación y test por su función.
- Elegir K-Fold, estratificación, grupos o cortes temporales.
- Comparar modelos contra baselines relevantes.
- Reportar distribución de métricas y no solo un promedio.

## Caso de negocio

Un scoring entrenado con operaciones de los mismos clientes en train y test parece excelente, pero falla con clientes nuevos.

## Secuencia de práctica

1. Identificar dependencias temporales o por entidad.
2. Construir un baseline antes de optimizar.
3. Aplicar el esquema de validación dentro del pipeline.
4. Reportar media, dispersión y comparación con test.

## Entregable

Protocolo de validación justificado, baseline, tabla de métricas por fold y evaluación final reservada.

## Autoría

Material elaborado por el profesor Sergio Gevatschnaider.
