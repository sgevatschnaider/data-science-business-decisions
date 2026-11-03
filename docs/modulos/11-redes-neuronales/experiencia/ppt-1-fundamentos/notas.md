# Notas del expositor



## 01 · Redes neuronales

Abrir con la decisión de retención: disponemos de datos previos, un presupuesto de contacto y un resultado futuro. Una red aprende una función a partir de ejemplos. El éxito de entrenamiento será una parte de la evidencia, no el criterio final de adopción. La clase principal usa las 28 diapositivas esenciales, con pausas para laboratorio. RNN y LSTM quedan en el segundo deck.

Pregunta: ¿Qué debería mejorar una red para justificar su uso?
Respuesta orientativa: La decisión fuera de muestra, considerando costos, estabilidad y comparación con un baseline.



## 02 · La decisión de retención

Fijar una fecha de corte para cada fila. Las variables deben estar disponibles en esa fecha. Definir abandono operativo y una ventana futura observable. Un score de riesgo ayuda a priorizar, pero no prueba que la oferta evite el abandono. Registrar quién decide y cuál es la capacidad de contacto.

Pregunta: ¿Una cancelación ya confirmada puede ser una variable predictora?
Respuesta orientativa: No, si la decisión debía tomarse antes de esa confirmación: introduce información del resultado.



## 03 · Resultados de aprendizaje

Solicitar una explicación verbal de cada símbolo. Al final, cada grupo deberá mostrar el cálculo de una actualización, identificar una fuga de información y justificar un umbral bajo restricciones. La precisión verbal importa: backpropagation calcula derivadas y el optimizador actualiza parámetros.

Pregunta: ¿Qué evidencia distinguiría comprensión de repetición de fórmulas?
Respuesta orientativa: Poder anticipar el signo de una actualización y explicar cuándo una mejora predictiva no cambia una decisión.



## 04 · Ruta de clase: 9:30 a 12:00

Usar el filtro Ruta esencial del visor. Reservar 12 minutos para el laboratorio de perceptrón, 10 para gradiente y 13 para umbral. La guía distribuye 150 minutos sin agregar una segunda exposición completa de RNN/LSTM. Las slides de ampliación sirven para consultas y trabajo posterior.

Pregunta: ¿Qué pregunta conecta los tres bloques?
Respuesta orientativa: Cómo pasar de una función aprendida a una decisión confiable.



## 05 · Cuándo conviene una solución simple

No existe un tamaño mínimo universal para deep learning. Importan señal, dimensionalidad, preentrenamiento y costo del error. Una regresión logística o un árbol con atributos apropiados puede ser suficiente. Comparar modelos con el mismo protocolo y recursos de ajuste, evitando elegir arquitectura por moda.

Pregunta: ¿Más datos garantizan que una red supere a un árbol?
Respuesta orientativa: No. Hay que medir desempeño, costos y estabilidad en el problema concreto.



## 06 · Regresión logística como baseline

La neurona sigmoide sin capas ocultas comparte la forma funcional de la regresión logística binaria. Esto no vuelve idénticos los algoritmos de ajuste, regularización o calibración usados por todas las implementaciones. Un cambio de umbral desplaza la frontera, pero no la convierte en no lineal respecto de x.

Pregunta: ¿Qué agrega una capa oculta a esta función?
Respuesta orientativa: Transformaciones de atributos que pueden construir fronteras no lineales.

Desarrollo conceptual: Una neurona lineal divide el espacio con un hiperplano. Agregar capas con activaciones permite construir nuevas coordenadas: la separación puede ser sencilla en esas coordenadas aunque sea imposible en las entradas originales.
Para XOR se construyen h₁=ReLU(x₁+x₂), h₂=ReLU(x₁+x₂−1). La salida h₁−2h₂ vale exactamente 0, 1, 1, 0 sobre las cuatro entradas binarias. Es una demostración de capacidad con pesos fijados, no una trayectoria de entrenamiento.
Ejemplo: (0,0) se transforma en (0,0), las entradas (0,1) y (1,0) coinciden en (1,0), y (1,1) llega a (2,1). En el espacio oculto, h₁−2h₂=0,5 separa las clases. La coincidencia de dos entradas de la misma clase es esperable.
Error frecuente: Agregar capas afines sin activación mantiene una función afín. Más épocas de un perceptrón tampoco resuelven la imposibilidad geométrica de XOR.



## 07 · Entradas, pesos, sesgo y activación

Los pesos representan sensibilidad condicionada al resto de la función y a la escala de las variables. No equivalen automáticamente a importancia causal. El sesgo permite desplazar la frontera sin modificar la orientación. Distinguir el parámetro entrenable de un hiperparámetro como learning rate.

Pregunta: ¿Cambiar la unidad de x cambia la interpretación de w?
Respuesta orientativa: Sí. Por eso escalar variables y documentar unidades es parte del pipeline.

Desarrollo conceptual: Una neurona lineal divide el espacio con un hiperplano. Agregar capas con activaciones permite construir nuevas coordenadas: la separación puede ser sencilla en esas coordenadas aunque sea imposible en las entradas originales.
Para XOR se construyen h₁=ReLU(x₁+x₂), h₂=ReLU(x₁+x₂−1). La salida h₁−2h₂ vale exactamente 0, 1, 1, 0 sobre las cuatro entradas binarias. Es una demostración de capacidad con pesos fijados, no una trayectoria de entrenamiento.
Ejemplo: (0,0) se transforma en (0,0), las entradas (0,1) y (1,0) coinciden en (1,0), y (1,1) llega a (2,1). En el espacio oculto, h₁−2h₂=0,5 separa las clases. La coincidencia de dos entradas de la misma clase es esperable.
Error frecuente: Agregar capas afines sin activación mantiene una función afín. Más épocas de un perceptrón tampoco resuelven la imposibilidad geométrica de XOR.



## 08 · Inferencia: un cálculo verificable

Todas las cifras de este ejemplo son didácticas. Resolver primero la suma y luego la activación. Una salida 0,622459 pertenece al modelo y no constituye por sí sola una frecuencia observada ni una garantía individual. En inferencia se mantienen los pesos fijos.

Pregunta: ¿Qué ocurre si b baja a −0,6?
Respuesta orientativa: z pasa a 0 y p a 0,5. Con la convención p≥0,5 sigue prediciendo clase 1.

Desarrollo conceptual: Una neurona lineal divide el espacio con un hiperplano. Agregar capas con activaciones permite construir nuevas coordenadas: la separación puede ser sencilla en esas coordenadas aunque sea imposible en las entradas originales.
Para XOR se construyen h₁=ReLU(x₁+x₂), h₂=ReLU(x₁+x₂−1). La salida h₁−2h₂ vale exactamente 0, 1, 1, 0 sobre las cuatro entradas binarias. Es una demostración de capacidad con pesos fijados, no una trayectoria de entrenamiento.
Ejemplo: (0,0) se transforma en (0,0), las entradas (0,1) y (1,0) coinciden en (1,0), y (1,1) llega a (2,1). En el espacio oculto, h₁−2h₂=0,5 separa las clases. La coincidencia de dos entradas de la misma clase es esperable.
Error frecuente: Agregar capas afines sin activación mantiene una función afín. Más épocas de un perceptrón tampoco resuelven la imposibilidad geométrica de XOR.



## 09 · Una frontera lineal

El perceptrón usa una salida umbral, no una probabilidad. La actualización se aplica sobre errores y también incluye b ← b+η(y−ŷ). La garantía clásica de convergencia requiere separabilidad y un conjunto finito con entradas acotadas. No trasladar esa garantía a XOR.

Pregunta: ¿Qué cambia el sesgo?
Respuesta orientativa: La posición de la frontera. Los pesos determinan su orientación.

Desarrollo conceptual: Una neurona lineal divide el espacio con un hiperplano. Agregar capas con activaciones permite construir nuevas coordenadas: la separación puede ser sencilla en esas coordenadas aunque sea imposible en las entradas originales.
Para XOR se construyen h₁=ReLU(x₁+x₂), h₂=ReLU(x₁+x₂−1). La salida h₁−2h₂ vale exactamente 0, 1, 1, 0 sobre las cuatro entradas binarias. Es una demostración de capacidad con pesos fijados, no una trayectoria de entrenamiento.
Ejemplo: (0,0) se transforma en (0,0), las entradas (0,1) y (1,0) coinciden en (1,0), y (1,1) llega a (2,1). En el espacio oculto, h₁−2h₂=0,5 separa las clases. La coincidencia de dos entradas de la misma clase es esperable.
Error frecuente: Agregar capas afines sin activación mantiene una función afín. Más épocas de un perceptrón tampoco resuelven la imposibilidad geométrica de XOR.



## 10 · XOR exige una representación distinta

El laboratorio usa los cuatro puntos canónicos para que la limitación sea inequívoca. La falta de convergencia de una neurona no implica un error del software. Dibujar la envolvente de cada clase ayuda a ver la imposibilidad de separarlas linealmente. Un modelo con atributos diseñados a mano también podría resolver XOR.

Pregunta: ¿Basta con entrenar más épocas un perceptrón?
Respuesta orientativa: No. La clase de funciones del modelo no contiene una solución perfecta para XOR.

Desarrollo conceptual: Una neurona lineal divide el espacio con un hiperplano. Agregar capas con activaciones permite construir nuevas coordenadas: la separación puede ser sencilla en esas coordenadas aunque sea imposible en las entradas originales.
Para XOR se construyen h₁=ReLU(x₁+x₂), h₂=ReLU(x₁+x₂−1). La salida h₁−2h₂ vale exactamente 0, 1, 1, 0 sobre las cuatro entradas binarias. Es una demostración de capacidad con pesos fijados, no una trayectoria de entrenamiento.
Ejemplo: (0,0) se transforma en (0,0), las entradas (0,1) y (1,0) coinciden en (1,0), y (1,1) llega a (2,1). En el espacio oculto, h₁−2h₂=0,5 separa las clases. La coincidencia de dos entradas de la misma clase es esperable.
Error frecuente: Agregar capas afines sin activación mantiene una función afín. Más épocas de un perceptrón tampoco resuelven la imposibilidad geométrica de XOR.



## 11 · XOR con dos unidades ReLU

Para entradas binarias: suma 0 produce salida 0, suma 1 produce 1, suma 2 produce 0. Es una construcción de capacidad, no una trayectoria de entrenamiento ni una salida probabilística. Los pesos podrían aprenderse, pero la existencia de una solución no asegura que todo optimizador la encuentre.

Pregunta: ¿Cuánto vale la salida para (1,1)?
Respuesta orientativa: h₁=2, h₂=1 y salida=0.

Desarrollo conceptual: Una neurona lineal divide el espacio con un hiperplano. Agregar capas con activaciones permite construir nuevas coordenadas: la separación puede ser sencilla en esas coordenadas aunque sea imposible en las entradas originales.
Para XOR se construyen h₁=ReLU(x₁+x₂), h₂=ReLU(x₁+x₂−1). La salida h₁−2h₂ vale exactamente 0, 1, 1, 0 sobre las cuatro entradas binarias. Es una demostración de capacidad con pesos fijados, no una trayectoria de entrenamiento.
Ejemplo: (0,0) se transforma en (0,0), las entradas (0,1) y (1,0) coinciden en (1,0), y (1,1) llega a (2,1). En el espacio oculto, h₁−2h₂=0,5 separa las clases. La coincidencia de dos entradas de la misma clase es esperable.
Error frecuente: Agregar capas afines sin activación mantiene una función afín. Más épocas de un perceptrón tampoco resuelven la imposibilidad geométrica de XOR.



## 12 · Dimensiones y parámetros de un MLP

Usar vectores columna para mantener coherencia. h=φ(W₁x+b₁) tiene dimensión 3 y la salida tiene dimensión 1. No contar las activaciones como parámetros. Si un framework usa matrices transpuestas o dos vectores de sesgo, su representación puede cambiar sin invalidar esta convención.

Pregunta: ¿Cuántos parámetros tiene una capa d→m con sesgo?
Respuesta orientativa: m·d+m. La salida siguiente agrega sus propios pesos y sesgos.

Desarrollo conceptual: Una neurona lineal divide el espacio con un hiperplano. Agregar capas con activaciones permite construir nuevas coordenadas: la separación puede ser sencilla en esas coordenadas aunque sea imposible en las entradas originales.
Para XOR se construyen h₁=ReLU(x₁+x₂), h₂=ReLU(x₁+x₂−1). La salida h₁−2h₂ vale exactamente 0, 1, 1, 0 sobre las cuatro entradas binarias. Es una demostración de capacidad con pesos fijados, no una trayectoria de entrenamiento.
Ejemplo: (0,0) se transforma en (0,0), las entradas (0,1) y (1,0) coinciden en (1,0), y (1,1) llega a (2,1). En el espacio oculto, h₁−2h₂=0,5 separa las clases. La coincidencia de dos entradas de la misma clase es esperable.
Error frecuente: Agregar capas afines sin activación mantiene una función afín. Más épocas de un perceptrón tampoco resuelven la imposibilidad geométrica de XOR.



## 13 · La no linealidad cambia la capacidad

A=W₂W₁ y c=W₂b₁+b₂. Llamamos afín a la transformación con sesgo. La simplificación demuestra por qué una red de muchas capas afines sigue teniendo frontera lineal si la salida es logística. La capacidad adicional necesita activaciones o mecanismos no lineales.

Pregunta: ¿Qué ocurre si todas las capas ocultas usan identidad?
Respuesta orientativa: La composición sigue siendo afín.

Desarrollo conceptual: Una neurona lineal divide el espacio con un hiperplano. Agregar capas con activaciones permite construir nuevas coordenadas: la separación puede ser sencilla en esas coordenadas aunque sea imposible en las entradas originales.
Para XOR se construyen h₁=ReLU(x₁+x₂), h₂=ReLU(x₁+x₂−1). La salida h₁−2h₂ vale exactamente 0, 1, 1, 0 sobre las cuatro entradas binarias. Es una demostración de capacidad con pesos fijados, no una trayectoria de entrenamiento.
Ejemplo: (0,0) se transforma en (0,0), las entradas (0,1) y (1,0) coinciden en (1,0), y (1,1) llega a (2,1). En el espacio oculto, h₁−2h₂=0,5 separa las clases. La coincidencia de dos entradas de la misma clase es esperable.
Error frecuente: Agregar capas afines sin activación mantiene una función afín. Más épocas de un perceptrón tampoco resuelven la imposibilidad geométrica de XOR.



## 14 · Sigmoide: salida acotada y saturación

Una sigmoide permite parametrizar una probabilidad binaria, pero el valor requiere validación de calibración. Su uso repetido en capas profundas puede atenuar gradientes. El límite máximo 0,25 se verifica completando el cuadrado p(1−p)=0,25−(p−0,5)².

Pregunta: ¿Cuál es la derivada en z=0?
Respuesta orientativa: 0,25.

Desarrollo conceptual: La activación determina qué señal entrega una unidad. Su derivada determina cuánto cambia esa señal ante un pequeño cambio de entrada. Una salida cercana a uno puede tener sensibilidad casi nula.
Sigmoide y tanh saturan en los extremos. ReLU conserva pendiente uno para entradas positivas y cero para negativas. El punto cero no tiene derivada única. Las salidas deben elegirse junto con la tarea y su pérdida.
Ejemplo: En z=0, la sigmoide vale 0,5 y su derivada 0,25. En z=5, vale aproximadamente 0,9933 y su derivada 0,00665. El laboratorio separa ambas curvas y dibuja la tangente en la activación.
Error frecuente: Una derivada sigmoide pequeña no implica por sí sola que todo gradiente de salida con BCE sea pequeño: al derivar BCE respecto del logit aparece p−y. En capas ocultas hay otros productos de derivadas.



## 15 · ReLU, tanh y Leaky ReLU

ReLU no es derivable en cero. Los motores adoptan una convención, frecuentemente cero, y el laboratorio lo informa. Una unidad que permanece en el lado negativo puede no recibir gradiente. Leaky ReLU reduce esa situación, sin garantizar mejor desempeño en todos los casos. Comparar valores y derivadas en el laboratorio.

Pregunta: ¿Una activación con salida grande tiene siempre derivada grande?
Respuesta orientativa: No. tanh puede aproximarse a 1 mientras su derivada se aproxima a 0.

Desarrollo conceptual: La activación determina qué señal entrega una unidad. Su derivada determina cuánto cambia esa señal ante un pequeño cambio de entrada. Una salida cercana a uno puede tener sensibilidad casi nula.
Sigmoide y tanh saturan en los extremos. ReLU conserva pendiente uno para entradas positivas y cero para negativas. El punto cero no tiene derivada única. Las salidas deben elegirse junto con la tarea y su pérdida.
Ejemplo: En z=0, la sigmoide vale 0,5 y su derivada 0,25. En z=5, vale aproximadamente 0,9933 y su derivada 0,00665. El laboratorio separa ambas curvas y dibuja la tangente en la activación.
Error frecuente: Una derivada sigmoide pequeña no implica por sí sola que todo gradiente de salida con BCE sea pequeño: al derivar BCE respecto del logit aparece p−y. En capas ocultas hay otros productos de derivadas.



## 16 · Salida según el objetivo

Restar el máximo evita desbordes sin cambiar el cociente. Softmax corresponde a clases mutuamente excluyentes y sus probabilidades suman uno. Para etiquetas múltiples simultáneas suelen usarse sigmoides independientes. La identidad permite regresión sin acotar el rango de salida.

Pregunta: ¿Dos etiquetas que pueden coexistir requieren softmax?
Respuesta orientativa: No necesariamente. Sigmoides por etiqueta modelan un problema multietiqueta.

Desarrollo conceptual: La activación determina qué señal entrega una unidad. Su derivada determina cuánto cambia esa señal ante un pequeño cambio de entrada. Una salida cercana a uno puede tener sensibilidad casi nula.
Sigmoide y tanh saturan en los extremos. ReLU conserva pendiente uno para entradas positivas y cero para negativas. El punto cero no tiene derivada única. Las salidas deben elegirse junto con la tarea y su pérdida.
Ejemplo: En z=0, la sigmoide vale 0,5 y su derivada 0,25. En z=5, vale aproximadamente 0,9933 y su derivada 0,00665. El laboratorio separa ambas curvas y dibuja la tangente en la activación.
Error frecuente: Una derivada sigmoide pequeña no implica por sí sola que todo gradiente de salida con BCE sea pequeño: al derivar BCE respecto del logit aparece p−y. En capas ocultas hay otros productos de derivadas.



## 17 · Laboratorio de activaciones

Antes de iniciar la simulación automática, pedir una predicción sobre las derivadas. El recorrido cambia z realmente y recalcula la función seleccionada. Pausar cerca de cero y comparar tanh, ReLU y sigmoide. Las unidades de z y la activación son adimensionales en este ejemplo.

Pregunta: ¿Qué se pierde al observar solo la curva de activación?
Respuesta orientativa: La sensibilidad local que participa en backpropagation.

Desarrollo conceptual: La activación determina qué señal entrega una unidad. Su derivada determina cuánto cambia esa señal ante un pequeño cambio de entrada. Una salida cercana a uno puede tener sensibilidad casi nula.
Sigmoide y tanh saturan en los extremos. ReLU conserva pendiente uno para entradas positivas y cero para negativas. El punto cero no tiene derivada única. Las salidas deben elegirse junto con la tarea y su pérdida.
Ejemplo: En z=0, la sigmoide vale 0,5 y su derivada 0,25. En z=5, vale aproximadamente 0,9933 y su derivada 0,00665. El laboratorio separa ambas curvas y dibuja la tangente en la activación.
Error frecuente: Una derivada sigmoide pequeña no implica por sí sola que todo gradiente de salida con BCE sea pequeño: al derivar BCE respecto del logit aparece p−y. En capas ocultas hay otros productos de derivadas.



## 18 · Forward propagation

Distinguir el grafo de cálculo de la arquitectura dibujada. Cada nodo conserva lo necesario para derivar luego. El forward es el mismo tipo de evaluación en entrenamiento e inferencia, pero capas como dropout cambian de modo. Señalar explícitamente el modo de evaluación al implementar.

Pregunta: ¿El forward cambia los pesos?
Respuesta orientativa: No. El paso del optimizador realiza la actualización.

Desarrollo conceptual: Predecir, medir error, derivar y actualizar son operaciones diferentes. Ver sus valores sobre un mismo ejemplo ayuda a entender qué aporta backpropagation y qué decide el optimizador.
Con una neurona sigmoide y BCE, el gradiente del logit es p−y. El peso multiplica ese gradiente por la entrada. El sesgo recibe la misma señal sin multiplicarla por x. El optimizador resta η veces cada gradiente; después hay que realizar un nuevo forward.
Ejemplo: Con x=2, y=1, w=0,3 y b=−0,1: z=0,5, p=0,622459, L=0,474077. Los gradientes son −0,755081 y −0,377541. Con η=0,1 se obtiene w=0,375508, b=−0,062246 y una nueva BCE de 0,406926.
Error frecuente: Backpropagation no actualiza los pesos por sí mismo. Un gradiente negativo tampoco es un error: indica que aumentar ese parámetro reduce localmente la pérdida.



## 19 · BCE para clasificación binaria

La BCE deriva de la verosimilitud Bernoulli bajo las hipótesis del modelo. Una probabilidad de 0 para un evento observado genera pérdida infinita en teoría. Para cálculo estable usar logits con logaddexp o BCEWithLogitsLoss. No confundir esta pérdida con accuracy ni beneficio de una campaña.

Pregunta: ¿Qué pérdida tiene un acierto con probabilidad 0,5?
Respuesta orientativa: −ln(0,5)=0,693147, cualquiera sea la etiqueta binaria observada.

Desarrollo conceptual: Predecir, medir error, derivar y actualizar son operaciones diferentes. Ver sus valores sobre un mismo ejemplo ayuda a entender qué aporta backpropagation y qué decide el optimizador.
Con una neurona sigmoide y BCE, el gradiente del logit es p−y. El peso multiplica ese gradiente por la entrada. El sesgo recibe la misma señal sin multiplicarla por x. El optimizador resta η veces cada gradiente; después hay que realizar un nuevo forward.
Ejemplo: Con x=2, y=1, w=0,3 y b=−0,1: z=0,5, p=0,622459, L=0,474077. Los gradientes son −0,755081 y −0,377541. Con η=0,1 se obtiene w=0,375508, b=−0,062246 y una nueva BCE de 0,406926.
Error frecuente: Backpropagation no actualiza los pesos por sí mismo. Un gradiente negativo tampoco es un error: indica que aumentar ese parámetro reduce localmente la pérdida.



## 20 · MSE para regresión

MSE resulta natural con errores Gaussianos de varianza constante si se interpreta por máxima verosimilitud. No es la única elección y puede resultar sensible a atípicos. En el ejemplo, si y mide unidades vendidas, MSE mide unidades². La BCE se elige por el objetivo binario del caso churn.

Pregunta: ¿Cambiar la unidad monetaria altera MSE?
Respuesta orientativa: Sí. Multiplicar y por k multiplica MSE por k².

Desarrollo conceptual: Predecir, medir error, derivar y actualizar son operaciones diferentes. Ver sus valores sobre un mismo ejemplo ayuda a entender qué aporta backpropagation y qué decide el optimizador.
Con una neurona sigmoide y BCE, el gradiente del logit es p−y. El peso multiplica ese gradiente por la entrada. El sesgo recibe la misma señal sin multiplicarla por x. El optimizador resta η veces cada gradiente; después hay que realizar un nuevo forward.
Ejemplo: Con x=2, y=1, w=0,3 y b=−0,1: z=0,5, p=0,622459, L=0,474077. Los gradientes son −0,755081 y −0,377541. Con η=0,1 se obtiene w=0,375508, b=−0,062246 y una nueva BCE de 0,406926.
Error frecuente: Backpropagation no actualiza los pesos por sí mismo. Un gradiente negativo tampoco es un error: indica que aumentar ese parámetro reduce localmente la pérdida.



## 21 · El grafo de una neurona logística

Elegimos una sola entrada para que toda la derivación pueda verificarse a mano. La secuencia es z=wx+b, p=σ(z), L=−ln(p). El código de pruebas usa diferencias finitas para comprobar las derivadas. No mezclar estos x y w con el ejemplo previo de dos variables.

Pregunta: ¿Qué valores deben guardarse para la derivación?
Respuesta orientativa: x, y, p y los parámetros del forward. Para este caso no es necesario reconstruir toda la pérdida.

Desarrollo conceptual: Predecir, medir error, derivar y actualizar son operaciones diferentes. Ver sus valores sobre un mismo ejemplo ayuda a entender qué aporta backpropagation y qué decide el optimizador.
Con una neurona sigmoide y BCE, el gradiente del logit es p−y. El peso multiplica ese gradiente por la entrada. El sesgo recibe la misma señal sin multiplicarla por x. El optimizador resta η veces cada gradiente; después hay que realizar un nuevo forward.
Ejemplo: Con x=2, y=1, w=0,3 y b=−0,1: z=0,5, p=0,622459, L=0,474077. Los gradientes son −0,755081 y −0,377541. Con η=0,1 se obtiene w=0,375508, b=−0,062246 y una nueva BCE de 0,406926.
Error frecuente: Backpropagation no actualiza los pesos por sí mismo. Un gradiente negativo tampoco es un error: indica que aumentar ese parámetro reduce localmente la pérdida.



## 22 · Regla de la cadena

Con BCE y sigmoide, ∂L/∂p=(p−y)/(p(1−p)), ∂p/∂z=p(1−p), ∂z/∂w=x. La cancelación algebraica conduce a (p−y)x. Las derivadas corresponden a un ejemplo sin regularización. Para un batch se promedian según la reducción de la pérdida.

Pregunta: ¿Por qué se suman gradientes cuando un parámetro tiene varios caminos?
Respuesta orientativa: Porque la pérdida depende del parámetro por todos esos caminos, según la regla de derivación total.

Desarrollo conceptual: Predecir, medir error, derivar y actualizar son operaciones diferentes. Ver sus valores sobre un mismo ejemplo ayuda a entender qué aporta backpropagation y qué decide el optimizador.
Con una neurona sigmoide y BCE, el gradiente del logit es p−y. El peso multiplica ese gradiente por la entrada. El sesgo recibe la misma señal sin multiplicarla por x. El optimizador resta η veces cada gradiente; después hay que realizar un nuevo forward.
Ejemplo: Con x=2, y=1, w=0,3 y b=−0,1: z=0,5, p=0,622459, L=0,474077. Los gradientes son −0,755081 y −0,377541. Con η=0,1 se obtiene w=0,375508, b=−0,062246 y una nueva BCE de 0,406926.
Error frecuente: Backpropagation no actualiza los pesos por sí mismo. Un gradiente negativo tampoco es un error: indica que aumentar ese parámetro reduce localmente la pérdida.



## 23 · Backpropagation: resultado numérico

Un gradiente negativo indica que aumentar el parámetro reduce la pérdida localmente. Los valores se calcularon con precisión completa antes de redondear. Backpropagation termina en estas derivadas: aún no se actualizaron los pesos. Una comprobación numérica central usa ε=10⁻⁵.

Pregunta: ¿Por qué el gradiente de w duplica al de b?
Respuesta orientativa: Porque x=2 y ∂z/∂w=x, mientras ∂z/∂b=1.

Desarrollo conceptual: Predecir, medir error, derivar y actualizar son operaciones diferentes. Ver sus valores sobre un mismo ejemplo ayuda a entender qué aporta backpropagation y qué decide el optimizador.
Con una neurona sigmoide y BCE, el gradiente del logit es p−y. El peso multiplica ese gradiente por la entrada. El sesgo recibe la misma señal sin multiplicarla por x. El optimizador resta η veces cada gradiente; después hay que realizar un nuevo forward.
Ejemplo: Con x=2, y=1, w=0,3 y b=−0,1: z=0,5, p=0,622459, L=0,474077. Los gradientes son −0,755081 y −0,377541. Con η=0,1 se obtiene w=0,375508, b=−0,062246 y una nueva BCE de 0,406926.
Error frecuente: Backpropagation no actualiza los pesos por sí mismo. Un gradiente negativo tampoco es un error: indica que aumentar ese parámetro reduce localmente la pérdida.



## 24 · Una actualización de descenso

El nuevo logit es 0,688770 y la pérdida exacta se verifica por código. La mejora en este ejemplo y con este paso no prueba convergencia global ni mejora de validación. Repetir con una tasa distinta permite distinguir cálculo de gradientes y elección del tamaño de paso.

Pregunta: ¿En qué dirección se movieron ambos parámetros?
Respuesta orientativa: Aumentaron porque sus gradientes eran negativos.

Desarrollo conceptual: Predecir, medir error, derivar y actualizar son operaciones diferentes. Ver sus valores sobre un mismo ejemplo ayuda a entender qué aporta backpropagation y qué decide el optimizador.
Con una neurona sigmoide y BCE, el gradiente del logit es p−y. El peso multiplica ese gradiente por la entrada. El sesgo recibe la misma señal sin multiplicarla por x. El optimizador resta η veces cada gradiente; después hay que realizar un nuevo forward.
Ejemplo: Con x=2, y=1, w=0,3 y b=−0,1: z=0,5, p=0,622459, L=0,474077. Los gradientes son −0,755081 y −0,377541. Con η=0,1 se obtiene w=0,375508, b=−0,062246 y una nueva BCE de 0,406926.
Error frecuente: Backpropagation no actualiza los pesos por sí mismo. Un gradiente negativo tampoco es un error: indica que aumentar ese parámetro reduce localmente la pérdida.



## 25 · Backpropagation en una capa oculta

Para salida binaria escalar con BCE y sigmoide, δ₂ es escalar. δ₁ tiene tantas componentes como unidades ocultas. Las dimensiones verifican el cálculo: δ₁xᵀ es m×d. El símbolo ⊙ denota producto componente a componente. Los sesgos reciben δ y los batches agregan sus gradientes.

Pregunta: ¿Qué dimensión tiene el gradiente de W₁?
Respuesta orientativa: La misma que W₁: m×d.

Desarrollo conceptual: Predecir, medir error, derivar y actualizar son operaciones diferentes. Ver sus valores sobre un mismo ejemplo ayuda a entender qué aporta backpropagation y qué decide el optimizador.
Con una neurona sigmoide y BCE, el gradiente del logit es p−y. El peso multiplica ese gradiente por la entrada. El sesgo recibe la misma señal sin multiplicarla por x. El optimizador resta η veces cada gradiente; después hay que realizar un nuevo forward.
Ejemplo: Con x=2, y=1, w=0,3 y b=−0,1: z=0,5, p=0,622459, L=0,474077. Los gradientes son −0,755081 y −0,377541. Con η=0,1 se obtiene w=0,375508, b=−0,062246 y una nueva BCE de 0,406926.
Error frecuente: Backpropagation no actualiza los pesos por sí mismo. Un gradiente negativo tampoco es un error: indica que aumentar ese parámetro reduce localmente la pérdida.



## 26 · Learning rate y estabilidad

Para esta parábola, la convergencia exige 0<η<2. η=2 oscila sin contraer y η>2 diverge. El laboratorio ofrece además BCE logística. La condición de esta parábola no se traslada como constante universal a todas las redes: depende de la curvatura de la función.

Pregunta: ¿Qué sucede con η=1 en esta parábola?
Respuesta orientativa: Llega al mínimo w=2 en un paso, usando el gradiente exacto.

Desarrollo conceptual: El gradiente señala la dirección local de mayor aumento. Su opuesto permite bajar, pero un paso demasiado grande puede cruzar repetidamente el mínimo y alejarse de él.
Para L(w)=½(w−2)², el error respecto del mínimo se multiplica por 1−η. Se contrae si |1−η|<1. La condición cambia con la curvatura: para una cuadrática multivariable depende del mayor autovalor del Hessiano.
Ejemplo: Con w₀=−0,5, η=0,2 avanza despacio, η=1,4 oscila con amplitud decreciente y η=2,2 amplifica el error. El laboratorio relaciona la posición sobre la parábola con la pérdida registrada por iteración.
Error frecuente: El límite η<2 corresponde a esta parábola de curvatura uno, no a todas las redes. La logística de una neurona es convexa; una red multicapa suele producir un problema no convexo.



## 27 · Mini-batch, iteración y época

El conteo supone que se usan todos los ejemplos exactamente una vez por época. Si n no es divisible por el batch, aparece un último lote menor o una política drop_last. En datos temporales hay que distinguir barajar ventanas de entrenamiento de filtrar futuro a una ventana.

Pregunta: ¿Cinco épocas equivalen a cinco actualizaciones?
Respuesta orientativa: Solo en entrenamiento full-batch. En este ejemplo son 50 actualizaciones.

Desarrollo conceptual: El gradiente señala la dirección local de mayor aumento. Su opuesto permite bajar, pero un paso demasiado grande puede cruzar repetidamente el mínimo y alejarse de él.
Para L(w)=½(w−2)², el error respecto del mínimo se multiplica por 1−η. Se contrae si |1−η|<1. La condición cambia con la curvatura: para una cuadrática multivariable depende del mayor autovalor del Hessiano.
Ejemplo: Con w₀=−0,5, η=0,2 avanza despacio, η=1,4 oscila con amplitud decreciente y η=2,2 amplifica el error. El laboratorio relaciona la posición sobre la parábola con la pérdida registrada por iteración.
Error frecuente: El límite η<2 corresponde a esta parábola de curvatura uno, no a todas las redes. La logística de una neurona es convexa; una red multicapa suele producir un problema no convexo.



## 28 · Inicialización y escalado

Inicializar todos los pesos ocultos iguales puede mantener neuronas idénticas durante el entrenamiento. He propone una escala para rectificadores bajo supuestos sobre las entradas y la propagación. No basta para garantizar estabilidad. Estandarizar atributos puede ayudar, siempre ajustando media y escala solo en train.

Pregunta: ¿Por qué no estimar el escalado con todo el dataset?
Respuesta orientativa: Porque usaría información de validación o test para construir el modelo.

Desarrollo conceptual: El gradiente señala la dirección local de mayor aumento. Su opuesto permite bajar, pero un paso demasiado grande puede cruzar repetidamente el mínimo y alejarse de él.
Para L(w)=½(w−2)², el error respecto del mínimo se multiplica por 1−η. Se contrae si |1−η|<1. La condición cambia con la curvatura: para una cuadrática multivariable depende del mayor autovalor del Hessiano.
Ejemplo: Con w₀=−0,5, η=0,2 avanza despacio, η=1,4 oscila con amplitud decreciente y η=2,2 amplifica el error. El laboratorio relaciona la posición sobre la parábola con la pérdida registrada por iteración.
Error frecuente: El límite η<2 corresponde a esta parábola de curvatura uno, no a todas las redes. La logística de una neurona es convexa; una red multicapa suele producir un problema no convexo.



## 29 · Gradientes que se atenúan o explotan

La norma del producto depende de matrices y activaciones, no solo del número de capas. Clipping limita magnitudes de gradientes explosivos, pero no recupera automáticamente gradientes pequeños. El segundo deck desarrolla la misma dificultad a través del tiempo y la memoria controlada de LSTM.

Pregunta: ¿Clipping resuelve un gradiente casi nulo?
Respuesta orientativa: No. Solo limita gradientes cuya norma excede el umbral.

Desarrollo conceptual: El gradiente señala la dirección local de mayor aumento. Su opuesto permite bajar, pero un paso demasiado grande puede cruzar repetidamente el mínimo y alejarse de él.
Para L(w)=½(w−2)², el error respecto del mínimo se multiplica por 1−η. Se contrae si |1−η|<1. La condición cambia con la curvatura: para una cuadrática multivariable depende del mayor autovalor del Hessiano.
Ejemplo: Con w₀=−0,5, η=0,2 avanza despacio, η=1,4 oscila con amplitud decreciente y η=2,2 amplifica el error. El laboratorio relaciona la posición sobre la parábola con la pérdida registrada por iteración.
Error frecuente: El límite η<2 corresponde a esta parábola de curvatura uno, no a todas las redes. La logística de una neurona es convexa; una red multicapa suele producir un problema no convexo.



## 30 · Laboratorio de optimización

Cada paso calcula gradientes de verdad. Pausar y contrastar números con la regla de actualización. Modificar w, b o η reinicia una trayectoria documentada para no mezclar experimentos. Exportar CSV permite comparar pérdidas por iteración sin atribuir esos valores a una campaña real.

Pregunta: ¿Cómo verificarías una derivada implementada?
Respuesta orientativa: Con diferencias finitas, tolerancia numérica y casos extremos.

Desarrollo conceptual: El gradiente señala la dirección local de mayor aumento. Su opuesto permite bajar, pero un paso demasiado grande puede cruzar repetidamente el mínimo y alejarse de él.
Para L(w)=½(w−2)², el error respecto del mínimo se multiplica por 1−η. Se contrae si |1−η|<1. La condición cambia con la curvatura: para una cuadrática multivariable depende del mayor autovalor del Hessiano.
Ejemplo: Con w₀=−0,5, η=0,2 avanza despacio, η=1,4 oscila con amplitud decreciente y η=2,2 amplifica el error. El laboratorio relaciona la posición sobre la parábola con la pérdida registrada por iteración.
Error frecuente: El límite η<2 corresponde a esta parábola de curvatura uno, no a todas las redes. La logística de una neurona es convexa; una red multicapa suele producir un problema no convexo.



## 31 · Train, validación y test

La separación debe representar el uso real. Agrupar por cliente o respetar el tiempo si hay observaciones repetidas. Mirar test repetidamente para elegir hiperparámetros lo convierte de hecho en validación. Una separación correcta no elimina drift ni garantiza que el próximo período replique el pasado.

Pregunta: ¿Dónde elegimos el umbral de retención?
Respuesta orientativa: En validación, antes de evaluar una única política congelada en test.

Desarrollo conceptual: Un modelo más flexible puede reducir el error de entrenamiento y empeorar en datos que no usó para ajustar sus parámetros. La figura debe mostrar tanto la función ajustada como el error fuera de entrenamiento.
El nuevo laboratorio ajusta polinomios en una base de Chebyshev sobre puntos sintéticos con semilla fija. El grado controla capacidad y λ penaliza coeficientes sin penalizar el intercepto. Las curvas de error se calculan con los datos de ese mismo experimento.
Ejemplo: Comparar grados 1, 3 y 9 con 12 puntos de entrenamiento. Observar la forma ajustada y los MSE de train y validación. Repetir con 32 puntos, más ruido o λ>0. Los valores se calculan, no son curvas prefabricadas.
Error frecuente: Usar validación para seleccionar grado y después presentarla como un test final sesga la evaluación. Un único ejemplo sintético tampoco demuestra que regularizar siempre mejore.



## 32 · Fuga de información en churn

Pedir a cada grupo una tabla con nombre de variable, momento de disponibilidad y transformación. Una promoción futura solo puede usarse si se conocía y estaba fijada al decidir. Una fuga también puede aparecer al ajustar imputación, escalado o selección supervisada sobre todo el dataset.

Pregunta: ¿Es suficiente borrar la columna objetivo?
Respuesta orientativa: No. Otras variables, duplicados o transformaciones pueden revelar indirectamente el resultado.

Desarrollo conceptual: Un modelo más flexible puede reducir el error de entrenamiento y empeorar en datos que no usó para ajustar sus parámetros. La figura debe mostrar tanto la función ajustada como el error fuera de entrenamiento.
El nuevo laboratorio ajusta polinomios en una base de Chebyshev sobre puntos sintéticos con semilla fija. El grado controla capacidad y λ penaliza coeficientes sin penalizar el intercepto. Las curvas de error se calculan con los datos de ese mismo experimento.
Ejemplo: Comparar grados 1, 3 y 9 con 12 puntos de entrenamiento. Observar la forma ajustada y los MSE de train y validación. Repetir con 32 puntos, más ruido o λ>0. Los valores se calculan, no son curvas prefabricadas.
Error frecuente: Usar validación para seleccionar grado y después presentarla como un test final sesga la evaluación. Un único ejemplo sintético tampoco demuestra que regularizar siempre mejore.



## 33 · Capacidad y generalización

Mostrar ambas curvas en la misma escala. La trayectoria ilustrada representa un patrón posible, no un diagnóstico automático de toda divergencia entre curvas. Ruido, cambio de distribución, tamaños de muestra y regularización pueden afectar la comparación. Conservar el mejor checkpoint según una regla previamente definida.

Pregunta: ¿Una pérdida train más baja implica un mejor modelo?
Respuesta orientativa: No. La decisión depende de validación y del costo operativo.

Desarrollo conceptual: Un modelo más flexible puede reducir el error de entrenamiento y empeorar en datos que no usó para ajustar sus parámetros. La figura debe mostrar tanto la función ajustada como el error fuera de entrenamiento.
El nuevo laboratorio ajusta polinomios en una base de Chebyshev sobre puntos sintéticos con semilla fija. El grado controla capacidad y λ penaliza coeficientes sin penalizar el intercepto. Las curvas de error se calculan con los datos de ese mismo experimento.
Ejemplo: Comparar grados 1, 3 y 9 con 12 puntos de entrenamiento. Observar la forma ajustada y los MSE de train y validación. Repetir con 32 puntos, más ruido o λ>0. Los valores se calculan, no son curvas prefabricadas.
Error frecuente: Usar validación para seleccionar grado y después presentarla como un test final sesga la evaluación. Un único ejemplo sintético tampoco demuestra que regularizar siempre mejore.



## 34 · L2 y weight decay

La equivalencia entre penalización L2 y un factor multiplicativo de pesos se verifica para SGD estándar con convenciones adecuadas. No afirmar equivalencia universal para Adam. λ se selecciona con validación. La penalización reduce capacidad efectiva, pero no corrige una variable con información futura.

Pregunta: ¿Qué ocurre al aumentar demasiado λ?
Respuesta orientativa: Puede aparecer subajuste: la solución penalizada pierde capacidad predictiva.

Desarrollo conceptual: Un modelo más flexible puede reducir el error de entrenamiento y empeorar en datos que no usó para ajustar sus parámetros. La figura debe mostrar tanto la función ajustada como el error fuera de entrenamiento.
El nuevo laboratorio ajusta polinomios en una base de Chebyshev sobre puntos sintéticos con semilla fija. El grado controla capacidad y λ penaliza coeficientes sin penalizar el intercepto. Las curvas de error se calculan con los datos de ese mismo experimento.
Ejemplo: Comparar grados 1, 3 y 9 con 12 puntos de entrenamiento. Observar la forma ajustada y los MSE de train y validación. Repetir con 32 puntos, más ruido o λ>0. Los valores se calculan, no son curvas prefabricadas.
Error frecuente: Usar validación para seleccionar grado y después presentarla como un test final sesga la evaluación. Un único ejemplo sintético tampoco demuestra que regularizar siempre mejore.



## 35 · Dropout

El reescalado conserva la esperanza de cada activación, condicionado a h. No significa que cada red parcial produzca la misma salida ni que cualquier p mejore generalización. Usar los modos train/eval del framework y guardar semilla. Las unidades retiradas aquí son un mecanismo de regularización, no poda permanente.

Pregunta: ¿Dropout=0,5 implica eliminar la mitad de los parámetros al exportar?
Respuesta orientativa: No. La máscara actúa sobre activaciones durante entrenamiento.

Desarrollo conceptual: Un modelo más flexible puede reducir el error de entrenamiento y empeorar en datos que no usó para ajustar sus parámetros. La figura debe mostrar tanto la función ajustada como el error fuera de entrenamiento.
El nuevo laboratorio ajusta polinomios en una base de Chebyshev sobre puntos sintéticos con semilla fija. El grado controla capacidad y λ penaliza coeficientes sin penalizar el intercepto. Las curvas de error se calculan con los datos de ese mismo experimento.
Ejemplo: Comparar grados 1, 3 y 9 con 12 puntos de entrenamiento. Observar la forma ajustada y los MSE de train y validación. Repetir con 32 puntos, más ruido o λ>0. Los valores se calculan, no son curvas prefabricadas.
Error frecuente: Usar validación para seleccionar grado y después presentarla como un test final sesga la evaluación. Un único ejemplo sintético tampoco demuestra que regularizar siempre mejore.



## 36 · Early stopping y checkpoints

Detener después de paciencia épocas sin mejora no significa usar los últimos pesos. Documentar restore_best_weights o cargar explícitamente el checkpoint. No seleccionar la paciencia mirando test. La validación se usa para una decisión más y debe tener tamaño y representatividad suficientes.

Pregunta: ¿Qué pesos evaluamos al final?
Respuesta orientativa: Los del checkpoint elegido con validación según la regla definida.

Desarrollo conceptual: Un modelo más flexible puede reducir el error de entrenamiento y empeorar en datos que no usó para ajustar sus parámetros. La figura debe mostrar tanto la función ajustada como el error fuera de entrenamiento.
El nuevo laboratorio ajusta polinomios en una base de Chebyshev sobre puntos sintéticos con semilla fija. El grado controla capacidad y λ penaliza coeficientes sin penalizar el intercepto. Las curvas de error se calculan con los datos de ese mismo experimento.
Ejemplo: Comparar grados 1, 3 y 9 con 12 puntos de entrenamiento. Observar la forma ajustada y los MSE de train y validación. Repetir con 32 puntos, más ruido o λ>0. Los valores se calculan, no son curvas prefabricadas.
Error frecuente: Usar validación para seleccionar grado y después presentarla como un test final sesga la evaluación. Un único ejemplo sintético tampoco demuestra que regularizar siempre mejore.



## 37 · Desbalance: 95% de accuracy sin detectar bajas

La etiqueta positiva es abandono. Un clasificador trivial puede conseguir accuracy alta cuando la prevalencia positiva es baja. No usar este ejemplo para inferir que accuracy siempre carece de utilidad. Comparar con el baseline y reportar métricas alineadas con la acción y con la prevalencia del período.

Pregunta: ¿Cuántos clientes de riesgo detectó la política?
Respuesta orientativa: Ninguno.

Desarrollo conceptual: El score ordena riesgos; el umbral elige acciones; los costos y el efecto de la intervención determinan valor. Son niveles distintos de la decisión.
La matriz de confusión debe cambiar junto con los clientes seleccionados. Cada contacto cuesta C, también los verdaderos positivos. La utilidad didáctica incorpora una efectividad q supuesta; para afirmar retención incremental hace falta un contrafactual defendible.
Ejemplo: Con TP=3, FP=7, q=0,4, B=100 y C=5 UM, la utilidad proxy es 70 UM. El laboratorio usa otra cohorte sintética de 100 clientes con semilla 991 y muestra qué personas quedan seleccionadas en cada umbral.
Error frecuente: Una mayor ROC-AUC no garantiza mayor beneficio al umbral operativo. Una mayor probabilidad de baja tampoco identifica necesariamente al cliente que más respondería a una oferta.



## 38 · Matriz de confusión y política

Las filas representan clase real y las columnas decisión. La matriz debe sumar 100. Contactos=TP+FP=10. Los valores aquí son un ejemplo manual y no el resultado del dataset con semilla del laboratorio. Pedir a un alumno que interprete un falso positivo en unidades de contactos y costo.

Pregunta: ¿Cuál es la especificidad?
Respuesta orientativa: TN/(TN+FP)=88/95≈0,9263.

Desarrollo conceptual: El score ordena riesgos; el umbral elige acciones; los costos y el efecto de la intervención determinan valor. Son niveles distintos de la decisión.
La matriz de confusión debe cambiar junto con los clientes seleccionados. Cada contacto cuesta C, también los verdaderos positivos. La utilidad didáctica incorpora una efectividad q supuesta; para afirmar retención incremental hace falta un contrafactual defendible.
Ejemplo: Con TP=3, FP=7, q=0,4, B=100 y C=5 UM, la utilidad proxy es 70 UM. El laboratorio usa otra cohorte sintética de 100 clientes con semilla 991 y muestra qué personas quedan seleccionadas en cada umbral.
Error frecuente: Una mayor ROC-AUC no garantiza mayor beneficio al umbral operativo. Una mayor probabilidad de baja tampoco identifica necesariamente al cliente que más respondería a una oferta.



## 39 · Precision y recall dependen del umbral

No afirmar que precision siempre cae al bajar el umbral en cualquier muestra finita. Si no hay positivos predichos, precision queda indefinida salvo convención de reporte. El laboratorio muestra “no definida” en vez de simular una evidencia inexistente. Reportar también cantidades absolutas.

Pregunta: ¿Qué métrica cuenta cuántos abandonos quedaron fuera?
Respuesta orientativa: Recall junto con FN, o tasa de falsos negativos.

Desarrollo conceptual: El score ordena riesgos; el umbral elige acciones; los costos y el efecto de la intervención determinan valor. Son niveles distintos de la decisión.
La matriz de confusión debe cambiar junto con los clientes seleccionados. Cada contacto cuesta C, también los verdaderos positivos. La utilidad didáctica incorpora una efectividad q supuesta; para afirmar retención incremental hace falta un contrafactual defendible.
Ejemplo: Con TP=3, FP=7, q=0,4, B=100 y C=5 UM, la utilidad proxy es 70 UM. El laboratorio usa otra cohorte sintética de 100 clientes con semilla 991 y muestra qué personas quedan seleccionadas en cada umbral.
Error frecuente: Una mayor ROC-AUC no garantiza mayor beneficio al umbral operativo. Una mayor probabilidad de baja tampoco identifica necesariamente al cliente que más respondería a una oferta.



## 40 · ROC-AUC y curva precision-recall

ROC-AUC resume ordenamiento sobre umbrales y no fija la política final. La average precision (AP) pondera precisiones por incrementos de recall y puede diferir del área trapezoidal PR-AUC. El notebook reporta AP con su nombre correcto. Para scores sin información, la precisión de referencia está ligada a prevalencia. Calibración es una propiedad distinta.

Pregunta: ¿Un ROC-AUC mayor garantiza más beneficio a capacidad del 15%?
Respuesta orientativa: No. Hay que evaluar ese tramo, costos y calibración.

Desarrollo conceptual: El score ordena riesgos; el umbral elige acciones; los costos y el efecto de la intervención determinan valor. Son niveles distintos de la decisión.
La matriz de confusión debe cambiar junto con los clientes seleccionados. Cada contacto cuesta C, también los verdaderos positivos. La utilidad didáctica incorpora una efectividad q supuesta; para afirmar retención incremental hace falta un contrafactual defendible.
Ejemplo: Con TP=3, FP=7, q=0,4, B=100 y C=5 UM, la utilidad proxy es 70 UM. El laboratorio usa otra cohorte sintética de 100 clientes con semilla 991 y muestra qué personas quedan seleccionadas en cada umbral.
Error frecuente: Una mayor ROC-AUC no garantiza mayor beneficio al umbral operativo. Una mayor probabilidad de baja tampoco identifica necesariamente al cliente que más respondería a una oferta.



## 41 · Calibración y ranking

La frase expresa una propiedad poblacional y aproximada, no una promesa sobre cada cliente. Un diagrama de confiabilidad agrupa scores y compara frecuencia observada. El tamaño de los grupos y la incertidumbre importan. Calibrar con un conjunto aparte o un procedimiento dentro de validación, sin usar test.

Pregunta: ¿AUC cambia si aplico una transformación estrictamente creciente al score?
Respuesta orientativa: El orden se conserva, por lo que ROC-AUC se conserva salvo empates o efectos numéricos.

Desarrollo conceptual: El score ordena riesgos; el umbral elige acciones; los costos y el efecto de la intervención determinan valor. Son niveles distintos de la decisión.
La matriz de confusión debe cambiar junto con los clientes seleccionados. Cada contacto cuesta C, también los verdaderos positivos. La utilidad didáctica incorpora una efectividad q supuesta; para afirmar retención incremental hace falta un contrafactual defendible.
Ejemplo: Con TP=3, FP=7, q=0,4, B=100 y C=5 UM, la utilidad proxy es 70 UM. El laboratorio usa otra cohorte sintética de 100 clientes con semilla 991 y muestra qué personas quedan seleccionadas en cada umbral.
Error frecuente: Una mayor ROC-AUC no garantiza mayor beneficio al umbral operativo. Una mayor probabilidad de baja tampoco identifica necesariamente al cliente que más respondería a una oferta.



## 42 · Una utilidad esperada explícita

Este es un proxy didáctico condicionado a una efectividad q, no una estimación causal del resultado de campaña. Asume efecto solo en clientes que habrían abandonado y valor homogéneo. Para beneficio incremental real se requiere experimento o identificación causal apropiada. Corrige el proxy original que solo descontaba costo a FP.

Pregunta: ¿Podemos medir q solo con las etiquetas de abandono y los scores?
Respuesta orientativa: No. Falta información sobre el efecto de intervenir frente a no hacerlo.

Desarrollo conceptual: El score ordena riesgos; el umbral elige acciones; los costos y el efecto de la intervención determinan valor. Son niveles distintos de la decisión.
La matriz de confusión debe cambiar junto con los clientes seleccionados. Cada contacto cuesta C, también los verdaderos positivos. La utilidad didáctica incorpora una efectividad q supuesta; para afirmar retención incremental hace falta un contrafactual defendible.
Ejemplo: Con TP=3, FP=7, q=0,4, B=100 y C=5 UM, la utilidad proxy es 70 UM. El laboratorio usa otra cohorte sintética de 100 clientes con semilla 991 y muestra qué personas quedan seleccionadas en cada umbral.
Error frecuente: Una mayor ROC-AUC no garantiza mayor beneficio al umbral operativo. Una mayor probabilidad de baja tampoco identifica necesariamente al cliente que más respondería a una oferta.



## 43 · Umbral con costo y capacidad

El umbral teórico supone p calibrada, efecto q homogéneo y ausencia de restricciones. Con capacidad limitada, elegir los mayores beneficios esperados entre acciones positivas. Las UM son unidades monetarias didácticas. En el laboratorio se puede recorrer el umbral, exportar la curva y ver la matriz en cada paso.

Pregunta: ¿Si el presupuesto solo permite dos contactos, basta el umbral 0,125?
Respuesta orientativa: No. También debe imponerse la capacidad y priorizar utilidad esperada.

Desarrollo conceptual: El score ordena riesgos; el umbral elige acciones; los costos y el efecto de la intervención determinan valor. Son niveles distintos de la decisión.
La matriz de confusión debe cambiar junto con los clientes seleccionados. Cada contacto cuesta C, también los verdaderos positivos. La utilidad didáctica incorpora una efectividad q supuesta; para afirmar retención incremental hace falta un contrafactual defendible.
Ejemplo: Con TP=3, FP=7, q=0,4, B=100 y C=5 UM, la utilidad proxy es 70 UM. El laboratorio usa otra cohorte sintética de 100 clientes con semilla 991 y muestra qué personas quedan seleccionadas en cada umbral.
Error frecuente: Una mayor ROC-AUC no garantiza mayor beneficio al umbral operativo. Una mayor probabilidad de baja tampoco identifica necesariamente al cliente que más respondería a una oferta.



## 44 · Comparación justa: logística frente a MLP

El notebook mide ROC-AUC, AP, matriz y utilidad proxy sobre datos sintéticos con semilla fija. No incluye una tabla de resultados inventados. Repetir con semillas y bootstrap por unidad independiente si se desea estudiar variabilidad. Si el MLP no mejora, conservar la referencia es una conclusión válida.

Pregunta: ¿Qué comparación sería injusta?
Respuesta orientativa: Ajustar el umbral del MLP con test y el de la logística solo con train.

Desarrollo conceptual: El score ordena riesgos; el umbral elige acciones; los costos y el efecto de la intervención determinan valor. Son niveles distintos de la decisión.
La matriz de confusión debe cambiar junto con los clientes seleccionados. Cada contacto cuesta C, también los verdaderos positivos. La utilidad didáctica incorpora una efectividad q supuesta; para afirmar retención incremental hace falta un contrafactual defendible.
Ejemplo: Con TP=3, FP=7, q=0,4, B=100 y C=5 UM, la utilidad proxy es 70 UM. El laboratorio usa otra cohorte sintética de 100 clientes con semilla 991 y muestra qué personas quedan seleccionadas en cada umbral.
Error frecuente: Una mayor ROC-AUC no garantiza mayor beneficio al umbral operativo. Una mayor probabilidad de baja tampoco identifica necesariamente al cliente que más respondería a una oferta.



## 45 · Un score de riesgo no es un efecto causal

Y debe definirse consistentemente, por ejemplo retención. La expresión es el efecto promedio condicionado y no es observable a nivel individual porque solo se ve uno de los resultados potenciales. No llamar incremento de retención a una mejora de AUC. El proxy del laboratorio sirve para sensibilidad bajo supuestos explícitos.

Pregunta: ¿Podemos atribuir las bajas evitadas al modelo sin grupo de comparación?
Respuesta orientativa: No con una interpretación causal confiable.

Desarrollo conceptual: El score ordena riesgos; el umbral elige acciones; los costos y el efecto de la intervención determinan valor. Son niveles distintos de la decisión.
La matriz de confusión debe cambiar junto con los clientes seleccionados. Cada contacto cuesta C, también los verdaderos positivos. La utilidad didáctica incorpora una efectividad q supuesta; para afirmar retención incremental hace falta un contrafactual defendible.
Ejemplo: Con TP=3, FP=7, q=0,4, B=100 y C=5 UM, la utilidad proxy es 70 UM. El laboratorio usa otra cohorte sintética de 100 clientes con semilla 991 y muestra qué personas quedan seleccionadas en cada umbral.
Error frecuente: Una mayor ROC-AUC no garantiza mayor beneficio al umbral operativo. Una mayor probabilidad de baja tampoco identifica necesariamente al cliente que más respondería a una oferta.



## 46 · Interpretación, equidad y trazabilidad

La explicación de una predicción no prueba causalidad ni equidad. Definir segmentos con justificación y tamaño suficiente. Registrar incertidumbre y evitar exponer información personal. Una model card incluye uso previsto, limitaciones y evaluación. El responsable humano debe poder suspender la política si cambia el contexto.

Pregunta: ¿Qué información permitiría reproducir una decisión tomada hoy?
Respuesta orientativa: Versión de datos y modelo, transformaciones, score, umbral, costos y regla de acción vigentes.

Desarrollo conceptual: El score ordena riesgos; el umbral elige acciones; los costos y el efecto de la intervención determinan valor. Son niveles distintos de la decisión.
La matriz de confusión debe cambiar junto con los clientes seleccionados. Cada contacto cuesta C, también los verdaderos positivos. La utilidad didáctica incorpora una efectividad q supuesta; para afirmar retención incremental hace falta un contrafactual defendible.
Ejemplo: Con TP=3, FP=7, q=0,4, B=100 y C=5 UM, la utilidad proxy es 70 UM. El laboratorio usa otra cohorte sintética de 100 clientes con semilla 991 y muestra qué personas quedan seleccionadas en cada umbral.
Error frecuente: Una mayor ROC-AUC no garantiza mayor beneficio al umbral operativo. Una mayor probabilidad de baja tampoco identifica necesariamente al cliente que más respondería a una oferta.



## 47 · Mapa de arquitecturas

Este mapa describe sesgos de arquitectura, no un ranking universal de calidad. CNN puede aplicarse a secuencias y Transformers a datos tabulares. La elección depende del protocolo y costo medidos. El segundo deck desarrolla recurrencia, gates y evaluación temporal, sin desplazar la clase principal de fundamentos.

Pregunta: ¿Qué criterio manda al elegir una arquitectura?
Respuesta orientativa: El tipo de señal, los datos disponibles y la evidencia de mejora en el uso previsto.



## 48 · Actividad: defensa de una política

Reservar los últimos minutos para una defensa breve. Una respuesta sólida incluye fecha de corte, train/valid/test, costo por contacto, capacidad y efecto de intervención supuesto. Evaluar claridad del argumento y evidencia, sin premiar complejidad por sí misma. Consultar rúbrica y respuestas en la guía docente.

Pregunta: ¿Adoptarían una red con mayor AUC y menor utilidad de validación?
Respuesta orientativa: No por AUC solamente. Revisar incertidumbre y política; si la desventaja persiste, mantener baseline.



## 49 · Comprobación de comprensión

Dar dos minutos individuales y luego contrastar en parejas. Respuestas: 13 parámetros bajo la convención de sesgo por unidad; XOR no es linealmente separable en las entradas originales; BCE no mide efecto causal ni utilidad de una campaña. Usar las respuestas para detectar confusión entre capacidad, aprendizaje y decisión.

Pregunta: ¿Qué concepto une los tres problemas?
Respuesta orientativa: Cada modelo y cada métrica tienen un alcance concreto que debe explicitarse.



## 50 · Material para continuar

Los seis videos quedan organizados por tema y diapositiva. Se verificaron URLs y metadatos accesibles, con límites expresos sobre reproducción, audio y subtítulos. Los recursos originales ampliados y las preguntas del módulo se conservan como consulta. Repetir el notebook permite observar que una red puede ganar o perder frente al baseline según la muestra.

Pregunta: ¿Qué experimento harías antes de usar datos reales?
Respuesta orientativa: Reproducir un caso sintético con semilla, verificar gradientes y comprobar que el pipeline no usa test para ajuste.



## 51 · Cierre: evidencia para decidir

Cerrar retomando el caso inicial. Pedir un compromiso concreto de evaluación: qué baseline, qué separación, qué métrica de negocio y qué condición detendría el despliegue. La clase termina a las 12:00. Las 23 diapositivas de ampliación quedan disponibles para estudio autónomo y preparación del siguiente encuentro.

Pregunta: ¿Qué dato falta para pasar de riesgo a retención incremental?
Respuesta orientativa: Evidencia del efecto de la intervención, idealmente un experimento con grupo de comparación.