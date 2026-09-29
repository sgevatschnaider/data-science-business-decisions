# Módulo 09: Árboles, Random Forest y ensembles

Aprender reglas no lineales, controlar complejidad y combinar modelos para mejorar estabilidad y desempeño.

## Pregunta de decisión

¿Qué reglas e interacciones segmentan el problema y cuánto mejora la decisión al combinar múltiples modelos?

## Índice interactivo

| Recurso | Acceso |
|---|---|
| Guía principal | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/09-arboles-ensembles/index.html) |
| Simulación interactiva | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/09-arboles-ensembles/simulacion.html) |
| Cuestionario | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/09-arboles-ensembles/cuestionario.html) |
| Glosario | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/09-arboles-ensembles/glosario.html) |
| Notebook en Colab | [Abrir](https://colab.research.google.com/github/sgevatschnaider/data-science-business-decisions/blob/main/notebooks/09-arboles-ensembles.ipynb) |

## Resultados de aprendizaje

- Interpretar particiones, impureza, hojas y profundidad.
- Controlar sobreajuste mediante poda y restricciones.
- Explicar bagging, Random Forest y boosting.
- Evaluar importancia con métodos que respeten validación.

## Caso de negocio

Una aseguradora necesita priorizar siniestros para revisión. Requiere desempeño, reglas comunicables y control de falsos positivos.

## Profundización aplicada

- Gradient boosting moderno, early stopping y regularización.
- Importancia por permutación, PDP/ICE y límites con variables correlacionadas.
- Optimización de hiperparámetros con presupuesto y validación anidada.

## Errores frecuentes

- Comparar modelos sin el mismo protocolo de validación.
- Interpretar importancia interna como causalidad.
- Aumentar profundidad y árboles sin medir latencia ni estabilidad.

## Desafío de transferencia

Compará árbol, bosque y boosting por valor, estabilidad, latencia y capacidad de explicación.

## Secuencia de práctica

1. Visualizar un árbol pequeño y traducir hojas a reglas.
2. Explorar profundidad y tamaño mínimo de hoja.
3. Comparar árbol, bosque y boosting bajo los mismos folds.
4. Calcular permutation importance fuera de muestra.

## Entregable

Comparación entre árbol podado, Random Forest y boosting, con curvas de aprendizaje, métricas y explicación validada.

## Autoría

Material elaborado por el profesor Sergio Gevatschnaider.

## Presentaciones completas

- [PPT 01: Árboles y CART, 41 diapositivas](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/09-arboles-ensembles/presentacion-01.html)
- [PPT 02: Bagging y Random Forest, 36 diapositivas](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/09-arboles-ensembles/presentacion-02.html)
- [PPT 03: Boosting, interpretación y decisión, 35 diapositivas](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/09-arboles-ensembles/presentacion-03.html)

Los visores permiten autoplay, pantalla completa y descargas. La fuente se conserva en `modules/09-arboles-ensembles/site/` y este paso la publica después del generador general.

## Laboratorio de 16 simulaciones

[Abrir el catálogo completo](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/09-arboles-ensembles/simulacion.html)

| Simulación | Acceso |
|---|---|
| Simulador 01 · Split óptimo e impureza Gini | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/09-arboles-ensembles/simuladores/simulador_01_split_gini.html) |
| Simulador 02 · Gini vs. Entropía | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/09-arboles-ensembles/simuladores/simulador_02_gini_entropia.html) |
| Simulador 03 · Árbol ↔ particiones 2D | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/09-arboles-ensembles/simuladores/simulador_03_arbol_particiones_2d.html) |
| Simulador 04 · Profundidad y overfitting | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/09-arboles-ensembles/simuladores/simulador_04_profundidad_overfitting.html) |
| Simulador 05 · Poda costo-complejidad | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/09-arboles-ensembles/simuladores/simulador_05_poda_ccp_alpha.html) |
| Simulador 06 · Inestabilidad de un árbol | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/09-arboles-ensembles/simuladores/simulador_06_inestabilidad_arbol.html) |
| Simulador 07 · Bootstrap y Out-of-Bag | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/09-arboles-ensembles/simuladores/simulador_07_bootstrap_oob.html) |
| Simulador 08 · Bagging | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/09-arboles-ensembles/simuladores/simulador_08_bagging.html) |
| Simulador 09 · Bagging vs. Random Forest | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/09-arboles-ensembles/simuladores/simulador_09_random_forest.html) |
| Simulador 10 · Número de árboles y error OOB | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/09-arboles-ensembles/simuladores/simulador_10_numero_arboles_oob.html) |
| Simulador 11 · max_features y correlación | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/09-arboles-ensembles/simuladores/simulador_11_max_features_correlacion.html) |
| Simulador 12 · MDI vs. permutation importance | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/09-arboles-ensembles/simuladores/simulador_12_feature_importance.html) |
| Simulador 13 · Variables correlacionadas | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/09-arboles-ensembles/simuladores/simulador_13_variables_correlacionadas.html) |
| Simulador 14 · PDP e ICE | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/09-arboles-ensembles/simuladores/simulador_14_pdp_ice.html) |
| Simulador 15 · Gradient Boosting | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/09-arboles-ensembles/simuladores/simulador_15_boosting.html) |
| Simulador 16 · Decision Lab: modelo, threshold y costos | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/09-arboles-ensembles/simuladores/simulador_16_decision_lab.html) |
