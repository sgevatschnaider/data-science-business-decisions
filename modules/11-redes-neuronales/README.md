# Módulo 11: Redes neuronales y arquitecturas modernas

Comprender neuronas, memoria recurrente, activaciones, backpropagation y regularización, con un mapa responsable de arquitecturas actuales.

## Pregunta de decisión

¿Cuándo la capacidad de aprender representaciones y contexto temporal justifica mayor complejidad, datos y costo computacional?

## Índice interactivo

| Recurso | Acceso |
|---|---|
| Guía principal | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/11-redes-neuronales/index.html) |
| Simulación RNN paso a paso | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/11-redes-neuronales/simulacion.html) |
| Cuestionario | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/11-redes-neuronales/cuestionario.html) |
| Glosario | [Abrir](https://sgevatschnaider.github.io/data-science-business-decisions/modulos/11-redes-neuronales/glosario.html) |
| Notebook en Colab | [Abrir](https://colab.research.google.com/github/sgevatschnaider/data-science-business-decisions/blob/main/notebooks/11-redes-neuronales.ipynb) |
| TensorFlow Playground | [Abrir](https://playground.tensorflow.org/) |

## Resultados de aprendizaje

- Explicar neurona, capa, activación, pérdida y gradiente.
- Desplegar una RNN en el tiempo y explicar cómo actualiza su estado oculto.
- Relacionar recurrencia, saturación, vanishing gradient y exploding gradient.
- Relacionar capacidad, sobreajuste y regularización.
- Distinguir CNN, RNN/LSTM/GRU, Transformers y autoencoders.

## Caso de negocio

Un centro de atención quiere clasificar secuencias de mensajes y detectar si la urgencia aumenta. El orden de los eventos importa: una palabra o una señal debe interpretarse según lo ocurrido antes.

## Secuencia de práctica

1. Recorrer una secuencia y calcular el estado oculto paso a paso.
2. Separar la contribución de la entrada actual y la memoria recurrente.
3. Comparar tanh, sigmoide y ReLU bajo distintos pesos.
4. Diagnosticar memoria corta, persistencia, oscilación y saturación.
5. Relacionar los límites de la RNN simple con la motivación de LSTM y GRU.

## Entregable

Experimento controlado que documente una secuencia, parámetros recurrentes, evolución del estado oculto, diagnóstico de estabilidad, comparación con un baseline y límites del modelo.

## Autoría

Material elaborado por el profesor Sergio Gevatschnaider.
