# Módulo 07 · Series de Tiempo y Forecasting

De la descomposición clásica al forecasting moderno y al Machine Learning temporal, con una regla metodológica transversal: **cada predicción se construye únicamente con información disponible en su origen de pronóstico**.

## Pregunta de decisión

¿Qué parte del futuro es predecible, con qué incertidumbre y con qué costo de error para la decisión de negocio?

## Recorrido principal

| Recurso | Acceso |
|---|---|
| Portal completo del módulo | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/07-series-tiempo/index.html) |
| Presentación 01 · Descomposición clásica | [Visor](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/07-series-tiempo/presentacion-01.html) · [Google Slides](https://docs.google.com/presentation/d/1NCfywwD7gu7h5V9fUN-P-sMdGi8uf2MPEtwA3oG4qZE/edit) |
| Presentación 02 · Tratamiento moderno | [Visor](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/07-series-tiempo/presentacion-02.html) · [Google Slides](https://docs.google.com/presentation/d/1sD37WdHpdv5n3zDzjrxlVB7Q-SRy0sGRj0XYxgxNgZo/edit) |
| Presentación 03 · Machine Learning temporal | [Visor](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/07-series-tiempo/presentacion-03.html) · [Google Slides](https://docs.google.com/presentation/d/1KsD2iQkIN_VoITKPN1oPI3JTk3elxotThVuic11yhm0/edit) |
| Laboratorio · 5 simulaciones | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/07-series-tiempo/simulacion.html) |
| Cuestionario avanzado | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/07-series-tiempo/cuestionario.html) |
| Glosario de estudio | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/07-series-tiempo/glosario.html) |
| Notebook en Colab | [Abrir](https://colab.research.google.com/github/sgevatschnaider/data-science-business-decisions/blob/main/notebooks/07-series-tiempo.ipynb) |

Los visores de las tres presentaciones incluyen autoplay configurable, acceso a pantalla completa y exportación de la versión vigente de Google Slides a PDF y PPTX. Los permisos de esos archivos siguen siendo los definidos en Google Drive.

## Secuencia didáctica

1. **Estructura y descomposición clásica.** Frecuencia, tendencia, ciclo, estacionalidad, irregularidad, modelos aditivo/multiplicativo, promedios móviles, índices estacionales y reconstrucción del pronóstico.
2. **Tratamiento moderno.** Transformaciones, estacionariedad, autocorrelación, diferenciación, suavizado y diagnóstico temporal; comparación de enfoques y residuos.
3. **Machine Learning temporal.** Reformulación supervisada, lags y ventanas, variables de calendario, validación walk-forward, múltiples horizontes y comparación contra baselines.
4. **Simulación.** Cinco laboratorios conceptuales para modificar parámetros y observar cómo cambian señal, fuga de información y error fuera de muestra.
5. **Estudio y evaluación.** Cuestionario con explicación de respuestas y glosario filtrable.

## Resultados de aprendizaje

- Distinguir tendencia, estacionalidad, ciclo, irregularidad y cambio de régimen.
- Elegir entre representaciones aditivas y multiplicativas y justificar transformaciones.
- Construir lags, ventanas y variables de calendario sin *future leakage*.
- Usar baselines ingenuos y estacionales antes de justificar complejidad adicional.
- Diseñar backtesting de origen rodante con horizonte, gap y ventana de entrenamiento explícitos.
- Comparar modelos clásicos y de Machine Learning con métricas coherentes con la decisión.
- Interpretar incertidumbre, intervalos y degradación del error a medida que aumenta el horizonte.

## Regla de oro

Una variable es válida para predecir el instante `t+h` solo si puede calcularse con información disponible en el origen `t`. Una media centrada, un escalador ajustado con toda la serie o una selección de hiperparámetros que mira el futuro contaminan la evaluación.

## Caso de negocio

Un comercio necesita pronosticar demanda para decidir inventario. Subestimar produce quiebres y pérdida de ventas; sobreestimar inmoviliza capital. El objetivo no es solo reducir MAE o RMSE: es elegir un procedimiento de forecasting que funcione en los mismos horizontes y condiciones en que se tomará la decisión.

## Publicación estable

El sitio avanzado se conserva en `modules/07-series-tiempo/site/`. Durante CI, `scripts/build_course.py` genera el curso general y `scripts/publish_module07.py` publica después esta versión completa en `docs/modulos/07-series-tiempo/`, evitando que un build futuro restaure la versión básica.

## Autoría

Material elaborado por el profesor Sergio Gevatschnaider.
