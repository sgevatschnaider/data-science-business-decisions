# Módulo 11: Redes neuronales y arquitecturas modernas

Comprender neuronas, activaciones, backpropagation y regularización, con un mapa responsable de arquitecturas actuales.

## Pregunta de decisión

¿Cuándo la capacidad de aprender representaciones justifica mayor complejidad, datos y costo computacional?

## Experiencia principal · UCA 5/11/2026

- [Portada integrada](../../docs/modulos/11-redes-neuronales/experiencia/index.html)
- [Fundamentos: 51 diapositivas, ruta esencial de 28](../../docs/modulos/11-redes-neuronales/experiencia/ppt-1-fundamentos/reader.html)
- [RNN/LSTM: 34 diapositivas](../../docs/modulos/11-redes-neuronales/experiencia/ppt-2-rnn-lstm/reader.html)
- [Laboratorios de fundamentos](../../docs/modulos/11-redes-neuronales/experiencia/ppt-1-fundamentos/lab.html) y [memoria LSTM](../../docs/modulos/11-redes-neuronales/experiencia/ppt-2-rnn-lstm/lab.html)
- [Videos](../../docs/modulos/11-redes-neuronales/experiencia/ppt-1-fundamentos/videos.html) y [guía docente](../../docs/modulos/11-redes-neuronales/experiencia/ppt-1-fundamentos/guide.html)
- [Notebook reproducible](../../notebooks/11-redes-neuronales.ipynb)
- PPTX editables y PDF sincronizados: `experiencia/ppt-*/downloads/`.

El programa conserva **Módulo 12** como número visible. `11-redes-neuronales` sigue siendo el identificador de carpeta. La clase principal dura 150 minutos y RNN/LSTM queda como ampliación.

Se preservan [cuestionario](../../docs/modulos/11-redes-neuronales/cuestionario.html), [glosario](../../docs/modulos/11-redes-neuronales/glosario.html), [NLP](../../docs/modulos/11-redes-neuronales/nlp-lab.html), [Transformer](../../docs/modulos/11-redes-neuronales/transformer-lab.html) y sus preguntas/glosarios. `simulacion.html` es un índice de compatibilidad con los cinco laboratorios nuevos.

Los ejemplos y experimentos son sintéticos. La utilidad de churn es un proxy con efectividad supuesta, no retención incremental medida. Ver los informes dentro de `experiencia/informes/`.

## Resultados de aprendizaje

- Explicar neurona, capa, activación, pérdida y gradiente.
- Relacionar capacidad, sobreajuste y regularización.
- Experimentar con fronteras no lineales en TensorFlow Playground.
- Distinguir CNN, RNN/LSTM/GRU, Transformers y autoencoders.

## Caso de negocio

Un centro de atención quiere clasificar mensajes y resumir motivos. Debe comparar una referencia simple con modelos complejos y evaluar errores.

## Profundización aplicada

- Embeddings, recuperación aumentada, evaluación de RAG y trazabilidad de fuentes.
- Structured outputs, herramientas y agentes con límites, permisos y observabilidad.
- Agencia responsable: separar recomendación, aprobación y ejecución, con criterios de detención y reversión.
- Evaluación de IA generativa: veracidad, utilidad, seguridad, costo y latencia.

## Errores frecuentes

- Elegir una red profunda sin superar un baseline simple.
- Evaluar texto generado solo con ejemplos favorables o impresión subjetiva.
- Confundir atención con explicación causal o razonamiento humano.

## Desafío de transferencia

Diseñá un asistente documental que cite evidencia, se abstenga cuando corresponda y sea evaluable antes de publicarse.

## Secuencia de práctica

1. Construir una neurona y observar su frontera.
2. Comparar activaciones y cantidad de capas.
3. Registrar pérdida de entrenamiento y validación.
4. Documentar por qué una arquitectura es adecuada al tipo de dato.

## Entregable

Experimento controlado de arquitectura y regularización, comparación con baseline, curva de aprendizaje y ficha de riesgos.

## Autoría

Material elaborado por el profesor Sergio Gevatschnaider.

## Recursos complementarios

- [TensorFlow Playground](https://playground.tensorflow.org/)
- [Preguntas Transformer](../../docs/modulos/11-redes-neuronales/transformer-preguntas.html)
- [Glosario Transformer](../../docs/modulos/11-redes-neuronales/transformer-glosario.html)
