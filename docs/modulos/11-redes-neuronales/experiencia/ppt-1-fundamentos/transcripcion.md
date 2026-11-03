# Redes neuronales: fundamentos y decisiones



## 01 · Redes neuronales

Redes neuronales

Fundamentos, aprendizaje y decisiones de negocio

Ciencias de Datos II · UCA

Sergio Gevatschnaider · 5 de noviembre de 2026



¿Qué debería mejorar una red para justificar su uso?



## 02 · La decisión de retención

La decisión de retención

Unidad: cliente al cierre de un mes

Objetivo: abandono en los próximos 30 días

Acción: ofrecer una intervención con presupuesto limitado



¿Una cancelación ya confirmada puede ser una variable predictora?



## 03 · Resultados de aprendizaje

Resultados de aprendizaje

Calcular una predicción y un gradiente

Explicar capas, activaciones y parámetros

Defender una política con evidencia de validación



¿Qué evidencia distinguiría comprensión de repetición de fórmulas?



## 04 · Ruta de clase: 9:30 a 12:00

Ruta de clase: 9:30 a 12:00

9:30–10:15 · decisión, neurona, XOR y activaciones

10:15–11:05 · forward, pérdidas y backpropagation

11:05–12:00 · generalización, churn y defensa



¿Qué pregunta conecta los tres bloques?



## 05 · Cuándo conviene una solución simple

Cuándo conviene una solución simple

Pocos ejemplos o etiquetas poco confiables

Exigencias estrictas de interpretación o latencia

Baselines tabulares que ya cumplen el objetivo



¿Más datos garantizan que una red supere a un árbol?



## 06 · Regresión logística como baseline

Regresión logística como baseline

Un score afín se transforma en una probabilidad modelada

La frontera con umbral 0,5 es un hiperplano

La calibración debe comprobarse fuera de entrenamiento

z = wᵀx + b
p = σ(z) = 1 / (1 + exp(−z))

¿Qué agrega una capa oculta a esta función?



## 07 · Entradas, pesos, sesgo y activación

Entradas, pesos, sesgo y activación

x contiene atributos medibles

w y b son parámetros aprendidos

φ transforma la suma ponderada

z = w₁x₁ + w₂x₂ + b
a = φ(z)

¿Cambiar la unidad de x cambia la interpretación de w?



## 08 · Inferencia: un cálculo verificable

Inferencia: un cálculo verificable

x₁ = 0,8 y x₂ = 0,4

w₁ = 1, w₂ = −0,5 y b = −0,1

Con umbral 0,5, la clase predicha es 1

z = 0,8 − 0,2 − 0,1 = 0,5
p = σ(0,5) = 0,622459

¿Qué ocurre si b baja a −0,6?



## 09 · Una frontera lineal

Una frontera lineal

El signo de wᵀx+b separa dos semiespacios

La regla del perceptrón corrige errores de clasificación

Convergencia: datos separables y condiciones de aprendizaje apropiadas

ŷ = 1[z ≥ 0]
w ← w + η(y−ŷ)x

¿Qué cambia el sesgo?



## 10 · XOR exige una representación distinta

XOR exige una representación distinta

(0,0) y (1,1) pertenecen a la clase 0

(1,0) y (0,1) pertenecen a la clase 1

Ninguna recta separa las clases en las entradas originales

XOR(0,0)=0   XOR(0,1)=1
XOR(1,0)=1   XOR(1,1)=0

¿Basta con entrenar más épocas un perceptrón?



## 11 · XOR con dos unidades ReLU

XOR con dos unidades ReLU

Una unidad detecta suma superior a cero

La segunda corrige cuando ambas entradas están activas

Ejemplo constructivo con salida exacta sobre los cuatro puntos

h₁ = ReLU(x₁+x₂)
h₂ = ReLU(x₁+x₂−1)
ŷ = h₁ − 2h₂

¿Cuánto vale la salida para (1,1)?



## 12 · Dimensiones y parámetros de un MLP

Dimensiones y parámetros de un MLP

Dos entradas, tres unidades ocultas y una salida

W₁: 3×2, b₁: 3, W₂: 1×3, b₂: 1

Cada conexión y cada sesgo agrega un parámetro

Parámetros = 3·2 + 3 + 1·3 + 1 = 13

¿Cuántos parámetros tiene una capa d→m con sesgo?



## 13 · La no linealidad cambia la capacidad

La no linealidad cambia la capacidad

Dos capas afines sin activación colapsan en una

La profundidad por sí sola no introduce no linealidad

Las activaciones permiten representaciones por regiones

W₂(W₁x+b₁)+b₂ = Ax+c

¿Qué ocurre si todas las capas ocultas usan identidad?



## 14 · Sigmoide: salida acotada y saturación

Sigmoide: salida acotada y saturación

Rango: (0,1)

Derivada máxima: 0,25 en z=0

En los extremos la sensibilidad se aproxima a cero

σ(z) = 1/(1+e⁻ᶻ)
σ′(z) = σ(z)(1−σ(z))

¿Cuál es la derivada en z=0?



## 15 · ReLU, tanh y Leaky ReLU

ReLU, tanh y Leaky ReLU

tanh se centra en cero, pero también satura

ReLU mantiene pendiente 1 en el lado positivo

Leaky ReLU conserva una pendiente α en el lado negativo

tanh′(z) = 1−tanh²(z)
ReLU(z)=max(0,z),  φ′(z)=1[z>0]
Leaky(z)=max(αz,z), 0<α<1

¿Una activación con salida grande tiene siempre derivada grande?



## 16 · Salida según el objetivo

Salida según el objetivo

Binaria: una sigmoide y BCE

Multiclase exclusiva: softmax y entropía cruzada

Regresión: identidad y una pérdida adecuada al ruido

softmax(z)ₖ = exp(zₖ−m) / Σⱼexp(zⱼ−m)
m = maxⱼ zⱼ

¿Dos etiquetas que pueden coexistir requieren softmax?



## 17 · Laboratorio de activaciones

Laboratorio de activaciones

Escenario 1: recorrer z entre −6 y 6

Escenario 2: observar saturación

Escenario 3: cruzar el punto no derivable de ReLU



¿Qué se pierde al observar solo la curva de activación?



## 18 · Forward propagation

Forward propagation

Las entradas pasan por las capas con pesos fijos

El entrenamiento agrega una pérdida y sus derivadas

La inferencia termina en la predicción

h = φ(W₁x+b₁)
z₂ = W₂h+b₂
p = σ(z₂)

¿El forward cambia los pesos?



## 19 · BCE para clasificación binaria

BCE para clasificación binaria

Penaliza probabilidades incompatibles con y

Usa logaritmo natural y promedia sobre ejemplos

La implementación con logits mejora estabilidad numérica

L = −[y·ln(p)+(1−y)·ln(1−p)]
y=1, p=0,622459: L=0,474077

¿Qué pérdida tiene un acierto con probabilidad 0,5?



## 20 · MSE para regresión

MSE para regresión

Penaliza más los errores grandes

Se expresa en unidades al cuadrado

RMSE devuelve la escala original del objetivo

MSE = (1/n) Σᵢ(ŷᵢ−yᵢ)²
y=10, ŷ=8: error²=4

¿Cambiar la unidad monetaria altera MSE?



## 21 · El grafo de una neurona logística

El grafo de una neurona logística

Un ejemplo: x=2, y=1, w=0,3 y b=−0,1

Primero se calcula z, luego p y después L

Derivaremos respecto de w y b

z=0,5   p=0,622459   L=0,474077

¿Qué valores deben guardarse para la derivación?



## 22 · Regla de la cadena

Regla de la cadena

Cada derivada local mide una sensibilidad

El producto conecta w con la pérdida

En redes ramificadas se suman contribuciones

∂L/∂w = (∂L/∂p)(∂p/∂z)(∂z/∂w)

¿Por qué se suman gradientes cuando un parámetro tiene varios caminos?



## 23 · Backpropagation: resultado numérico

Backpropagation: resultado numérico

p−y = −0,377541

∂L/∂w = (p−y)x = −0,755081

∂L/∂b = p−y = −0,377541

∂L/∂z = p−y
∇L = (−0,755081, −0,377541)

¿Por qué el gradiente de w duplica al de b?



## 24 · Una actualización de descenso

Una actualización de descenso

Con η=0,1: w pasa a 0,375508

b pasa a −0,062246

El nuevo forward reduce la BCE a aproximadamente 0,4069

wₙᵤₑᵥₒ = w−η·∂L/∂w
bₙᵤₑᵥₒ = b−η·∂L/∂b

¿En qué dirección se movieron ambos parámetros?



## 25 · Backpropagation en una capa oculta

Backpropagation en una capa oculta

El error de salida se transporta por los pesos

La derivada de la activación modula la señal

Un producto externo construye el gradiente de W

δ₂ = p−y
δ₁ = (W₂ᵀδ₂) ⊙ φ′(z₁)
∂L/∂W₁ = δ₁xᵀ

¿Qué dimensión tiene el gradiente de W₁?



## 26 · Learning rate y estabilidad

Learning rate y estabilidad

Paso pequeño: avance lento

Paso intermedio: descenso estable en este ejemplo

Paso excesivo: oscilación o divergencia

L(w)=½(w−2)²
wₜ₊₁−2 = (1−η)(wₜ−2)

¿Qué sucede con η=1 en esta parábola?



## 27 · Mini-batch, iteración y época

Mini-batch, iteración y época

Mini-batch: ejemplos para estimar un gradiente

Iteración: una actualización

Época: recorrido del conjunto de entrenamiento

n=1.000, batch=100
10 actualizaciones por época

¿Cinco épocas equivalen a cinco actualizaciones?



## 28 · Inicialización y escalado

Inicialización y escalado

Romper simetrías entre unidades

Mantener una escala razonable de activaciones

Ajustar transformaciones solo con entrenamiento

He para ReLU: Var(w) ≈ 2/fan_in

¿Por qué no estimar el escalado con todo el dataset?



## 29 · Gradientes que se atenúan o explotan

Gradientes que se atenúan o explotan

Productos de Jacobianos pueden cambiar mucho de escala

Saturación limita la señal de aprendizaje

Inicialización, arquitectura y clipping cumplen papeles distintos

∂L/∂h₀ contiene productos de ∂hₖ/∂hₖ₋₁

¿Clipping resuelve un gradiente casi nulo?



## 30 · Laboratorio de optimización

Laboratorio de optimización

BCE: aprender w y b con cuatro observaciones

Cuadrática estable: observar convergencia

Cuadrática inestable: explicar oscilación y divergencia



¿Cómo verificarías una derivada implementada?



## 31 · Train, validación y test

Train, validación y test

Train ajusta parámetros y transformaciones

Validación selecciona arquitectura y umbral

Test estima desempeño final de la política elegida



¿Dónde elegimos el umbral de retención?



## 32 · Fuga de información en churn

Fuga de información en churn

Ejemplo: usar el motivo de baja para predecir la baja

Transformaciones y selección de variables dentro del split

Repeticiones del mismo cliente requieren agrupamiento



¿Es suficiente borrar la columna objetivo?



## 33 · Curvas de generalización

Curvas de generalización

La pérdida de train puede seguir bajando

Un deterioro de validación alerta sobre sobreajuste

La curva es esquemática, no un resultado medido



¿Una pérdida train más baja implica un mejor modelo?



## 34 · L2 y weight decay

L2 y weight decay

L2 penaliza pesos grandes en la función objetivo

El sesgo suele quedar fuera de la penalización

Con optimizadores adaptativos, L2 y decay desacoplado difieren

J = L_datos + (λ/2)‖W‖²
∂J/∂W = ∂L_datos/∂W + λW

¿Qué ocurre al aumentar demasiado λ?



## 35 · Dropout

Dropout

Durante entrenamiento elimina activaciones al azar

Inverted dropout reescala las supervivientes

Durante inferencia se desactiva la máscara

h̃ = m ⊙ h / (1−p_drop)
mⱼ ~ Bernoulli(1−p_drop)

¿Dropout=0,5 implica eliminar la mitad de los parámetros al exportar?



## 36 · Early stopping y checkpoints

Early stopping y checkpoints

Monitorear una métrica de validación

Definir paciencia y mejora mínima

Restaurar el mejor checkpoint al terminar



¿Qué pesos evaluamos al final?



## 37 · Desbalance: 95% de accuracy sin detectar bajas

Desbalance: 95% de accuracy sin detectar bajas

Ejemplo sintético: 100 clientes, 5 abandonos

Predecir siempre “no abandona” acierta 95

Recall de abandono: 0 de 5

Accuracy = 95/100 = 95%
Recall = 0/5 = 0%

¿Cuántos clientes de riesgo detectó la política?



## 38 · Matriz de confusión y política

Matriz de confusión y política

Ejemplo sintético con umbral fijo

TP=3, FP=7, FN=2, TN=88

Diez contactos para detectar tres de cinco abandonos

Precision = 3/10 = 0,30
Recall = 3/5 = 0,60

¿Cuál es la especificidad?



## 39 · Precision y recall dependen del umbral

Precision y recall dependen del umbral

Bajar el umbral suele aumentar contactos y recall

Precision puede subir o bajar según los scores

Capacidad y costo definen qué intercambio conviene

Precision = TP/(TP+FP)
Recall = TP/(TP+FN)

¿Qué métrica cuenta cuántos abandonos quedaron fuera?



## 40 · ROC-AUC y curva precision-recall

ROC-AUC y curva precision-recall

ROC compara TPR frente a FPR

Precision-recall enfoca la clase positiva

La prevalencia cambia la referencia de precisión

TPR = TP/(TP+FN)
FPR = FP/(FP+TN)

¿Un ROC-AUC mayor garantiza más beneficio a capacidad del 15%?



## 41 · Calibración y ranking

Calibración y ranking

Ranking ordena clientes por score

Calibración relaciona probabilidades con frecuencias

Un buen ordenamiento puede coexistir con mala calibración

P(Y=1 | p≈0,20) ≈ 0,20

¿AUC cambia si aplico una transformación estrictamente creciente al score?



## 42 · Una utilidad esperada explícita

Una utilidad esperada explícita

q: probabilidad supuesta de evitar una baja detectada

B: margen preservado por baja evitada

C: costo de cada contacto, también para verdaderos positivos

U_proxy = TP·q·B − (TP+FP)·C

¿Podemos medir q solo con las etiquetas de abandono y los scores?



## 43 · Umbral con costo y capacidad

Umbral con costo y capacidad

Ejemplo manual: TP=3, FP=7

q=0,4, B=100 UM y C=5 UM por contacto

U_proxy=3·0,4·100−10·5=70 UM

Actuar si p·q·B > C
p > C/(q·B) = 0,125

¿Si el presupuesto solo permite dos contactos, basta el umbral 0,125?



## 44 · Comparación justa: logística frente a MLP

Comparación justa: logística frente a MLP

Mismas filas, objetivo, splits y transformaciones

Selección con validación y presupuesto comparable

Test final con política congelada y costos documentados



¿Qué comparación sería injusta?



## 45 · Un score de riesgo no es un efecto causal

Un score de riesgo no es un efecto causal

Clientes de alto riesgo pueden no responder a una oferta

Medir retención incremental requiere contrafactual

Un experimento aleatorizado permite estimar el efecto

E[Y(1)−Y(0) | X=x]

¿Podemos atribuir las bajas evitadas al modelo sin grupo de comparación?



## 46 · Interpretación, equidad y trazabilidad

Interpretación, equidad y trazabilidad

Inspeccionar errores por segmentos pertinentes

Documentar datos, versiones, semillas y política

Monitorear drift y resultados después de adoptar



¿Qué información permitiría reproducir una decisión tomada hoy?



## 47 · Mapa de arquitecturas

Mapa de arquitecturas

MLP: combinaciones de atributos

CNN: patrones locales en grillas

RNN/LSTM: estado temporal; Transformer: atención



¿Qué criterio manda al elegir una arquitectura?



## 48 · Actividad: defensa de una política

Actividad: defensa de una política

Grupos: elegir baseline y MLP para churn mensual

Justificar split, métrica y umbral

Presentar una limitación y una condición de rechazo



¿Adoptarían una red con mayor AUC y menor utilidad de validación?



## 49 · Comprobación de comprensión

Comprobación de comprensión

1. ¿Cuántos parámetros tiene 2→3→1?

2. ¿Por qué una neurona no resuelve XOR?

3. ¿Puede una mejor BCE asegurar más retención?



¿Qué concepto une los tres problemas?



## 50 · Material para continuar

Material para continuar

Lectura: Deep Learning, capítulos 6, 7 y 8

Videos: intuición, gradiente y backpropagation

Práctica: notebook y laboratorios reproducibles



¿Qué experimento harías antes de usar datos reales?



## 51 · Cierre: evidencia para decidir

Cierre: evidencia para decidir

Una red compone funciones y aprende parámetros

Backprop calcula gradientes; el optimizador actualiza

La adopción exige utilidad y generalización verificadas



¿Qué dato falta para pasar de riesgo a retención incremental?