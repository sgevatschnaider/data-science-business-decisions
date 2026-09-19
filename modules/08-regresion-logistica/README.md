# Módulo 08 · Regresión Logística y Decisiones de Clasificación

De la función sigmoide a la interpretación, la validación, la decisión basada en costos, la extensión multiclase y el monitoreo en producción.

## Pregunta de decisión

**¿Qué probabilidad estimamos, qué acción tomamos y a qué costo?**

La regresión logística produce probabilidades. La decisión operativa requiere además un umbral, una función de valor/costo, restricciones de capacidad y una evaluación fuera de muestra.

## Recorrido principal

| Recurso | Acceso |
|---|---|
| Portal completo | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/08-regresion-logistica/index.html) |
| Presentación 01 · Fundamentos de clasificación | [Visor](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/08-regresion-logistica/presentacion-01.html) |
| Presentación 02 · Interpretación, validación y decisiones | [Visor](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/08-regresion-logistica/presentacion-02.html) |
| Laboratorio · 14 simulaciones | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/08-regresion-logistica/simulacion.html) |
| Guía completa de simulaciones | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/08-regresion-logistica/guia.html) |
| Cuestionario avanzado · 30 preguntas | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/08-regresion-logistica/cuestionario.html) |
| Glosario avanzado | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/08-regresion-logistica/glosario.html) |
| Notebook en Colab | [Abrir](https://colab.research.google.com/github/sgevatschnaider/data-science-business-decisions/blob/main/notebooks/08-regresion-logistica.ipynb) |

## Simuladores originales completos

Los siguientes archivos se publican **sin resumir, recomponer ni simplificar**. Son los HTML originales provistos para el módulo.

| Nº | Simulador original |
|---:|---|
| 01 | [Función sigmoide](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/08-regresion-logistica/simuladores/simulador_01_funcion_sigmoide_regresion_logistica.html) |
| 02 | [Probabilidad, Odds, Logit y Odds Ratio](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/08-regresion-logistica/simuladores/simulador_02_probabilidad_odds_logit_odds_ratio.html) |
| 03 | [Efectos marginales](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/08-regresion-logistica/simuladores/simulador_03_efectos_marginales_regresion_logistica.html) |
| 04 | [Log-Loss y Máxima Verosimilitud](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/08-regresion-logistica/simuladores/simulador_04_log_loss_maxima_verosimilitud.html) |
| 05 | [Threshold, Matriz de Confusión y Métricas](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/08-regresion-logistica/simuladores/simulador_05_threshold_matriz_confusion_metricas.html) |
| 06 | [ROC, Precision–Recall y Desbalance](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/08-regresion-logistica/simuladores/simulador_06_roc_precision_recall_desbalance.html) |
| 07 | [Frontera de Decisión 2D](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/08-regresion-logistica/simuladores/simulador_07_frontera_decision_2d_regresion_logistica.html) |
| 08 | [Regularización L1/L2 y Overfitting](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/08-regresion-logistica/simuladores/simulador_08_regularizacion_l1_l2_overfitting.html) |
| 09 | [Dummies, Interacciones y No Linealidades](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/08-regresion-logistica/simuladores/simulador_09_dummies_interacciones_no_linealidades.html) |
| 10 | [Train, Validation, Test y K-Fold](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/08-regresion-logistica/simuladores/simulador_10_train_validation_test_kfold_cross_validation.html) |
| 11 | [Calibración vs Discriminación](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/08-regresion-logistica/simuladores/simulador_11_calibracion_vs_discriminacion.html) |
| 12 | [Decision Lab — Credit Scoring, Threshold y Costos](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/08-regresion-logistica/simuladores/simulador_12_decision_lab_credit_scoring_costos.html) |
| 13 | [Softmax y Clasificación Multiclase](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/08-regresion-logistica/simuladores/simulador_13_softmax_clasificacion_multiclase.html) |
| 14 | [Model Drift & Monitoring](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/08-regresion-logistica/simuladores/simulador_14_model_drift_monitoring.html) |

El glosario y el cuestionario también se publican desde los HTML originales completos.

## Ruta didáctica

1. **Fundamentos probabilísticos (Sim 01–04):** score, sigmoide, odds/logit, efectos marginales, likelihood y log-loss.
2. **De probabilidad a clasificación (Sim 05–07):** threshold, matriz de confusión, ROC/PR y frontera de decisión.
3. **Generalización y diseño (Sim 08–10):** regularización, especificación, train/validation/test y K-fold.
4. **Probabilidades útiles para decidir (Sim 11–12):** discriminación, calibración, costos y política de decisión.
5. **Extensión multiclase (Sim 13):** softmax, competencia entre clases y temperatura.
6. **Ciclo de vida en producción (Sim 14):** drift, PSI, desempeño, calibración y monitoreo.

## Resultados de aprendizaje

- Derivar e interpretar la relación entre score lineal, sigmoide, probabilidad, odds y logit.
- Interpretar coeficientes y odds ratios sin tratarlos como cambios lineales en probabilidad.
- Comprender máxima verosimilitud y log-loss.
- Separar discriminación, calibración y decisión.
- Evaluar con train/validation/test o validación cruzada sin contaminar el test.
- Analizar ROC-AUC y Precision–Recall bajo desbalance.
- Seleccionar thresholds en función de costos, capacidad y objetivo.
- Entender regularización L1/L2, especificación e interacciones.
- Extender a softmax/multiclase.
- Monitorear drift y degradación en producción.

## Regla de oro

**Probabilidad estimada no equivale a decisión.** Entrenamiento, evaluación de probabilidades y elección de política deben separarse. Un buen ranking puede estar mal calibrado y un threshold útil depende del contexto económico y operativo.

## Publicación estable

El sitio avanzado vive en `modules/08-regresion-logistica/site/`. El pipeline genera primero el curso general y luego `scripts/publish_module08.py` repone este sitio canónico en `docs/modulos/08-regresion-logistica/`, evitando que un build futuro restaure la versión básica.

## Autoría

Material elaborado por el profesor Sergio Gevatschnaider.
