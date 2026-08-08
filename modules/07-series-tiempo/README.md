# Módulo 07: Series de tiempo y backtesting

Modelar tendencia, estacionalidad y dependencia temporal con baselines honestos y evaluación de origen rodante.

## Pregunta de decisión

¿Qué parte del futuro es predecible usando solo la información disponible en cada momento de decisión?

## Índice interactivo

| Recurso | Acceso |
|---|---|
| Guía principal | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/07-series-tiempo/index.html) |
| Simulación interactiva | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/07-series-tiempo/simulacion.html) |
| Cuestionario | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/07-series-tiempo/cuestionario.html) |
| Glosario | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/07-series-tiempo/glosario.html) |
| Notebook en Colab | [Abrir](https://colab.research.google.com/github/sgevatschnaider/data-science-business-decisions/blob/main/notebooks/07-series-tiempo.ipynb) |

## Resultados de aprendizaje

- Reconocer tendencia, estacionalidad, ciclos y ruido.
- Crear lags y ventanas móviles sin usar el futuro.
- Construir baselines ingenuos y estacionales.
- Evaluar múltiples horizontes con backtesting.

## Caso de negocio

Un comercio pronostica demanda semanal para decidir inventario. Los errores por defecto generan quiebres; por exceso, capital inmovilizado.

## Profundización aplicada

- Pronósticos probabilísticos, cuantiles y cobertura de intervalos.
- Demanda intermitente, jerarquías y reconciliación entre niveles.
- Forecast Value Added para medir si cada etapa mejora un baseline.

## Errores frecuentes

- Mezclar pasado y futuro o usar ventanas centradas.
- Elegir un único horizonte y ocultar degradación a largo plazo.
- Comparar contra un baseline demasiado débil.

## Desafío de transferencia

Definí cuantiles de demanda que minimicen el costo conjunto de stock, urgencias y pérdida de ventas.

## Secuencia de práctica

1. Ordenar frecuencia, huecos y duplicados temporales.
2. Descomponer nivel, tendencia y estacionalidad.
3. Crear features rezagadas dentro de cada corte.
4. Comparar modelos y baselines en backtesting.

## Entregable

Pronóstico con baseline estacional, backtesting por horizonte, intervalos y traducción del error a inventario.

## Autoría

Material elaborado por el profesor Sergio Gevatschnaider.
