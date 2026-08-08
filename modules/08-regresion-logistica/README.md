# Módulo 08: Regresión logística y decisiones de clasificación

Estimar probabilidades, evaluar ranking y calibración, y elegir umbrales según costos, capacidad y valor.

## Pregunta de decisión

¿A quién conviene asignar una acción cuando los errores tienen costos distintos y la capacidad es limitada?

## Índice interactivo

| Recurso | Acceso |
|---|---|
| Guía principal | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/08-regresion-logistica/index.html) |
| Simulación interactiva | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/08-regresion-logistica/simulacion.html) |
| Cuestionario | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/08-regresion-logistica/cuestionario.html) |
| Glosario | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/08-regresion-logistica/glosario.html) |
| Notebook en Colab | [Abrir](https://colab.research.google.com/github/sgevatschnaider/data-science-business-decisions/blob/main/notebooks/08-regresion-logistica.ipynb) |

## Resultados de aprendizaje

- Interpretar probabilidad, logit y odds.
- Leer matrices de confusión y métricas por clase.
- Distinguir discriminación, calibración y decisión.
- Elegir umbrales con costos y restricciones de capacidad.

## Caso de negocio

Una campaña de retención solo puede contactar al 15 por ciento de la cartera; el equipo debe ordenar riesgo y estimar valor neto por contacto.

## Profundización aplicada

- Calibración fuera de muestra, Brier score y diagramas de confiabilidad.
- Curvas de ganancia, lift, capacidad y valor neto por política.
- Tuning del umbral separado del entrenamiento y análisis por segmentos.

## Errores frecuentes

- Evaluar probabilidades sobre los mismos casos usados para ajustar.
- Elegir 0,5 por costumbre o maximizar F1 sin función de valor.
- Confundir buen ranking con probabilidades confiables.

## Desafío de transferencia

Elegí una política de contacto con capacidad limitada y costos distintos por falso positivo y falso negativo.

## Secuencia de práctica

1. Definir clase positiva y consecuencias de error.
2. Construir un baseline de prevalencia.
3. Evaluar ranking, calibración y métricas a varios umbrales.
4. Elegir una política compatible con capacidad y valor.

## Entregable

Modelo probabilístico con curva de calibración, matriz de confusión, selección de umbral y matriz de costos.

## Autoría

Material elaborado por el profesor Sergio Gevatschnaider.
