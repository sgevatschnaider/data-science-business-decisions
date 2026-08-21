# Módulo 03: Outliers, robustez e influencia

Separar errores, rarezas válidas y observaciones influyentes con criterios estadísticos y de negocio.

## Pregunta de decisión

¿Una observación extrema es un error, un evento valioso o una señal de que el proceso cambió?

## Índice interactivo

| Recurso | Acceso |
|---|---|
| Guía principal | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/03-outliers/index.html) |
| Diapositivas 01 · Diagnóstico, robustez y tratamiento | [Abrir](https://docs.google.com/presentation/d/15nnL4qm_aKb3G2-G0xbna0MiUtl05-9Ic3NIHF0FwKk/view?usp=sharing) |
| Diapositivas 02 · Métodos de detección con ML | [Abrir](https://docs.google.com/presentation/d/1I-jQOc8mkt1WVhGZffWr6p9EWAYg13SBjryxTvYUAtc/view?usp=sharing) |
| Simulación interactiva | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/03-outliers/simulacion.html) |
| Colab 01 · Fundamentos y sensibilidad | [Abrir](https://colab.research.google.com/github/sgevatschnaider/data-science-business-decisions/blob/main/notebooks/03-outliers.ipynb) |
| Colab 02 · Detectores con Machine Learning | [Abrir](https://colab.research.google.com/drive/13FwdNX2jd5lMrgNjNR0wEQJEtwlynfO8) |
| Colab 03 · Distribuciones y Hotel Booking | [Abrir](https://colab.research.google.com/drive/1BJU3zTYvxerrVwQDhyz3%76%32ZU113cp3Dp?usp=sharing) |
| Colab 04 · Atlas interactivo de outliers | [Abrir](https://colab.research.google.com/drive/1C9k3F2sWIGx8ORQRN6HCB0V70z-r_Bia?usp=sharing) |
| Cuestionario | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/03-outliers/cuestionario.html) |
| Glosario | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/03-outliers/glosario.html) |
| Simulación 01 · IQR, Z-score y MAD | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/03-outliers/sim-01-iqr-z-mad.html) |
| Simulación 02 · Influencia en regresión | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/03-outliers/sim-02-influencia-regresion.html) |
| Simulación 03 · Outlier multivariado | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/03-outliers/sim-03-multivariado.html) |
| Simulación 04 · Isolation Forest | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/03-outliers/sim-04-isolation-forest.html) |
| Simulación 05 · LOF y One-Class SVM | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/03-outliers/sim-05-lof-ocsvm.html) |
| Simulación 06 · Model Arena y costos | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/03-outliers/sim-06-model-arena.html) |

## Resultados de aprendizaje

- Definir rareza respecto de una distribución, relación, segmento o tiempo.
- Comparar IQR, Z-score, MAD y criterios multivariados sin automatizar la eliminación.
- Diferenciar residuo, leverage, influencia y anomalía respecto del modelo.
- Seleccionar y evaluar detectores con ML según geometría, densidad, escala y objetivo.
- Calibrar thresholds y justificar conservar, corregir, transformar, segmentar o excluir.

## Caso de negocio

En reservas hoteleras, un lead time muy alto puede ser error, grupo legítimo o señal temprana de cancelación. El equipo debe contrastar distribución, segmento e impacto predictivo antes de intervenir.

## Profundización aplicada

- Distancia de Mahalanobis robusta, leverage, Cook y sensibilidad de parámetros.
- Rareza global, local y contextual por segmento, tiempo, canal o régimen.
- Outlier detection frente a novelty detection y datos de referencia limpios.
- Isolation Forest, LOF, One-Class SVM, Elliptic Envelope, DBSCAN y PCA.
- Calibración de thresholds por etiquetas, capacidad, contaminación y costo.

## Errores frecuentes

- Eliminar automáticamente todo punto marcado por una regla estadística.
- Usar puntuación z en distribuciones muy asimétricas sin contraste robusto.
- Ajustar escala, modelo o threshold con información del conjunto de test.
- Comparar detectores con orientaciones de score o tasas de alerta diferentes.
- Evaluar influencia sin contrastar conclusiones con y sin el caso.

## Desafío de transferencia

Construí un protocolo que separe error, evento raro válido, segmento especial, observación influyente y cambio de régimen; luego definí una acción y un responsable para cada clase.

## Secuencia de práctica

1. Verificar unidades, reglas, duplicados, temporalidad y procedencia.
2. Comparar IQR, Z-score y MAD bajo distintas formas de distribución.
3. Medir residuo, leverage, Cook y cambios del modelo con y sin el caso.
4. Detectar rarezas multivariadas después de escalar y segmentar.
5. Contrastar Isolation Forest, LOF y One-Class SVM con una referencia común.
6. Calibrar el threshold y registrar tratamiento, impacto, límite y responsable.

## Entregable

Informe de diagnóstico con bitácora de casos, comparación de detectores, threshold justificado, análisis de sensibilidad y recomendación de tratamiento.

## Autoría

Material elaborado por el profesor Sergio Gevatschnaider.
