# Módulo 06 · Validación, selección y generalización

> **Pregunta de decisión:** ¿el desempeño observado representa casos futuros o es una consecuencia del azar, el sobreajuste, el leakage o una partición incorrecta?

Este módulo convierte la validación de modelos en un **laboratorio docente completo**: teoría, presentación, 14 simulaciones, notebook reproducible, cuestionario desarrollado y glosario de referencia.

## Accesos directos

| Recurso | Acceso | Propósito |
|---|---|---|
| Portal del módulo | [Abrir GitHub Pages](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/06-validacion-modelos/index.html) | Punto de entrada único |
| Presentación 01 · Clase conceptual | [Abrir visor](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/06-validacion-modelos/presentacion.html) | 14 slides, autoplay, fullscreen, teclado y PDF |
| Presentación 02 · Guía de simulaciones | [Abrir visor](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/06-validacion-modelos/presentacion-simulaciones.html) | 23 láminas, autoplay, velocidad, vista general, fullscreen, teclado y PDF |
| PPTX descargable | [Descargar](../../docs/modulos/06-validacion-modelos/Modulo_06_Guia_de_las_14_Simulaciones.pptx) | 23 láminas: teoría, uso, controles y glosario de los 14 laboratorios |
| Google Slides | [Abrir](https://docs.google.com/presentation/d/1-kgUluIRzdMO6SJa_MX2vQd_N01J_dmB10Zei4SgdPE/edit?usp=drivesdk) | Versión nativa del PPT |
| PDF | [Generar / guardar](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/06-validacion-modelos/presentacion.html?print=1) | Vista de impresión para guardar como PDF |
| 14 laboratorios | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/06-validacion-modelos/simulaciones/index.html) | Intuición visual y experimentación |
| Cuestionario | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/06-validacion-modelos/cuestionario.html) | 10 preguntas desarrolladas |
| Glosario | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/06-validacion-modelos/glosario.html) | 90 términos y flashcards |
| Notebook Colab | [Abrir](https://colab.research.google.com/github/sgevatschnaider/data-science-business-decisions/blob/main/notebooks/06-validacion-modelos.ipynb) | Implementación reproducible |

## Resultados de aprendizaje

Al finalizar el módulo el estudiante debería poder:

1. distinguir **train, validation y test** por su función metodológica;
2. explicar por qué el training score no estima generalización;
3. comparar hold-out con K-Fold y justificar cuándo conviene cada uno;
4. elegir K y discutir el compromiso entre sesgo, varianza y costo;
5. seleccionar `KFold`, `StratifiedKFold`, `GroupKFold` o `TimeSeriesSplit` según la estructura del dato;
6. detectar **data leakage** y encapsular preprocessing + modelo en un `Pipeline`;
7. reportar media, dispersión y estabilidad entre folds;
8. usar Repeated CV, tuning y **Nested CV** sin reutilizar información de evaluación;
9. generar predicciones **out-of-fold (OOF)** y realizar una evaluación final reservada;
10. traducir el score técnico a riesgo, umbral y decisión de negocio.

## Ruta didáctica

**Ver → experimentar → programar → explicar → decidir**

1. **Presentación 01:** construye la intuición conceptual.
2. **Presentación 02:** explica la teoría, los controles y la lectura de cada simulación.
3. **Laboratorios 01–04:** generalización y mecánica de CV.
4. **Laboratorios 05–07:** splitters que respetan clases, grupos y tiempo.
5. **Laboratorios 08–10:** leakage, overfitting y estabilidad.
6. **Laboratorios 11–12:** tuning y Nested CV.
7. **Laboratorios 13–14:** métricas y decisión empresarial.
8. **Notebook Colab:** reproduce los conceptos con scikit-learn.
9. **Cuestionario + glosario:** consolida explicación y vocabulario.

## Los 14 laboratorios

| # | Laboratorio | Concepto central |
|---|---|---|
| 01 | [Train · Validation · Test](../../docs/modulos/06-validacion-modelos/simulaciones/01_train_validation_test.html) | Por qué train, validation y test cumplen funciones distintas. |
| 02 | [Hold-out vs. K-Fold](../../docs/modulos/06-validacion-modelos/simulaciones/02_holdout_vs_kfold.html) | Sensibilidad a una única partición frente a una distribución de scores. |
| 03 | [K-Fold Visual Laboratory](../../docs/modulos/06-validacion-modelos/simulaciones/03_kfold_visual.html) | Rotación de folds, score por iteración y promedio acumulado. |
| 04 | [¿Cuántos folds elegir?](../../docs/modulos/06-validacion-modelos/simulaciones/04_numero_de_folds.html) | Compromiso entre sesgo, varianza, tamaño de muestra y costo. |
| 05 | [Stratified K-Fold](../../docs/modulos/06-validacion-modelos/simulaciones/05_stratified_kfold.html) | Preservación de clases cuando el target está desbalanceado. |
| 06 | [GroupKFold y leakage por identidad](../../docs/modulos/06-validacion-modelos/simulaciones/06_group_kfold.html) | Separar entidades completas: clientes, pacientes, empresas. |
| 07 | [TimeSeriesSplit](../../docs/modulos/06-validacion-modelos/simulaciones/07_time_series_split.html) | Validar futuro con pasado, incluyendo horizonte y gap temporal. |
| 08 | [Data Leakage Laboratory](../../docs/modulos/06-validacion-modelos/simulaciones/08_data_leakage.html) | Cómo una transformación fuera del fold infla artificialmente el score. |
| 09 | [Overfitting y Cross-Validation](../../docs/modulos/06-validacion-modelos/simulaciones/09_overfitting_cv.html) | Brecha train-CV y complejidad como señales de sobreajuste. |
| 10 | [Repeated K-Fold](../../docs/modulos/06-validacion-modelos/simulaciones/10_repeated_kfold.html) | Distribuciones de desempeño para estudiar estabilidad e incertidumbre. |
| 11 | [CV + Hyperparameter Tuning](../../docs/modulos/06-validacion-modelos/simulaciones/11_hyperparameter_tuning.html) | Búsqueda de hiperparámetros sin elegir por rendimiento de train. |
| 12 | [Nested Cross-Validation](../../docs/modulos/06-validacion-modelos/simulaciones/12_nested_cv.html) | Separar tuning interno de estimación externa de generalización. |
| 13 | [Métricas y estabilidad entre folds](../../docs/modulos/06-validacion-modelos/simulaciones/13_metricas_cv.html) | La métrica correcta depende del error que cuesta en el negocio. |
| 14 | [Cross-Validation Business Lab](../../docs/modulos/06-validacion-modelos/simulaciones/14_business_lab.html) | Integrar split, métrica, estabilidad y umbral operativo. |

## Regla de oro

> **El split correcto es el que reproduce la forma en que el modelo encontrará datos nuevos en producción.**

Eso significa que la unidad de separación puede ser una fila, una clase, un cliente, un paciente, una empresa, una geografía o un período temporal. El diseño de validación es parte del problema estadístico y del problema de negocio.

## Protocolo de auditoría

- Definir unidad de observación y unidad de generalización.
- Construir un baseline antes de optimizar.
- Reservar test final cuando corresponda.
- Ajustar toda transformación aprendida **dentro** de los folds.
- Reportar media y dispersión de métricas.
- Revisar estabilidad por fold y segmentos relevantes.
- Separar tuning de evaluación con Nested CV si es necesario.
- Traducir el resultado a una decisión operativa explícita.

## Entregable esperado

Un protocolo de validación justificado que incluya: unidad de generalización, splitter, baseline, pipeline, tabla de métricas por fold, estabilidad, selección de hiperparámetros, evaluación final reservada y lectura de negocio.

## Autoría

Material elaborado por **Sergio Gevatschnaider** para *Data Science for Business Decisions*.
