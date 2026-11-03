# Secuencias, RNN y LSTM



## 01 · Secuencias, RNN y LSTM

Secuencias, RNN y LSTM

Ampliación de Ciencias de Datos II · UCA

Memoria, gradientes y predicción temporal

Sergio Gevatschnaider



¿Cuándo puede importar el orden?



## 02 · El orden puede contener información

El orden puede contener información

Tabular: atributos de una unidad

Secuencial: observaciones indexadas por tiempo o posición

Ejemplo: misma venta actual, historial creciente o decreciente



¿Podemos modelar una serie con un árbol?



## 03 · Ventanas para predecir demanda

Ventanas para predecir demanda

Ventana de entrada: cuatro semanas observadas

Objetivo: la semana siguiente

La ventana se construye desde una fecha de origen

Xₜ=[yₜ₋₃,yₜ₋₂,yₜ₋₁,yₜ]
Objetivo=yₜ₊₁

¿La venta de t+1 puede estar en Xₜ?



## 04 · Formas de entrada y salida

Formas de entrada y salida

Muchos a uno: pronóstico de la siguiente semana

Muchos a muchos: etiquetado por paso

Máscaras permiten longitudes diferentes en un batch



¿Qué representa la dimensión temporal de una ventana?



## 05 · La recurrencia transporta un estado

La recurrencia transporta un estado

El estado anterior y la entrada actual producen hₜ

La salida puede leerse en cada paso o al final

Los pesos se comparten en el tiempo

hₜ=tanh(Wₓxₜ+Wₕhₜ₋₁+b)
ŷₜ=Wᵧhₜ+bᵧ

¿Aumentar de 10 a 20 pasos duplica parámetros?



## 06 · RNN desplegada en el tiempo

RNN desplegada en el tiempo

Una celda se aplica sucesivamente

El dibujo desplegado muestra dependencias

Cada copia usa exactamente Wₓ, Wₕ y b



¿Qué pasaría si cada paso tuviera pesos distintos?



## 07 · Parámetros de una RNN

Parámetros de una RNN

d atributos, m unidades ocultas y una salida

Wₓ es m×d y Wₕ es m×m

Usamos un único sesgo oculto en esta convención

P_oculta = md+m²+m
d=2,m=3: 6+9+3=18
P_salida=3+1, total=22

¿Por qué aparece m²?



## 08 · Forward de una RNN escalar

Forward de una RNN escalar

h₀=0, Wₓ=1, Wₕ=0,5 y b=0

Entradas: x₁=1, x₂=0

Los estados cambian aunque la segunda entrada sea cero

h₁=tanh(1)=0,761594
h₂=tanh(0,5·h₁)=0,363399

¿Cuánto vale h₂ si Wₕ=0?



## 09 · Pérdida sobre una secuencia

Pérdida sobre una secuencia

Puede evaluarse en todos los pasos observados

También puede usarse solo la salida final

El enmascarado evita puntuar padding

L = Σₜ ℓ(ŷₜ,yₜ)

¿Dos pérdidas con igual mínimo pueden generar pasos distintos?



## 10 · BPTT aplica la regla de la cadena

BPTT aplica la regla de la cadena

Primero se despliega la secuencia

Luego se propagan gradientes hacia el pasado

Los usos repetidos de un peso suman contribuciones

∂L/∂Wₕ = Σₜ contribución del paso t

¿BPTT necesita un optimizador especial?



## 11 · Productos temporales de Jacobianos

Productos temporales de Jacobianos

Cada paso multiplica por una matriz local

Sus efectos pueden contraerse o amplificarse

Importan activación, pesos y trayectoria

Jₜ=diag(1−hₜ²)Wₕ
∂hₜ/∂hₜ₋ₖ = JₜJₜ₋₁…Jₜ₋ₖ₊₁

¿Por qué tanh saturada puede dificultar el aprendizaje?



## 12 · Vanishing y exploding gradients

Vanishing y exploding gradients

Ejemplo escalar con sensibilidad constante

0,5 por paso atenúa la señal

1,5 por paso puede amplificarla

0,5²⁰ ≈ 0,000000954
1,5²⁰ ≈ 3.325,26

¿Una dependencia larga exige siempre recordar literalmente cada dato?



## 13 · Clipping y BPTT truncada

Clipping y BPTT truncada

Clipping limita la norma de gradientes grandes

Truncar reduce el horizonte del grafo de derivadas

Mantener estado no equivale a mantener todos los gradientes

g_clip = g·min(1,τ/‖g‖)

¿Truncar a 20 pasos permite atribuir directamente una pérdida a 100 pasos atrás?



## 14 · LSTM agrega memoria controlada

LSTM agrega memoria controlada

cₜ: estado de celda

hₜ: estado oculto expuesto

Gates regulan conservación, escritura y salida

cₜ=fₜ⊙cₜ₋₁+iₜ⊙gₜ
hₜ=oₜ⊙tanh(cₜ)

¿Por qué se necesitan c y h?



## 15 · Compuerta de olvido

Compuerta de olvido

Concatena entrada actual y estado oculto previo

La sigmoide produce valores entre 0 y 1

Cada componente escala una memoria previa

uₜ=[hₜ₋₁;xₜ]
fₜ=σ(W_f uₜ+b_f)

¿Qué implica fₜ=0 en una componente?



## 16 · Entrada y contenido candidato

Entrada y contenido candidato

iₜ decide cuánto escribir por componente

gₜ propone contenido con signo

Una misma i puede introducir valores positivos o negativos

iₜ=σ(W_i uₜ+b_i)
gₜ=tanh(W_g uₜ+b_g)

¿Abrir i siempre aumenta c?



## 17 · Actualización aditiva de la celda

Actualización aditiva de la celda

Una rama conserva el pasado

Otra agrega nueva información

c puede superar el intervalo (−1,1)

cₜ=fₜ⊙cₜ₋₁+iₜ⊙gₜ

¿Puede c=2 aunque g esté entre −1 y 1?



## 18 · Compuerta de salida y estado oculto

Compuerta de salida y estado oculto

o controla la exposición de la memoria

tanh acota lo que se expone

Memoria presente puede permanecer poco visible

oₜ=σ(W_o uₜ+b_o)
hₜ=oₜ⊙tanh(cₜ)

¿o=0 obliga a c=0?



## 19 · LSTM: ecuaciones completas

LSTM: ecuaciones completas

Una única convención para u=[h anterior;x]

Sigmoide para f, i y o

tanh para g y para la exposición de c

f=σ(W_fu+b_f)    i=σ(W_iu+b_i)
g=tanh(W_gu+b_g)    o=σ(W_ou+b_o)
c=f⊙c_anterior+i⊙g    h=o⊙tanh(c)

¿Cuáles son los parámetros entrenables?



## 20 · Ejemplo: conservar y escribir

Ejemplo: conservar y escribir

cₜ₋₁=0,8; f=0,9; i=0,2; g=−0,5

Memoria conservada: 0,72

Escritura: −0,10

cₜ=0,9·0,8+0,2·(−0,5)=0,62

¿Cuánto vale cₜ si i=0?



## 21 · Ejemplo: exponer la memoria

Ejemplo: exponer la memoria

Usamos cₜ=0,62 y o=0,75

tanh(0,62)≈0,551128

h queda menor que c y acotado por o

hₜ=0,75·tanh(0,62)≈0,413346

¿Qué memoria ve la capa de salida si o baja?



## 22 · Persistencia con gates constantes

Persistencia con gates constantes

Impulso inicial con i=0,5 y g₁=1

Después no entra contenido: gₜ=0

f controla la velocidad de decaimiento

cₜ = 0,5·fᵗ⁻¹
f=0,9: vida media ≈6,58 pasos

¿Qué sucede si f=1 y no llega más contenido?



## 23 · Qué dice el gradiente directo

Qué dice el gradiente directo

Manteniendo gates fijos, la derivada directa es fₜ

Varios pasos multiplican esas compuertas

La derivada total incluye rutas adicionales por los gates

∂cₜ/∂cₜ₋₁ (gates fijos)=fₜ

¿LSTM elimina todo vanishing gradient?



## 24 · Laboratorio: retener, alternar, sobrescribir

Laboratorio: retener, alternar, sobrescribir

Impulso: observar memoria sin nueva escritura

Alternancia: contenido con cambios de signo

Sobrescritura: nueva señal tras varios pasos



¿Qué diferencia observás al cerrar o en vez de cerrar f?



## 25 · Conteo de parámetros LSTM

Conteo de parámetros LSTM

Cuatro transformaciones sobre d+m entradas

m salidas por transformación

Más parámetros permiten control, pero aumentan costo

P_celda = 4m(d+m+1)
d=2,m=3: P=4·3·6=72

¿La longitud de la secuencia aparece en P?



## 26 · GRU: una alternativa con menos compuertas

GRU: una alternativa con menos compuertas

Combina memoria y estado oculto

Usa gates de actualización y reinicio

La convención de z debe quedar explícita

z=σ(W_zx+U_zh_prev+b_z)
r=σ(W_rx+U_rh_prev+b_r)
h̃=tanh(Wx+U(r⊙h_prev)+b)
h=(1−z)⊙h_prev+z⊙h̃

¿Qué conserva el pasado en esta convención?



## 27 · RNN, LSTM/GRU y Transformer

RNN, LSTM/GRU y Transformer

RNN: estado recurrente y transición simple

LSTM/GRU: gates y recurrencia secuencial

Transformer: atención con información de posición



¿La atención recibe el orden temporal sin posición ni máscara?



## 28 · Costo y paralelización dependen del uso

Costo y paralelización dependen del uso

RNN: O(Tm²) para recurrencia d≈m

Atención densa: O(T²m) más proyecciones

Inferencia autoregresiva conserva pasos secuenciales

T: longitud de secuencia
m: dimensión del estado

¿Una menor complejidad asintótica garantiza menos latencia para T pequeño?



## 29 · Partición cronológica para demanda

Partición cronológica para demanda

Entrenar con el pasado disponible

Elegir configuración en un período posterior

Reservar el último bloque como test final



¿Una ventana test puede contener valores de train?



## 30 · Walk-forward

Walk-forward

Cada origen simula una decisión real

Entrenamiento expansivo o ventana móvil

Comparación de modelos sobre los mismos orígenes



¿Por qué un split aleatorio puede sobreestimar calidad temporal?



## 31 · Baseline ingenuo y estacional

Baseline ingenuo y estacional

Ingenuo: repetir el último dato

Estacional: repetir el mismo período del ciclo previo

Calendario y rezagos también alimentan modelos simples

Naive: ŷₜ₊₁=yₜ
Estacional, período s: ŷₜ₊₁=yₜ₊₁₋ₛ

¿Qué baseline exigirías para demanda diaria con patrón semanal?



## 32 · MAE, RMSE y límites de MAPE

MAE, RMSE y límites de MAPE

MAE conserva unidades e interpreta error absoluto

RMSE penaliza más errores grandes

MAPE falla con ceros y distorsiona valores pequeños

MAE=mean(|e|)    RMSE=√mean(e²)
MAPE=100·mean(|e/y|)

¿Cómo reportarías MAPE si hay y=0?



## 33 · Práctica reproducible en Python

Práctica reproducible en Python

Crear ventanas y separar por fecha

Ajustar baseline estacional, modelo con rezagos y LSTM

Medir MAE/RMSE sobre idénticos orígenes



¿Qué entregar además del score?



## 34 · Defensa final y respuestas

Defensa final y respuestas

Si f=1 e i=0, c se conserva

Clipping limita explosión, sin recuperar gradientes nulos

Una LSTM debe superar un baseline con evidencia temporal



¿Adoptarías LSTM si la mejora media es pequeña y varía de signo por período?