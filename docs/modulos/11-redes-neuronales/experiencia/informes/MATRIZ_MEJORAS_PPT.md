# Matriz de mejoras de PowerPoint

Los originales son 28 y 13 diapositivas. Los nuevos decks contienen 51 y 34. La correspondencia es por desarrollo temático, no una afirmación de reutilización mecánica de cada objeto.

## Redes neuronales: fundamentos y decisiones

| Original | Título original | Diagnóstico y mejora | Nueva(s) |
|---|---|---|---|
| 01 | Redes neuronales: de los datos a la decisión | Conservar propósito y rediseñar apertura. | 01 |
| 02 | La pregunta de negocio | Ampliar decisión, restricciones, utilidad y criterios para elegir complejidad. | 02, 05 |
| 03 | Objetivos de aprendizaje | Convertir objetivos en evidencia observable. | 03 |
| 04 | Recorrido de 150 minutos | Señalizar 28 slides esenciales y distribuir 150 minutos con laboratorios. | 04 |
| 05 | Antes de una red: el baseline | Explicitar equivalencia funcional de neurona sigmoide y logística. | 06 |
| 06 | Una neurona no “piensa”: calcula | Precisar sesgo, escala y diferencia entre peso e importancia causal. | 07 |
| 07 | Ejemplo numérico de inferencia | Conservar el cálculo correcto y conectarlo con probabilidad modelada. | 08 |
| 08 | Fronteras de decisión: límites del perceptrón | Agregar XOR canónico, frontera vectorial y construcción con dos ReLU. | 09, 10 |
| 09 | Las capas construyen representaciones | Agregar dimensiones, conteo de 13 parámetros y capacidad de representación. | 11, 12 |
| 10 | Por qué importan las activaciones | Incluir fórmulas y derivadas, saturación y caso no derivable. | 13, 14 |
| 11 | ¿Qué función de activación elegir? | Distinguir tareas binarias, multiclase, multietiqueta y regresión. | 15, 16 |
| 12 | Forward propagation: información que avanza | Separar forward de actualización de parámetros. | 18 |
| 13 | Qué mide la función de pérdida | Desarrollar BCE estable y MSE con unidades. | 19, 20 |
| 14 | Aprender = reducir una pérdida | Agregar inicialización, estabilidad y comprobaciones numéricas. | 28 |
| 15 | El gradiente indica sensibilidad | Derivar actualización y condición de estabilidad de una parábola. | 24, 26, 29 |
| 16 | Backpropagation y regla de la cadena | Completar cadena, gradientes numéricos, capa oculta y diferencias finitas. | 21, 22, 23, 25 |
| 17 | Mini-batches, épocas e iteraciones | Contar lotes y actualizaciones por época. | 27 |
| 18 | Sobreajuste: memorizar no es generalizar | Separar curvas de generalización y checkpoint elegido. | 33, 36 |
| 19 | Regularización y decisiones de diseño | Desarrollar L2, decay y dropout con sus límites. | 34, 35 |
| 20 | Datos que representan el futuro | Precisar disponibilidad temporal y ajuste de transformaciones solo con train. | 31, 32 |
| 21 | Accuracy puede engañar | Agregar matriz de confusión, ROC/PR, AP y calibración. | 37, 38, 39, 40 |
| 22 | El umbral es una decisión económica | Corregir costo de todos los contactos y distinguir riesgo de efecto causal. | 42, 43, 45 |
| 23 | Caso aplicado: retención de clientes | Comparación medida en notebook, con igual protocolo y política congelada. | 41, 44 |
| 24 | RNN, LSTM, CNN y Transformers: mapa | Mapa de arquitecturas sin un ranking universal. | 47 |
| 25 | Riesgos: precisión no basta | Vincular explicación, equidad y trazabilidad con decisiones de operación. | 46 |
| 26 | Laboratorio integrado | Reemplazar pregunta repetitiva por tareas, predicciones y respuestas específicas. | 17, 30, 49 |
| 27 | Actividad: defender una arquitectura | Agregar defensa y rúbrica formativa. | 48 |
| 28 | Videos y materiales para continuar | Videos con metadatos corroborados y enlaces contextuales. | 50, 51 |
## Secuencias, RNN y LSTM

| Original | Título original | Diagnóstico y mejora | Nueva(s) |
|---|---|---|---|
| 01 | RNN y LSTM: cómo modelar secuencias | Abrir una ampliación independiente de la clase principal. | 01 |
| 02 | Tabular vs secuencial | Construir ventanas y formas de entrada/salida. | 02, 04 |
| 03 | RNN: estado oculto recurrente | Agregar dimensiones y convención de conteo de parámetros. | 05, 07 |
| 04 | Una RNN desplegada en el tiempo | Desplegar recurrencia y calcular estados escalares. | 06, 08 |
| 05 | Vanishing y exploding gradients | Desarrollar BPTT, Jacobianos, ejemplos de contracción/expansión y clipping. | 09, 10, 11, 12, 13, 23 |
| 06 | LSTM: memoria y puertas | Completar las seis ecuaciones LSTM y su parametrización. | 14, 17, 19, 25 |
| 07 | ¿Qué controla cada compuerta? | Desarrollar cada gate y distinguir memoria interna de estado expuesto. | 15, 16, 18 |
| 08 | Simulación: retener o sobrescribir | Cálculo numérico de c/h y modelo de gates constantes claramente delimitado. | 20, 21, 22, 24 |
| 09 | Cuándo considerar una LSTM | Comparar condiciones de uso y costo con baselines y datos concretos. | 27, 28, 29, 30, 31, 32, 33 |
| 10 | RNN vs LSTM vs Transformer | Agregar GRU, convenciones y costos de atención/recurrencia sin superioridad universal. | 26, 27, 28 |
| 11 | Diseño correcto del experimento temporal | Precisar orígenes, ventanas, partición cronológica y walk-forward. | 03, 29, 30 |
| 12 | Actividad aplicada: demanda semanal | Agregar baseline estacional, MAE/RMSE/MAPE y LSTM CPU reproducible. | 31, 32, 33 |
| 13 | Cierre: arquitectura sigue al problema | Cerrar con ejercicios resueltos y criterios de adopción. | 34 |
