# Notas del expositor



## 01 · Secuencias, RNN y LSTM

Este deck amplía la clase de fundamentos. El objetivo es calcular estados temporales, comprender las dificultades de aprender dependencias largas y diseñar evaluación cronológica. Evitar presentar memoria como comprensión humana o garantía de pronóstico. Todos los números de los ejemplos son didácticos.

Pregunta: ¿Cuándo puede importar el orden?
Respuesta orientativa: Cuando el significado o el resultado dependen de observaciones previas.



## 02 · El orden puede contener información

Una fila tabular también puede contener rezagos diseñados. La diferencia no es simplemente el formato del archivo, sino cómo representamos las dependencias. No todas las dependencias secuenciales son temporales físicas: el orden de palabras es otro ejemplo. Verificar cuándo se conoce cada variable.

Pregunta: ¿Podemos modelar una serie con un árbol?
Respuesta orientativa: Sí, construyendo rezagos y un protocolo temporal correcto.



## 03 · Ventanas para predecir demanda

Con serie 10,12,11,14,15, una primera entrada contiene 10,12,11,14 y el objetivo es 15. La escala se ajusta solo con train. Las ventanas pueden compartir pasado conocido, pero ninguna etiqueta futura puede incorporarse como atributo. El horizonte determina qué covariables son legales.

Pregunta: ¿La venta de t+1 puede estar en Xₜ?
Respuesta orientativa: No, porque aún no existe cuando emitimos el pronóstico.



## 04 · Formas de entrada y salida

Definir batch, longitud y número de atributos por paso. Las API pueden usar batch-first o sequence-first, por lo que conviene escribir dimensiones explícitas. Una máscara impide que el padding aporte señal espuria. En producción, el estado inicial y los reinicios por serie deben documentarse.

Pregunta: ¿Qué representa la dimensión temporal de una ventana?
Respuesta orientativa: La secuencia ordenada de observaciones por ejemplo.



## 05 · La recurrencia transporta un estado

h no es una copia literal de todo el pasado. Es una representación de dimensión fija. Compartir pesos reduce el crecimiento de parámetros con longitud, pero el cómputo recurrente sigue dependiendo de pasos anteriores. La salida de regresión es afín en este ejemplo.

Pregunta: ¿Aumentar de 10 a 20 pasos duplica parámetros?
Respuesta orientativa: No si se reutilizan las mismas matrices. Aumenta cómputo y activaciones de entrenamiento.



## 06 · RNN desplegada en el tiempo

El despliegue convierte la recurrencia finita en un grafo acíclico para una secuencia concreta. El flujo de estados va hacia delante y el gradiente vuelve por el mismo grafo. No interpretar las copias como modelos independientes. Esto permite explicar BPTT sin una nueva regla de derivación.

Pregunta: ¿Qué pasaría si cada paso tuviera pesos distintos?
Respuesta orientativa: Cambiaría el modelo y perderíamos el esquema habitual de pesos compartidos.



## 07 · Parámetros de una RNN

Algunas bibliotecas separan sesgos de entrada y recurrente: su conteo será mayor. Aquí contamos una formulación matemática con un sesgo por unidad oculta. El número de pasos no aparece en la fórmula porque comparte parámetros. La capa de salida agrega m+1 parámetros para regresión escalar.

Pregunta: ¿Por qué aparece m²?
Respuesta orientativa: Por todas las conexiones del estado anterior al nuevo estado oculto.



## 08 · Forward de una RNN escalar

El segundo estado depende del primero. Estos parámetros están fijados a mano para demostrar la recurrencia. No confundir persistencia de estado con entrenamiento de memoria larga. Verificar con calculadora o las pruebas del paquete. Un cambio de Wₕ altera tanto la retención como la estabilidad de la dinámica.

Pregunta: ¿Cuánto vale h₂ si Wₕ=0?
Respuesta orientativa: Cero con x₂=0 y b=0.



## 09 · Pérdida sobre una secuencia

Una suma y un promedio producen escalas de gradiente distintas. Definir la reducción utilizada es parte de la especificación. Para un pronóstico de muchos a uno, solo se observa la pérdida del objetivo final. Para secuencias de distinta longitud, un promedio por token o por secuencia pondera ejemplos de modo diferente.

Pregunta: ¿Dos pérdidas con igual mínimo pueden generar pasos distintos?
Respuesta orientativa: Sí, si difieren por un factor de escala y mantenemos η.



## 10 · BPTT aplica la regla de la cadena

BPTT significa backpropagation through time. El parámetro compartido recibe la suma de todos los caminos por los que influye en la pérdida. Las derivadas no viajan literalmente por un reloj físico: recorren el grafo construido durante el forward. La memoria necesaria crece con las activaciones guardadas.

Pregunta: ¿BPTT necesita un optimizador especial?
Respuesta orientativa: No. Calcula gradientes que pueden usar SGD, Adam u otros optimizadores.



## 11 · Productos temporales de Jacobianos

La fórmula corresponde a tanh aplicada componente a componente con vectores columna. La norma del producto no depende solo de un autovalor fijo: los Jacobianos varían con t. Usar ejemplos escalares constantes ilustra el mecanismo sin presentar una condición universal para todas las matrices.

Pregunta: ¿Por qué tanh saturada puede dificultar el aprendizaje?
Respuesta orientativa: Porque 1−h² se acerca a cero y reduce la sensibilidad local.



## 12 · Vanishing y exploding gradients

Son productos hipotéticos, no métricas de una RNN entrenada. Una dependencia estadística larga puede existir aunque el gradiente que permitiría aprenderla sea pequeño. Un gradiente grande no implica que la predicción sea de valor. El objetivo es relacionar escala numérica y dificultad de optimización.

Pregunta: ¿Una dependencia larga exige siempre recordar literalmente cada dato?
Respuesta orientativa: No. Puede bastar un resumen adecuado, pero aprenderlo puede ser difícil.



## 13 · Clipping y BPTT truncada

τ debe ser positivo. Clipping no soluciona gradientes desvanecidos. En BPTT truncada puede arrastrarse el estado entre segmentos pero cortar el grafo con detach, por lo que no se aprende a través de todos los pasos anteriores. Documentar dónde se reinicia estado entre series para no contaminar unidades distintas.

Pregunta: ¿Truncar a 20 pasos permite atribuir directamente una pérdida a 100 pasos atrás?
Respuesta orientativa: No por el grafo truncado, aunque el estado pueda transportar información.



## 14 · LSTM agrega memoria controlada

LSTM introduce un camino aditivo de memoria. Las compuertas son vectores aprendidos, no decisiones humanas ni porcentajes fijos de todas las celdas. El laboratorio los fija para aislar sus efectos y debe interpretarse como un modelo escalar simplificado. No garantiza recordar todo ni elimina todo problema de gradiente.

Pregunta: ¿Por qué se necesitan c y h?
Respuesta orientativa: Separan la memoria interna de la parte expuesta a la salida y al siguiente cálculo de gates.



## 15 · Compuerta de olvido

Mantener la convención de concatenación en las tres compuertas y el candidato. El sesgo inicial de olvido afecta la dinámica inicial, pero no fija la memoria final después de entrenar. Un valor cercano a uno conserva gran parte del estado por el camino directo, condicionado al resto del sistema.

Pregunta: ¿Qué implica fₜ=0 en una componente?
Respuesta orientativa: Elimina la contribución directa de esa componente de cₜ₋₁ a cₜ en ese paso.



## 16 · Entrada y contenido candidato

g no es una cuarta sigmoide. Su rango (−1,1) permite escribir contenido firmado. La compuerta i controla magnitud y g contenido, aunque ambos se aprenden conjuntamente. El producto i⊙g no tiene por qué incrementar c: puede reducirlo si g es negativo.

Pregunta: ¿Abrir i siempre aumenta c?
Respuesta orientativa: No. Depende del signo de g y del estado anterior.



## 17 · Actualización aditiva de la celda

c no pasa obligatoriamente por tanh al actualizarse, por eso puede acumular magnitud mayor que uno. La salida sí incorpora tanh(c). El camino directo aditivo facilita aprender ciertas dependencias, sujeto a las compuertas y al entrenamiento. No describirlo como memoria infinita.

Pregunta: ¿Puede c=2 aunque g esté entre −1 y 1?
Respuesta orientativa: Sí, por acumulación de memoria previa.



## 18 · Compuerta de salida y estado oculto

Con o cercano a cero, h puede ser pequeño aunque c tenga magnitud grande. Eso no borra c automáticamente. Como los gates futuros dependen de h, modificar o también puede afectar el desarrollo posterior en una LSTM completa. El modelo de gates constantes omite esa realimentación.

Pregunta: ¿o=0 obliga a c=0?
Respuesta orientativa: No. Fuerza h=0 en ese paso, pero c puede conservar información.



## 19 · LSTM: ecuaciones completas

Es la variante estándar sin peepholes ni proyección. Otras variantes cambian la parametrización y deben indicarse. La implementación de PyTorch usa matrices separadas de entrada y estado y dos sesgos por grupo, algebraicamente combinables con esta formulación. Verificar orden de gates al exportar pesos entre frameworks.

Pregunta: ¿Cuáles son los parámetros entrenables?
Respuesta orientativa: Las matrices y sesgos de cada gate y del candidato, además de la capa de salida.



## 20 · Ejemplo: conservar y escribir

Los gates están fijados a mano. Podrían obtenerse con logits logit(0,9), logit(0,2) y atanh(−0,5), pero aquí no entrenamos sus matrices. La escritura negativa reduce la memoria respecto de la parte conservada. Resolver antes de abrir el laboratorio.

Pregunta: ¿Cuánto vale cₜ si i=0?
Respuesta orientativa: 0,72.



## 21 · Ejemplo: exponer la memoria

El valor exacto se obtiene con la misma función usada en las pruebas. Diferenciar estado interno y estado expuesto con colores y etiquetas. Si o cambia a 0,1, h se reduce, mientras c se mantiene 0,62 en este cálculo aislado. En una LSTM completa, h participará en los gates del siguiente paso.

Pregunta: ¿Qué memoria ve la capa de salida si o baja?
Respuesta orientativa: Una versión más atenuada mediante h, no necesariamente una celda borrada.



## 22 · Persistencia con gates constantes

Vida media = ln(0,5)/ln(f), para 0<f<1. Como c₁=0,5, después de unos 6,58 intervalos queda la mitad de ese valor. En una secuencia discreta se observan pasos enteros. f=1 conserva el impulso y f=0 lo borra al siguiente paso. Esto describe la dinámica simplificada, no un resultado entrenado.

Pregunta: ¿Qué sucede si f=1 y no llega más contenido?
Respuesta orientativa: c permanece constante en este modelo.



## 23 · Qué dice el gradiente directo

Evitar la simplificación de afirmar que toda la derivada de una LSTM siempre es f. Los gates dependen de h anterior y este depende de c anterior, de modo que el gradiente total incluye otros caminos. El camino aditivo es una ventaja estructural, no un teorema de gradiente perfecto.

Pregunta: ¿LSTM elimina todo vanishing gradient?
Respuesta orientativa: No. Lo mitiga en ciertos caminos y condiciones, pero aún requiere diseño y entrenamiento adecuados.



## 24 · Laboratorio: retener, alternar, sobrescribir

La trayectoria se revela paso a paso. Controles manuales para f, i, o y paso temporal. Pausar, cambiar un gate y comparar una nueva trayectoria desde c₀=0. La pantalla aclara que no se entrenan pesos y que no representa una LSTM vectorial completa. Exportar CSV conserva g, c y h.

Pregunta: ¿Qué diferencia observás al cerrar o en vez de cerrar f?
Respuesta orientativa: Cerrar o oculta la memoria en h; cerrar f elimina su contribución previa en c.



## 25 · Conteo de parámetros LSTM

La cuenta asume un único vector de sesgo por transformación, sin proyección ni peepholes. PyTorch usa dos vectores de sesgo y arroja 4m(d+m+2), por lo que para d=2,m=3 cuenta 84 parámetros internos. La capa de salida agrega sus parámetros por separado. Registrar esta convención evita discrepancias falsas.

Pregunta: ¿La longitud de la secuencia aparece en P?
Respuesta orientativa: No. Sí afecta cómputo y memoria de activaciones.



## 26 · GRU: una alternativa con menos compuertas

Esta ecuación elige z como proporción del candidato. Otras bibliotecas usan z para retención y pueden aplicar el gate de reinicio en otra posición. No mezclar pesos entre variantes sin verificar. Menos parámetros no asegura superioridad de precisión o tiempo en todos los equipos.

Pregunta: ¿Qué conserva el pasado en esta convención?
Respuesta orientativa: 1−z.



## 27 · RNN, LSTM/GRU y Transformer

Comparar con criterios de longitud, dimensión, datos y hardware. RNN procesa un estado por paso. LSTM/GRU agregan control y operaciones. Un Transformer estándar permite paralelizar posiciones durante entrenamiento con máscaras apropiadas, pero la generación autoregresiva sigue siendo secuencial. No afirmar que siempre necesita más datos o siempre rinde mejor.

Pregunta: ¿La atención recibe el orden temporal sin posición ni máscara?
Respuesta orientativa: No de la forma requerida para distinguir el orden en el Transformer estándar.



## 28 · Costo y paralelización dependen del uso

Estas son escalas simplificadas de capas y omiten constantes, batches y componentes de feedforward. Atención eficiente y caches alteran costos prácticos. La memoria de una implementación estándar de atención puede crecer cuadráticamente en T, pero existen kernels y variantes distintas. Medir latencia, memoria y calidad en el entorno del proyecto.

Pregunta: ¿Una menor complejidad asintótica garantiza menos latencia para T pequeño?
Respuesta orientativa: No. Constantes, hardware y paralelización pueden dominar.



## 29 · Partición cronológica para demanda

Las ventanas de evaluación pueden usar observaciones del pasado inmediato si ya se conocen al origen del pronóstico. Para horizontes solapados, usar un gap cuando corresponda para impedir contaminación de etiquetas futuras. Ajustar escalado solo en entrenamiento de cada fold. No barajar fechas antes de partir.

Pregunta: ¿Una ventana test puede contener valores de train?
Respuesta orientativa: Sí como historial conocido, siempre que ninguna observación futura al origen se filtre.



## 30 · Walk-forward

La ventana expansiva retiene todo el pasado; la móvil descarta lo más antiguo. Definir si se reentrena el modelo y cada cuánto. Los errores de horizontes y orígenes solapados pueden ser dependientes: no tratarlos como observaciones independientes al estimar intervalos. Congelar el protocolo antes de comparar.

Pregunta: ¿Por qué un split aleatorio puede sobreestimar calidad temporal?
Respuesta orientativa: Permite que entrenamiento vea períodos posteriores a los que intenta predecir.



## 31 · Baseline ingenuo y estacional

El período s debe corresponder a la frecuencia y al patrón, por ejemplo 7 para datos diarios con ciclo semanal. Para datos semanales anuales puede considerarse 52 con precaución por calendario. No inventar que LSTM supera este baseline. El notebook usa una señal sintética y mide resultados de verdad.

Pregunta: ¿Qué baseline exigirías para demanda diaria con patrón semanal?
Respuesta orientativa: Como mínimo, el ingenuo estacional de siete días.



## 32 · MAE, RMSE y límites de MAPE

e=ŷ−y. WAPE=Σ|e|/Σ|y| también es indefinida si el denominador es cero y puede ocultar segmentos. Para decisiones de stock pueden importar costos asimétricos o cuantiles, no solo error simétrico. Informar horizonte y nivel de agregación de cada métrica.

Pregunta: ¿Cómo reportarías MAPE si hay y=0?
Respuesta orientativa: No como un porcentaje válido sin una regla explícita. Preferir MAE/RMSE o métricas escaladas apropiadas.



## 33 · Práctica reproducible en Python

El notebook incluye una celda LSTM CPU opcional con semilla fija y entrenamiento breve. La práctica básica con NumPy y scikit-learn no requiere GPU ni API. Registrar versiones. No transferir estado entre series independientes. La semilla ayuda a reproducir dentro de un entorno, pero no asegura bits idénticos entre versiones y dispositivos.

Pregunta: ¿Qué entregar además del score?
Respuesta orientativa: Fechas de corte, ventanas, transformaciones, versiones, baseline y costo de cómputo.



## 34 · Defensa final y respuestas

Ejercicio 1: con c previo 0,8, f=0,9, i=0,2 y g=−0,5, c=0,62. Ejercicio 2: con o=0,75, h≈0,413346. Ejercicio 3: proponer dos orígenes walk-forward sin información futura. La guía contiene rúbrica y respuestas ampliadas. Cerrar con una condición operativa para rechazar complejidad sin ganancia.

Pregunta: ¿Adoptarías LSTM si la mejora media es pequeña y varía de signo por período?
Respuesta orientativa: Revisar incertidumbre y costo. Esa evidencia puede ser insuficiente para justificar adopción.