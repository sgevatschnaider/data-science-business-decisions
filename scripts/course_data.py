"""Fuente única de contenidos para el curso.

El generador usa estas estructuras para producir el sitio, los README de cada
módulo, los glosarios y los cuestionarios. Mantener el contenido aquí evita
divergencias entre recursos.
"""

COURSE = {
    "title": "Ciencia de Datos para Decisiones de Negocio",
    "short_title": "Datos y Decisiones",
    "repository": "data-science-business-decisions",
    "owner": "sgevatschnaider",
    "author": "Sergio Gevatschnaider",
    "description": (
        "Curso aplicado de ciencia de datos, machine learning e inteligencia "
        "artificial orientado a convertir problemas de negocio en decisiones "
        "medibles, reproducibles y responsables."
    ),
}


UNITS = [
    {
        "id": "unidad-1",
        "number": "I",
        "title": "Fundamentos y calidad de datos",
        "modules": ["00", "01", "02", "03", "04"],
        "question": "¿Podemos convertir datos crudos en evidencia confiable?",
    },
    {
        "id": "unidad-2",
        "number": "II",
        "title": "Modelos predictivos y evaluación",
        "modules": ["05", "06", "07", "08", "09"],
        "question": "¿Cómo predecimos y validamos sin engañarnos?",
    },
    {
        "id": "unidad-3",
        "number": "III",
        "title": "Aprendizaje no supervisado e inteligencia artificial",
        "modules": ["10", "11"],
        "question": "¿Qué estructuras y representaciones puede aprender un modelo?",
    },
    {
        "id": "unidad-4",
        "number": "IV",
        "title": "Decisión, optimización y responsabilidad",
        "modules": ["12", "13"],
        "question": "¿Cómo transformamos predicciones en acciones defendibles?",
    },
    {
        "id": "unidad-5",
        "number": "V",
        "title": "Proyecto integrador",
        "modules": ["14"],
        "question": "¿Podemos sostener una recomendación de punta a punta?",
    },
]


def q(question, options, answer, explanation):
    return {
        "question": question,
        "options": options,
        "answer": answer,
        "explanation": explanation,
    }


MODULES = [
    {
        "id": "00",
        "slug": "00-orientacion-python",
        "unit": "I",
        "title": "Orientación, Python y flujo de trabajo",
        "short_title": "Orientación y Python",
        "summary": (
            "Del problema ambiguo al experimento reproducible: entorno, "
            "notebooks, datos, código y evidencia."
        ),
        "business_question": (
            "¿Qué condiciones mínimas debe cumplir un análisis para que otra "
            "persona pueda comprenderlo, ejecutarlo y auditarlo?"
        ),
        "duration": "2 encuentros más práctica asincrónica",
        "prerequisites": "Ninguno",
        "objectives": [
            "Traducir una necesidad de negocio a una pregunta analítica verificable.",
            "Usar notebooks sin perder trazabilidad entre narrativa, código y resultados.",
            "Manipular estructuras básicas de Python, NumPy y pandas.",
            "Organizar un proyecto reproducible con datos, código, documentación y Git.",
        ],
        "theory": [
            {
                "title": "De la inquietud a la pregunta",
                "text": (
                    "Una frase como «queremos vender más» no define todavía un "
                    "problema analítico. Se necesita una unidad de análisis, una "
                    "población, un horizonte, una decisión y una métrica de éxito."
                ),
            },
            {
                "title": "Notebook como argumento",
                "text": (
                    "Un notebook útil intercala propósito, supuestos, código, "
                    "resultados y conclusión. El orden de ejecución debe ser "
                    "lineal y cada salida tiene que poder regenerarse."
                ),
            },
            {
                "title": "Ecosistema mínimo",
                "text": (
                    "Python aporta el lenguaje; NumPy, cálculo vectorizado; pandas, "
                    "datos tabulares; Matplotlib y Seaborn, comunicación visual; "
                    "scikit-learn, una interfaz coherente para modelar."
                ),
            },
            {
                "title": "Reproducibilidad práctica",
                "text": (
                    "Semillas aleatorias, dependencias explícitas, rutas relativas, "
                    "diccionario de datos y control de versiones convierten un "
                    "resultado aislado en un activo reutilizable."
                ),
            },
        ],
        "case": (
            "Una gerencia solicita identificar clientes con riesgo de abandono. "
            "Antes de modelar, el equipo debe fijar qué significa abandonar, cuál "
            "es la ventana de observación y qué acción se tomará con el resultado."
        ),
        "deliverable": (
            "Notebook ejecutable con pregunta, unidad de análisis, métrica, "
            "diccionario mínimo y una primera tabla de control."
        ),
        "lab_steps": [
            "Abrir el notebook en Colab o Jupyter y ejecutar todo desde cero.",
            "Crear una tabla pequeña con listas, diccionarios y un DataFrame.",
            "Validar tipos, dimensiones y valores únicos.",
            "Documentar una pregunta de negocio y el criterio de éxito.",
        ],
        "simulation_title": "Constructor de un flujo reproducible",
        "simulation_instruction": (
            "Ordená las etapas, modificá la semilla y observá qué elementos "
            "permiten reconstruir exactamente un resultado."
        ),
        "glossary": [
            ("Unidad de análisis", "Entidad elemental sobre la que se mide, predice o decide."),
            ("Variable", "Atributo observado o calculado para cada unidad de análisis."),
            ("Métrica de éxito", "Medida acordada para evaluar si una intervención crea valor."),
            ("Notebook", "Documento ejecutable que combina texto, código y resultados."),
            ("DataFrame", "Estructura tabular etiquetada provista por pandas."),
            ("Vectorización", "Operación sobre colecciones completas sin bucles explícitos."),
            ("Semilla aleatoria", "Valor que permite repetir una secuencia pseudoaleatoria."),
            ("Dependencia", "Biblioteca externa requerida para ejecutar un proyecto."),
            ("Control de versiones", "Registro trazable de cambios en archivos y código."),
            ("Reproducibilidad", "Capacidad de regenerar un resultado con los mismos insumos."),
        ],
        "quiz": [
            q(
                "¿Cuál de estas preguntas está mejor formulada para un análisis?",
                [
                    "¿Cómo vendemos más?",
                    "¿Qué clientes abandonarán?",
                    "¿Qué clientes activos al cierre del mes tienen mayor riesgo de cancelar en los próximos 30 días?",
                    "¿Podemos usar inteligencia artificial?",
                ],
                2,
                "Define población, momento de observación, evento y horizonte.",
            ),
            q(
                "¿Qué práctica favorece la reproducibilidad?",
                [
                    "Editar manualmente los resultados",
                    "Fijar semillas y declarar dependencias",
                    "Ejecutar celdas en cualquier orden",
                    "Guardar solo capturas de pantalla",
                ],
                1,
                "La semilla y el entorno declarado permiten repetir el proceso.",
            ),
            q(
                "¿Qué representa una fila en una tabla analítica?",
                [
                    "Siempre una persona",
                    "La unidad de análisis definida",
                    "Una variable",
                    "Una visualización",
                ],
                1,
                "La interpretación de cada fila depende de la unidad de análisis.",
            ),
            q(
                "¿Por qué conviene ejecutar un notebook de principio a fin?",
                [
                    "Para aumentar el tamaño del archivo",
                    "Para comprobar que no depende de estados ocultos",
                    "Para cambiar los gráficos",
                    "Para evitar documentar",
                ],
                1,
                "Una ejecución lineal detecta variables o resultados creados fuera de orden.",
            ),
            q(
                "¿Qué elemento conecta el análisis con una decisión?",
                [
                    "La cantidad de librerías",
                    "La métrica de éxito",
                    "El color del gráfico",
                    "El número de celdas",
                ],
                1,
                "La métrica explicita cómo se juzga el valor de la recomendación.",
            ),
            q(
                "¿Qué archivo ayuda a interpretar correctamente las columnas?",
                [
                    "Diccionario de datos",
                    "Captura de pantalla",
                    "Archivo temporal",
                    "Historial del navegador",
                ],
                0,
                "El diccionario registra significado, tipo, unidad y reglas relevantes.",
            ),
        ],
    },
    {
        "id": "01",
        "slug": "01-eda-negocio",
        "unit": "I",
        "title": "Problema de negocio, EDA y visualización",
        "short_title": "EDA y visualización",
        "summary": (
            "Explorar con propósito: estructura, distribuciones, relaciones, "
            "segmentos y visualizaciones que respondan preguntas."
        ),
        "business_question": (
            "¿Qué patrones, anomalías y límites de los datos debemos comprender "
            "antes de proponer una explicación o un modelo?"
        ),
        "duration": "2 encuentros",
        "prerequisites": "Módulo 00",
        "objectives": [
            "Construir un perfil estructural y estadístico de un conjunto de datos.",
            "Elegir visualizaciones según variable, audiencia y pregunta.",
            "Comparar segmentos sin confundir asociación con causalidad.",
            "Cerrar el EDA con hallazgos, riesgos y próximos análisis.",
        ],
        "theory": [
            {
                "title": "Exploración guiada por decisiones",
                "text": (
                    "El EDA no es una galería de gráficos. Cada cálculo debe reducir "
                    "una incertidumbre: cobertura, distribución, relación, segmento "
                    "o anomalía relevante para la decisión."
                ),
            },
            {
                "title": "Distribución y escala",
                "text": (
                    "Media, mediana, cuantiles, dispersión, asimetría y colas cuentan "
                    "historias distintas. Resumir sin observar la forma puede ocultar "
                    "subpoblaciones o eventos extremos."
                ),
            },
            {
                "title": "Relaciones y segmentación",
                "text": (
                    "Tablas cruzadas, facetas y gráficos bivariados permiten comparar "
                    "grupos. Las diferencias observadas son asociaciones descriptivas "
                    "hasta que un diseño causal justifique otra interpretación."
                ),
            },
            {
                "title": "Comunicación visual",
                "text": (
                    "Un gráfico debe tener una pregunta, una jerarquía visual y una "
                    "conclusión legible. La precisión importa más que la decoración."
                ),
            },
        ],
        "case": (
            "Una cadena minorista analiza ticket, frecuencia, canal y región para "
            "decidir dónde concentrar una campaña de fidelización."
        ),
        "deliverable": (
            "Informe breve con perfil de datos, cuatro visualizaciones justificadas, "
            "tres hallazgos y dos limitaciones."
        ),
        "lab_steps": [
            "Auditar dimensiones, tipos, claves y cardinalidades.",
            "Resumir variables numéricas y categóricas con medidas pertinentes.",
            "Comparar al menos dos segmentos del negocio.",
            "Redactar títulos de gráficos que expresen el hallazgo.",
        ],
        "simulation_title": "Laboratorio de distribuciones",
        "simulation_instruction": (
            "Modificá asimetría, dispersión y observaciones extremas; compará cómo "
            "reaccionan la media, la mediana y el histograma."
        ),
        "glossary": [
            ("EDA", "Proceso iterativo de comprender estructura, calidad, patrones y anomalías."),
            ("Distribución", "Forma en que se reparten los valores de una variable."),
            ("Media", "Promedio aritmético, sensible a valores extremos."),
            ("Mediana", "Valor central de los datos ordenados, robusto frente a extremos."),
            ("Cuantil", "Punto que divide una distribución según una proporción acumulada."),
            ("Dispersión", "Grado de variabilidad de los valores."),
            ("Asimetría", "Falta de simetría en la forma de una distribución."),
            ("Cardinalidad", "Cantidad de valores distintos de una variable."),
            ("Faceta", "Subgráfico que replica una visualización para diferentes grupos."),
            ("Asociación", "Relación estadística que no implica necesariamente causalidad."),
        ],
        "quiz": [
            q(
                "Si una variable tiene una cola derecha pronunciada, ¿qué suele ocurrir?",
                ["La media queda debajo de la mediana", "La media supera a la mediana", "Ambas siempre son cero", "No existe dispersión"],
                1,
                "Los valores altos de la cola desplazan la media más que la mediana.",
            ),
            q(
                "¿Qué gráfico es apropiado para estudiar la distribución de una variable continua?",
                ["Histograma", "Gráfico de torta con cien categorías", "Mapa sin geografía", "Diagrama de flujo"],
                0,
                "El histograma representa frecuencias a lo largo de intervalos.",
            ),
            q(
                "¿Qué debería orientar la selección de una visualización?",
                ["La pregunta y el tipo de variable", "La mayor cantidad de colores", "La plantilla disponible", "El gráfico más complejo"],
                0,
                "La forma visual debe responder a la tarea analítica.",
            ),
            q(
                "Una asociación fuerte entre descuento y ventas demuestra que el descuento causó las ventas.",
                ["Siempre", "Solo si la correlación es positiva", "No; se necesita un diseño causal", "Sí, si hay muchas filas"],
                2,
                "Confusores y selección pueden generar asociaciones sin efecto causal.",
            ),
            q(
                "¿Qué cierre es más útil para un EDA?",
                ["Una lista de funciones usadas", "Hallazgos, riesgos y próximos pasos", "Solo el número de filas", "Todos los gráficos sin interpretación"],
                1,
                "El cierre conecta evidencia, incertidumbre y decisión.",
            ),
            q(
                "¿Qué medida es más robusta ante un valor extremadamente alto?",
                ["Media", "Mediana", "Rango", "Varianza"],
                1,
                "La posición central cambia poco cuando se modifica un extremo.",
            ),
        ],
    },
    {
        "id": "02",
        "slug": "02-calidad-datos",
        "unit": "I",
        "title": "Calidad de datos y valores faltantes",
        "short_title": "Calidad y faltantes",
        "summary": (
            "Diagnosticar completitud, validez, consistencia, duplicados y "
            "mecanismos de ausencia antes de imputar."
        ),
        "business_question": (
            "¿La evidencia disponible representa el proceso real o sus defectos "
            "pueden cambiar la conclusión y perjudicar la decisión?"
        ),
        "duration": "2 encuentros",
        "prerequisites": "Módulos 00 y 01",
        "objectives": [
            "Definir pruebas de calidad alineadas con reglas de negocio.",
            "Distinguir ausencia MCAR, MAR y MNAR como hipótesis de trabajo.",
            "Comparar eliminación, imputación simple y estrategias multivariadas.",
            "Documentar impacto, trazabilidad e indicadores de ausencia.",
        ],
        "theory": [
            {
                "title": "Calidad multidimensional",
                "text": (
                    "Completitud no equivale a calidad. También importan unicidad, "
                    "validez, consistencia temporal, exactitud, oportunidad y "
                    "coherencia con reglas del negocio."
                ),
            },
            {
                "title": "El patrón importa",
                "text": (
                    "La ausencia completamente aleatoria, condicionada por variables "
                    "observadas o relacionada con el valor no observado requiere "
                    "supuestos y tratamientos diferentes."
                ),
            },
            {
                "title": "Imputar es modelar",
                "text": (
                    "Reemplazar por media o moda altera varianza y relaciones. La "
                    "estrategia debe estimarse dentro del conjunto de entrenamiento "
                    "y evaluarse por su efecto en la tarea final."
                ),
            },
            {
                "title": "Trazabilidad",
                "text": (
                    "Conservar indicadores de ausencia, reglas y conteos antes y "
                    "después permite auditar cuánto dependió el resultado de una "
                    "decisión de limpieza."
                ),
            },
        ],
        "case": (
            "En una solicitud de crédito faltan ingresos con mayor frecuencia en "
            "trabajadores independientes. Imputar sin segmentar puede ocultar una "
            "diferencia estructural."
        ),
        "deliverable": (
            "Reporte de calidad con reglas automatizadas, mapa de faltantes, hipótesis "
            "del mecanismo y comparación de dos estrategias."
        ),
        "lab_steps": [
            "Definir clave, rangos y reglas de consistencia.",
            "Medir faltantes por variable y por segmento.",
            "Crear indicadores de ausencia antes de imputar.",
            "Comparar distribución y métrica posterior a cada tratamiento.",
        ],
        "simulation_title": "Laboratorio de faltantes e imputación",
        "simulation_instruction": (
            "Controlá el porcentaje y el mecanismo de ausencia; compará sesgo y "
            "dispersión después de eliminar o imputar."
        ),
        "glossary": [
            ("Completitud", "Proporción de datos requeridos que están presentes."),
            ("Validez", "Cumplimiento de formato, dominio y reglas permitidas."),
            ("Consistencia", "Ausencia de contradicciones entre campos, tablas o tiempos."),
            ("Duplicado", "Registro repetido según una clave y una definición operacional."),
            ("MCAR", "Ausencia independiente de valores observados y no observados."),
            ("MAR", "Ausencia explicable condicionalmente por variables observadas."),
            ("MNAR", "Ausencia relacionada con el propio valor no observado u otra causa no medida."),
            ("Imputación", "Estimación de valores ausentes bajo supuestos explícitos."),
            ("Indicador de ausencia", "Variable binaria que conserva el hecho de que faltaba un dato."),
            ("Leakage", "Uso de información que no estaría disponible al momento de predecir."),
        ],
        "quiz": [
            q(
                "¿Por qué imputar con la media puede ser problemático?",
                ["Aumenta siempre la varianza", "Puede reducir artificialmente la variabilidad", "Elimina todas las filas", "Convierte números en texto"],
                1,
                "Repetir un mismo valor concentra la distribución y distorsiona relaciones.",
            ),
            q(
                "Si los ingresos faltan más entre independientes y la ocupación está observada, ¿qué mecanismo es plausible?",
                ["MCAR necesariamente", "MAR como hipótesis", "No hay faltantes", "Duplicación"],
                1,
                "La ausencia podría explicarse por una variable observada.",
            ),
            q(
                "¿Dónde debe ajustarse un imputador en un flujo predictivo?",
                ["Con todo el dataset antes de dividir", "Solo con entrenamiento", "Solo con test", "Después de publicar el modelo"],
                1,
                "Ajustarlo con test filtraría información hacia el entrenamiento.",
            ),
            q(
                "¿Qué prueba detecta mejor una edad imposible?",
                ["Regla de rango", "Conteo de columnas", "Cambio de color", "Orden alfabético"],
                0,
                "La validez puede formalizarse con límites permitidos.",
            ),
            q(
                "¿Cuándo son duplicados dos registros?",
                ["Cuando tienen el mismo color", "Según una clave y criterio de negocio", "Cuando están consecutivos", "Siempre que comparten un valor"],
                1,
                "La duplicación depende de la entidad y evento representados.",
            ),
            q(
                "¿Qué aporta un indicador de ausencia?",
                ["Recupera el valor real", "Conserva una posible señal del proceso de captura", "Evita validar", "Garantiza causalidad"],
                1,
                "El hecho de faltar puede contener información útil y auditable.",
            ),
        ],
    },
    {
        "id": "03",
        "slug": "03-outliers",
        "unit": "I",
        "title": "Outliers, robustez e influencia",
        "short_title": "Outliers y robustez",
        "summary": (
            "Separar errores, rarezas válidas y observaciones influyentes con "
            "criterios estadísticos y de negocio."
        ),
        "business_question": (
            "¿Una observación extrema es un error, un evento valioso o una señal "
            "de que el proceso cambió?"
        ),
        "duration": "2 encuentros",
        "prerequisites": "Módulos 01 y 02",
        "objectives": [
            "Detectar extremos con IQR, puntuación z y criterios multivariados.",
            "Diferenciar outlier, alta palanca e influencia sobre un modelo.",
            "Aplicar estadísticas robustas y análisis de sensibilidad.",
            "Justificar conservar, corregir, transformar, limitar o excluir.",
        ],
        "theory": [
            {
                "title": "Extremo no significa error",
                "text": (
                    "Un valor puede ser raro y legítimo, imposible por una regla o "
                    "resultado de otro régimen. El diagnóstico estadístico inicia "
                    "la investigación; el contexto decide el tratamiento."
                ),
            },
            {
                "title": "Detección univariada",
                "text": (
                    "El rango intercuartílico resiste colas; la puntuación z supone "
                    "que media y desvío son representativos. Ningún umbral reemplaza "
                    "la inspección de unidades y procesos."
                ),
            },
            {
                "title": "Influencia",
                "text": (
                    "Una observación influyente cambia sustancialmente parámetros o "
                    "predicciones. Combina residuo, posición en el espacio de variables "
                    "y sensibilidad del estimador."
                ),
            },
            {
                "title": "Decisiones robustas",
                "text": (
                    "Medianas, pérdidas robustas, transformaciones y análisis con y "
                    "sin casos extremos permiten comunicar cuánto depende la conclusión "
                    "de unas pocas observaciones."
                ),
            },
        ],
        "case": (
            "Una venta corporativa multiplica por veinte el ticket habitual. Borrarla "
            "mejora un promedio, pero elimina el segmento de mayor valor."
        ),
        "deliverable": (
            "Bitácora de observaciones extremas con evidencia, decisión de tratamiento "
            "y comparación de conclusiones antes y después."
        ),
        "lab_steps": [
            "Verificar unidades, reglas y procedencia de extremos.",
            "Comparar IQR, puntuación z y percentiles.",
            "Medir cambios en estadísticas y modelos.",
            "Registrar cada decisión de tratamiento.",
        ],
        "simulation_title": "Detector de extremos e influencia",
        "simulation_instruction": (
            "Cambiá el método y el umbral; mové una observación y observá cómo "
            "varían la clasificación, la media y la recta ajustada."
        ),
        "glossary": [
            ("Outlier", "Observación inusual respecto de un patrón o distribución de referencia."),
            ("IQR", "Diferencia entre tercer y primer cuartil; medida robusta de dispersión."),
            ("Puntuación z", "Distancia a la media expresada en desvíos estándar."),
            ("Estadística robusta", "Estimador poco sensible a desviaciones o valores extremos."),
            ("Winsorización", "Limitación de valores a umbrales seleccionados sin eliminar filas."),
            ("Palanca", "Grado de excepcionalidad de una observación en el espacio de predictores."),
            ("Residuo", "Diferencia entre valor observado y estimado por un modelo."),
            ("Influencia", "Capacidad de una observación de modificar el ajuste."),
            ("Distancia de Cook", "Resumen de influencia de una observación en regresión."),
            ("Análisis de sensibilidad", "Comparación de resultados bajo supuestos o tratamientos alternativos."),
        ],
        "quiz": [
            q(
                "Un ticket muy alto pero verificado debe eliminarse automáticamente.",
                ["Sí", "No; puede representar un segmento real", "Sí, si supera la media", "Solo por su color"],
                1,
                "La rareza estadística no demuestra un error.",
            ),
            q(
                "¿Qué medida es más robusta ante extremos?",
                ["Media", "Desvío estándar", "Mediana", "Rango"],
                2,
                "La mediana depende del orden y no de la magnitud extrema.",
            ),
            q(
                "¿Qué combina una observación influyente?",
                ["Solo gran residuo", "Residuo, palanca y sensibilidad", "Solo una categoría rara", "Únicamente tamaño muestral"],
                1,
                "La influencia depende de error, posición y efecto sobre el estimador.",
            ),
            q(
                "¿Qué aporta comparar resultados con y sin extremos?",
                ["Una prueba de causalidad", "Un análisis de sensibilidad", "Una nueva variable objetivo", "La eliminación de sesgo garantizada"],
                1,
                "Muestra cuánto depende la conclusión de esas observaciones.",
            ),
            q(
                "¿Qué supuesto hace delicada la puntuación z en distribuciones muy asimétricas?",
                ["Media y desvío representan bien el centro y escala", "No existen números", "Todos los valores son categorías", "La muestra está ordenada"],
                0,
                "Ambos estimadores son sensibles a colas y extremos.",
            ),
            q(
                "Antes de tratar un outlier conviene revisar:",
                ["Unidades y proceso de generación", "Solo el nombre del archivo", "El fondo del gráfico", "La longitud del código"],
                0,
                "Muchos extremos provienen de errores de unidad o de regímenes distintos.",
            ),
        ],
    },
    {
        "id": "04",
        "slug": "04-transformacion-pipelines",
        "unit": "I",
        "title": "Transformación de variables y pipelines",
        "short_title": "Transformación y pipelines",
        "summary": (
            "Transformar, escalar, codificar y construir variables sin filtrar "
            "información ni romper la reproducibilidad."
        ),
        "business_question": (
            "¿Cómo representamos los datos para que un modelo aprenda el patrón "
            "correcto y pueda repetirse exactamente en producción?"
        ),
        "duration": "2 encuentros",
        "prerequisites": "Módulos 00 a 03",
        "objectives": [
            "Elegir transformaciones según distribución, relación y algoritmo.",
            "Codificar categorías y escalar variables de forma segura.",
            "Crear variables con disponibilidad temporal explícita.",
            "Encapsular preparación y estimación en pipelines.",
        ],
        "theory": [
            {
                "title": "Transformar con hipótesis",
                "text": (
                    "Logaritmos, raíces y potencias pueden estabilizar varianza o "
                    "linealizar relaciones. La transformación debe responder a una "
                    "razón analítica y conservar una interpretación posible."
                ),
            },
            {
                "title": "Escalado y codificación",
                "text": (
                    "Distancias y regularización son sensibles a escala; los árboles, "
                    "mucho menos. One-hot evita imponer orden a categorías nominales, "
                    "mientras una codificación ordinal requiere jerarquía real."
                ),
            },
            {
                "title": "Ingeniería de variables",
                "text": (
                    "Ratios, recencia, frecuencia, interacciones y agregaciones pueden "
                    "acercar el modelo al mecanismo de negocio. Toda variable debe "
                    "existir al momento de la decisión."
                ),
            },
            {
                "title": "Pipeline contra leakage",
                "text": (
                    "Un pipeline aprende imputación, escalado y codificación solo con "
                    "entrenamiento y reaplica los parámetros a validación y test."
                ),
            },
        ],
        "case": (
            "Un modelo de demanda combina precios, categorías y recencia. Calcular "
            "promedios usando meses futuros produce métricas excelentes e inútiles."
        ),
        "deliverable": (
            "Pipeline reproducible con columnas numéricas y categóricas, variables "
            "derivadas documentadas y prueba explícita de no leakage."
        ),
        "lab_steps": [
            "Clasificar variables por tipo y tratamiento.",
            "Comparar escala original, logarítmica y estandarizada.",
            "Construir un ColumnTransformer dentro de un Pipeline.",
            "Verificar disponibilidad temporal de cada feature.",
        ],
        "simulation_title": "Taller de transformaciones y leakage",
        "simulation_instruction": (
            "Elegí transformación, escala y momento de ajuste; observá la forma, "
            "la comparabilidad y el efecto de usar información futura."
        ),
        "glossary": [
            ("Transformación logarítmica", "Cambio de escala que comprime valores altos y requiere dominio válido."),
            ("Estandarización", "Centrado por media y escalado por desvío estándar."),
            ("Min-max", "Reexpresión lineal dentro de un intervalo, habitualmente de cero a uno."),
            ("One-hot encoding", "Representación binaria separada para cada categoría nominal."),
            ("Codificación ordinal", "Asignación numérica que conserva un orden real entre categorías."),
            ("Feature engineering", "Construcción de variables útiles a partir de datos disponibles."),
            ("Interacción", "Variable que representa el efecto conjunto de dos o más factores."),
            ("Pipeline", "Secuencia encapsulada de transformaciones y estimación."),
            ("ColumnTransformer", "Aplicador de transformaciones diferentes por grupos de columnas."),
            ("Leakage temporal", "Uso de información futura para construir una variable o ajustar un proceso."),
        ],
        "quiz": [
            q(
                "¿Qué algoritmo suele ser sensible a la escala por usar distancias?",
                ["K-Means", "Árbol de decisión", "Regla de negocio", "Tabla dinámica"],
                0,
                "Las distancias quedan dominadas por variables con mayor escala.",
            ),
            q(
                "¿Cuándo corresponde una codificación ordinal?",
                ["Cuando las categorías tienen jerarquía real", "Para cualquier texto", "Solo con dos filas", "Nunca"],
                0,
                "Los números asignados implican un orden que debe existir en el dominio.",
            ),
            q(
                "¿Qué evita un pipeline correctamente usado?",
                ["Toda incertidumbre", "Ajustar transformaciones con datos de test", "Necesitar variables", "Definir una métrica"],
                1,
                "El pipeline respeta el ajuste dentro de cada partición de entrenamiento.",
            ),
            q(
                "Una variable de recencia calculada con datos posteriores a la predicción es:",
                ["Una mejora segura", "Leakage temporal", "Una categoría ordinal", "Un residuo"],
                1,
                "La información no estaría disponible cuando se toma la decisión.",
            ),
            q(
                "¿Por qué aplicar logaritmo a una variable positiva muy asimétrica?",
                ["Para comprimir la cola y facilitar ciertas relaciones", "Para crear categorías", "Para eliminar todas las filas", "Para garantizar causalidad"],
                0,
                "El logaritmo reduce diferencias multiplicativas grandes.",
            ),
            q(
                "Los parámetros del escalador deben aprenderse:",
                ["Con entrenamiento", "Con test", "Con todo antes de dividir", "Manualmente mirando el resultado final"],
                0,
                "Así se mantiene la independencia del conjunto de evaluación.",
            ),
        ],
    },
    {
        "id": "05",
        "slug": "05-regresion-lineal",
        "unit": "II",
        "title": "Correlación y regresión lineal",
        "short_title": "Regresión lineal",
        "summary": (
            "Cuantificar relaciones, diagnosticar supuestos y evaluar errores con "
            "una interpretación conectada al negocio."
        ),
        "business_question": (
            "¿Cuánto cambia una variable de interés cuando cambia un predictor y "
            "con qué incertidumbre podemos usar esa relación?"
        ),
        "duration": "2 encuentros",
        "prerequisites": "Módulos 01 y 04",
        "objectives": [
            "Interpretar covarianza, correlación y coeficientes sin afirmar causalidad.",
            "Ajustar regresiones simples y múltiples.",
            "Diagnosticar linealidad, residuos, varianza y colinealidad.",
            "Comparar MAE, MSE, RMSE y R cuadrado según el costo del error.",
        ],
        "theory": [
            {
                "title": "Correlación con límites",
                "text": (
                    "Pearson resume asociación lineal y Spearman asociación monótona. "
                    "Ambas pueden cambiar por outliers, mezcla de grupos o variables "
                    "omitidas; ninguna prueba por sí sola causalidad."
                ),
            },
            {
                "title": "Modelo lineal",
                "text": (
                    "La regresión estima una media condicional como combinación de "
                    "predictores. Cada coeficiente se interpreta manteniendo constantes "
                    "los demás, dentro del rango observado."
                ),
            },
            {
                "title": "Diagnóstico",
                "text": (
                    "Residuos contra predicciones, Q-Q plots, palanca y VIF ayudan a "
                    "detectar no linealidad, heterocedasticidad, colinealidad e "
                    "influencia."
                ),
            },
            {
                "title": "Error y valor",
                "text": (
                    "MAE conserva unidades y es robusto; RMSE penaliza más los errores "
                    "grandes; R cuadrado compara variabilidad explicada. Ninguna métrica "
                    "reemplaza el costo económico."
                ),
            },
        ],
        "case": (
            "Una empresa estima ventas en función de inversión, precio y estacionalidad "
            "para definir presupuesto y rango de incertidumbre."
        ),
        "deliverable": (
            "Modelo lineal con interpretación, diagnóstico de residuos, validación y "
            "traducción de error a una consecuencia operativa."
        ),
        "lab_steps": [
            "Explorar relaciones y posibles grupos.",
            "Ajustar un baseline y una regresión múltiple.",
            "Inspeccionar residuos y observaciones influyentes.",
            "Comparar métricas y comunicar un intervalo.",
        ],
        "simulation_title": "Mesa de regresión, ruido y métricas",
        "simulation_instruction": (
            "Modificá pendiente, intercepto y ruido; observá la recta, los residuos "
            "y cómo responden MAE, RMSE y R cuadrado."
        ),
        "glossary": [
            ("Covarianza", "Medida no estandarizada de variación conjunta."),
            ("Correlación de Pearson", "Asociación lineal estandarizada entre dos variables."),
            ("Correlación de Spearman", "Asociación monótona calculada sobre rangos."),
            ("Coeficiente", "Cambio estimado en la respuesta ante una unidad del predictor, bajo condiciones."),
            ("Intercepto", "Valor estimado cuando los predictores valen cero."),
            ("Residuo", "Diferencia entre observación y predicción."),
            ("Heterocedasticidad", "Varianza no constante de los errores."),
            ("Multicolinealidad", "Dependencia fuerte entre predictores que inestabiliza coeficientes."),
            ("RMSE", "Raíz del promedio de errores cuadrados."),
            ("R cuadrado", "Proporción de variabilidad de la respuesta explicada dentro de la muestra."),
        ],
        "quiz": [
            q(
                "Una correlación alta demuestra causalidad.",
                ["Sí", "No", "Solo con Pearson", "Solo con muchas variables"],
                1,
                "La asociación puede surgir por confusión, selección o coincidencia.",
            ),
            q(
                "¿Qué métrica penaliza con mayor fuerza errores grandes?",
                ["MAE", "RMSE", "Mediana", "Exactitud"],
                1,
                "Elevar al cuadrado aumenta el peso de desviaciones grandes.",
            ),
            q(
                "En regresión múltiple, un coeficiente se interpreta:",
                ["Sin considerar otros predictores", "Manteniendo constantes los demás", "Como causal siempre", "Solo por su signo"],
                1,
                "Es un efecto parcial dentro del modelo especificado.",
            ),
            q(
                "Un patrón curvo en residuos contra predicción sugiere:",
                ["Linealidad perfecta", "No linealidad no capturada", "Ausencia de datos", "Clasificación balanceada"],
                1,
                "Los residuos deberían fluctuar sin estructura sistemática.",
            ),
            q(
                "¿Cuál conserva las unidades de la variable objetivo?",
                ["MSE", "R cuadrado", "RMSE", "Correlación"],
                2,
                "La raíz devuelve la escala original.",
            ),
            q(
                "¿Cuándo es riesgoso interpretar el intercepto?",
                ["Cuando cero está fuera del rango observado", "Cuando hay una sola variable", "Cuando RMSE es positivo", "Siempre que existe media"],
                0,
                "Puede ser una extrapolación sin sentido de negocio.",
            ),
        ],
    },
    {
        "id": "06",
        "slug": "06-validacion-modelos",
        "unit": "II",
        "title": "Validación, selección y generalización",
        "short_title": "Validación de modelos",
        "summary": (
            "Diseñar particiones, baselines y validación cruzada que estimen el "
            "desempeño futuro sin contaminar la evaluación."
        ),
        "business_question": (
            "¿El desempeño observado representa casos futuros o es una consecuencia "
            "del azar, el sobreajuste o una partición incorrecta?"
        ),
        "duration": "2 encuentros",
        "prerequisites": "Módulos 04 y 05",
        "objectives": [
            "Separar entrenamiento, validación y test por su función.",
            "Elegir K-Fold, estratificación, grupos o cortes temporales.",
            "Comparar modelos contra baselines relevantes.",
            "Reportar distribución de métricas y no solo un promedio.",
        ],
        "theory": [
            {
                "title": "Generalización",
                "text": (
                    "El objetivo no es explicar perfectamente los datos conocidos, "
                    "sino estimar el comportamiento en unidades futuras de la misma "
                    "población operacional."
                ),
            },
            {
                "title": "Tres roles",
                "text": (
                    "Entrenamiento ajusta parámetros, validación guía decisiones de "
                    "modelado y test estima una única vez el resultado final. Reusar "
                    "test lo convierte de hecho en validación."
                ),
            },
            {
                "title": "Esquema según dependencia",
                "text": (
                    "La partición aleatoria supone observaciones intercambiables. "
                    "Series temporales, pacientes repetidos o sucursales exigen "
                    "orden o agrupación para evitar unidades relacionadas en ambos lados."
                ),
            },
            {
                "title": "Incertidumbre de evaluación",
                "text": (
                    "Promedio, dispersión e intervalos entre folds muestran estabilidad. "
                    "La validación anidada separa ajuste de hiperparámetros y estimación "
                    "cuando la comparación es exigente."
                ),
            },
        ],
        "case": (
            "Un scoring entrenado con operaciones de los mismos clientes en train y "
            "test parece excelente, pero falla con clientes nuevos."
        ),
        "deliverable": (
            "Protocolo de validación justificado, baseline, tabla de métricas por fold "
            "y evaluación final reservada."
        ),
        "lab_steps": [
            "Identificar dependencias temporales o por entidad.",
            "Construir un baseline antes de optimizar.",
            "Aplicar el esquema de validación dentro del pipeline.",
            "Reportar media, dispersión y comparación con test.",
        ],
        "simulation_title": "Diseñador de validación cruzada",
        "simulation_instruction": (
            "Elegí cantidad de folds, orden y agrupación; observá cobertura, tamaño "
            "de entrenamiento y riesgo de contaminación."
        ),
        "glossary": [
            ("Generalización", "Desempeño sobre datos no usados para construir el modelo."),
            ("Entrenamiento", "Partición empleada para ajustar parámetros."),
            ("Validación", "Partición o rotación usada para comparar decisiones de modelado."),
            ("Test", "Conjunto reservado para la estimación final."),
            ("Baseline", "Referencia simple que un modelo debe superar."),
            ("K-Fold", "Rotación en K bloques que alterna validación y entrenamiento."),
            ("Estratificación", "Preservación aproximada de proporciones de clase entre folds."),
            ("Group K-Fold", "Separación que mantiene grupos completos en un solo lado."),
            ("Walk-forward", "Validación temporal que entrena en el pasado y evalúa más adelante."),
            ("Sobreajuste", "Adaptación excesiva a datos conocidos con pobre desempeño futuro."),
        ],
        "quiz": [
            q(
                "¿Para qué se reserva el conjunto de test?",
                ["Ajustar hiperparámetros muchas veces", "Estimación final independiente", "Imputar entrenamiento", "Crear la variable objetivo"],
                1,
                "Su valor depende de no usarlo durante la selección.",
            ),
            q(
                "Si hay varias filas por cliente, ¿qué esquema evita compartir clientes?",
                ["K-Fold cualquiera", "Group K-Fold", "Shuffle sin grupos", "Leave-one-column-out"],
                1,
                "Los grupos se mantienen completos en una partición.",
            ),
            q(
                "¿Por qué incluir un baseline?",
                ["Para aumentar complejidad", "Para saber si el modelo aporta valor incremental", "Para evitar métricas", "Para reemplazar test"],
                1,
                "Una solución sofisticada debe superar una referencia operativa simple.",
            ),
            q(
                "¿Qué indica gran variación entre folds?",
                ["Estabilidad alta", "Sensibilidad a la muestra", "Causalidad", "Ausencia de clases"],
                1,
                "El resultado depende de qué observaciones integran cada partición.",
            ),
            q(
                "En series temporales conviene:",
                ["Entrenar con futuro y validar en pasado", "Preservar el orden temporal", "Mezclar siempre", "Eliminar la fecha"],
                1,
                "El protocolo debe imitar la disponibilidad real de información.",
            ),
            q(
                "Revisar test después de cada cambio produce:",
                ["Una evaluación más independiente", "Sobreajuste al test", "Menos leakage siempre", "Una nueva población"],
                1,
                "Las decisiones terminan adaptándose indirectamente a ese conjunto.",
            ),
        ],
    },
    {
        "id": "07",
        "slug": "07-series-tiempo",
        "unit": "II",
        "title": "Series de tiempo y backtesting",
        "short_title": "Series de tiempo",
        "summary": (
            "Modelar tendencia, estacionalidad y dependencia temporal con baselines "
            "honestos y evaluación de origen rodante."
        ),
        "business_question": (
            "¿Qué parte del futuro es predecible usando solo la información "
            "disponible en cada momento de decisión?"
        ),
        "duration": "2 encuentros",
        "prerequisites": "Módulos 05 y 06",
        "objectives": [
            "Reconocer tendencia, estacionalidad, ciclos y ruido.",
            "Crear lags y ventanas móviles sin usar el futuro.",
            "Construir baselines ingenuos y estacionales.",
            "Evaluar múltiples horizontes con backtesting.",
        ],
        "theory": [
            {
                "title": "La fecha es estructura",
                "text": (
                    "En una serie, el orden contiene información. Tendencia, "
                    "estacionalidad, autocorrelación y cambios de régimen invalidan "
                    "el supuesto de observaciones intercambiables."
                ),
            },
            {
                "title": "Features temporales",
                "text": (
                    "Lags, medias móviles, calendario y eventos deben calcularse "
                    "usando datos anteriores al origen de pronóstico. Un simple "
                    "centrado puede introducir futuro."
                ),
            },
            {
                "title": "Baselines fuertes",
                "text": (
                    "Último valor, promedio reciente y último ciclo estacional suelen "
                    "ser difíciles de superar. Sin ellos no sabemos si la complejidad "
                    "agrega capacidad predictiva."
                ),
            },
            {
                "title": "Backtesting",
                "text": (
                    "Evaluar varios orígenes y horizontes reproduce decisiones "
                    "históricas. Las métricas deben segmentarse por horizonte y período."
                ),
            },
        ],
        "case": (
            "Un comercio pronostica demanda semanal para decidir inventario. Los "
            "errores por defecto generan quiebres; por exceso, capital inmovilizado."
        ),
        "deliverable": (
            "Pronóstico con baseline estacional, backtesting por horizonte, intervalos "
            "y traducción del error a inventario."
        ),
        "lab_steps": [
            "Ordenar frecuencia, huecos y duplicados temporales.",
            "Descomponer nivel, tendencia y estacionalidad.",
            "Crear features rezagadas dentro de cada corte.",
            "Comparar modelos y baselines en backtesting.",
        ],
        "simulation_title": "Generador de series y backtesting",
        "simulation_instruction": (
            "Ajustá tendencia, estacionalidad, ruido y horizonte; compará un "
            "pronóstico ingenuo con uno estacional en varios cortes."
        ),
        "glossary": [
            ("Tendencia", "Cambio sostenido del nivel de una serie."),
            ("Estacionalidad", "Patrón que se repite con período relativamente estable."),
            ("Ciclo", "Oscilación de duración no necesariamente fija."),
            ("Lag", "Valor pasado usado como predictor."),
            ("Ventana móvil", "Resumen calculado sobre un tramo temporal previo."),
            ("Autocorrelación", "Asociación de una serie con sus propios rezagos."),
            ("Estacionariedad", "Estabilidad de propiedades estadísticas bajo ciertos supuestos."),
            ("Horizonte", "Distancia entre origen y momento pronosticado."),
            ("Backtesting", "Evaluación repetida desde orígenes históricos."),
            ("Baseline estacional", "Pronóstico que repite el valor del ciclo anterior."),
        ],
        "quiz": [
            q(
                "¿Por qué no conviene mezclar aleatoriamente una serie?",
                ["Porque reduce filas", "Porque puede entrenar con información futura", "Porque elimina tendencia", "Porque impide calcular medias"],
                1,
                "La partición debe respetar lo que estaba disponible en cada origen.",
            ),
            q(
                "Una media móvil centrada para pronosticar puede:",
                ["Usar datos futuros", "Eliminar toda estacionalidad", "Garantizar precisión", "Crear categorías"],
                0,
                "El centrado incluye observaciones posteriores al punto.",
            ),
            q(
                "¿Qué baseline usa el valor del mismo período del ciclo anterior?",
                ["Media global", "Ingenuo estacional", "Regresión logística", "K-Means"],
                1,
                "Por ejemplo, la demanda del mismo mes del año previo.",
            ),
            q(
                "¿Qué evalúa el backtesting?",
                ["Un único corte al azar", "Múltiples decisiones históricas simuladas", "Solo entrenamiento", "La estética del gráfico"],
                1,
                "Mueve el origen y mide el desempeño posterior.",
            ),
            q(
                "El error debería reportarse por horizonte porque:",
                ["La dificultad suele crecer o cambiar con la distancia", "Siempre es idéntico", "No existen fechas", "Reduce el dataset"],
                0,
                "Pronosticar una semana y doce semanas son tareas diferentes.",
            ),
            q(
                "¿Cuál es una feature temporal válida para el día t?",
                ["Venta de t+1", "Promedio de t-7 a t-1", "Objetivo futuro", "Promedio centrado t-3 a t+3"],
                1,
                "Solo usa observaciones anteriores al momento de decisión.",
            ),
        ],
    },
    {
        "id": "08",
        "slug": "08-regresion-logistica",
        "unit": "II",
        "title": "Regresión logística y decisiones de clasificación",
        "short_title": "Regresión logística",
        "summary": (
            "Estimar probabilidades, evaluar ranking y calibración, y elegir "
            "umbrales según costos, capacidad y valor."
        ),
        "business_question": (
            "¿A quién conviene asignar una acción cuando los errores tienen costos "
            "distintos y la capacidad es limitada?"
        ),
        "duration": "2 encuentros",
        "prerequisites": "Módulos 04 a 06",
        "objectives": [
            "Interpretar probabilidad, logit y odds.",
            "Leer matrices de confusión y métricas por clase.",
            "Distinguir discriminación, calibración y decisión.",
            "Elegir umbrales con costos y restricciones de capacidad.",
        ],
        "theory": [
            {
                "title": "De puntaje a probabilidad",
                "text": (
                    "La función logística transforma cualquier combinación lineal en "
                    "un valor entre cero y uno. Los coeficientes son aditivos en "
                    "log-odds y multiplicativos en odds."
                ),
            },
            {
                "title": "Métricas de clasificación",
                "text": (
                    "Precision responde cuántos positivos señalados eran correctos; "
                    "recall, cuántos positivos reales fueron encontrados. La clase "
                    "y el costo determinan cuál importa."
                ),
            },
            {
                "title": "Ranking y calibración",
                "text": (
                    "ROC-AUC evalúa ordenamiento global; PR-AUC es informativa con "
                    "eventos escasos. Una probabilidad calibrada significa que grupos "
                    "con puntaje similar exhiben frecuencias similares."
                ),
            },
            {
                "title": "Umbral como política",
                "text": (
                    "El valor por defecto rara vez representa la decisión. Costos de "
                    "falsos positivos y negativos, capacidad y beneficio esperado "
                    "definen la política de acción."
                ),
            },
        ],
        "case": (
            "Una campaña de retención solo puede contactar al 15 por ciento de la "
            "cartera; el equipo debe ordenar riesgo y estimar valor neto por contacto."
        ),
        "deliverable": (
            "Modelo probabilístico con curva de calibración, matriz de confusión, "
            "selección de umbral y matriz de costos."
        ),
        "lab_steps": [
            "Definir clase positiva y consecuencias de error.",
            "Construir un baseline de prevalencia.",
            "Evaluar ranking, calibración y métricas a varios umbrales.",
            "Elegir una política compatible con capacidad y valor.",
        ],
        "simulation_title": "Umbrales, errores y valor",
        "simulation_instruction": (
            "Mové el umbral y la prevalencia; observá matriz de confusión, precision, "
            "recall y utilidad esperada."
        ),
        "glossary": [
            ("Logit", "Logaritmo de las odds de un evento."),
            ("Odds", "Razón entre probabilidad de ocurrencia y de no ocurrencia."),
            ("Umbral", "Punto de corte que convierte un puntaje en una acción o clase."),
            ("Verdadero positivo", "Caso positivo correctamente señalado."),
            ("Falso positivo", "Caso negativo señalado como positivo."),
            ("Precision", "Proporción de señalados positivos que realmente lo son."),
            ("Recall", "Proporción de positivos reales detectados."),
            ("ROC-AUC", "Probabilidad de ordenar un positivo por encima de un negativo."),
            ("PR-AUC", "Resumen de precision y recall a través de umbrales."),
            ("Calibración", "Correspondencia entre probabilidades predichas y frecuencias observadas."),
        ],
        "quiz": [
            q(
                "Cambiar el umbral modifica:",
                ["Los coeficientes ya ajustados", "La matriz de confusión", "La variable objetivo histórica", "El número de columnas"],
                1,
                "El mismo puntaje produce decisiones distintas según el corte.",
            ),
            q(
                "Si es muy costoso omitir un positivo, conviene priorizar:",
                ["Recall", "Solo especificidad", "R cuadrado", "Silhouette"],
                0,
                "Recall mide la cobertura de positivos reales.",
            ),
            q(
                "Una probabilidad bien calibrada de 0,7 implica:",
                ["Certeza individual", "Aproximadamente 70 por ciento de eventos en grupos comparables", "70 variables", "Un umbral obligatorio"],
                1,
                "La calibración es una propiedad frecuentista de grupos de predicciones.",
            ),
            q(
                "Con una clase positiva muy escasa suele ser útil mirar:",
                ["PR-AUC", "Solo accuracy", "Rango", "MSE del predictor"],
                0,
                "Precision-recall enfoca el rendimiento sobre la clase positiva.",
            ),
            q(
                "¿Por qué 0,5 no es un umbral universal?",
                ["Porque costos y capacidad cambian", "Porque no está entre cero y uno", "Porque elimina probabilidades", "Porque solo sirve para regresión lineal"],
                0,
                "La decisión óptima depende de consecuencias y restricciones.",
            ),
            q(
                "¿Qué distingue discriminación de calibración?",
                ["Ordenar casos frente a acertar frecuencias", "No hay diferencia", "Una usa texto y otra números", "La cantidad de filas"],
                0,
                "Un modelo puede ordenar bien y producir probabilidades sesgadas.",
            ),
        ],
    },
    {
        "id": "09",
        "slug": "09-arboles-ensembles",
        "unit": "II",
        "title": "Árboles, Random Forest y ensembles",
        "short_title": "Árboles y ensembles",
        "summary": (
            "Aprender reglas no lineales, controlar complejidad y combinar modelos "
            "para mejorar estabilidad y desempeño."
        ),
        "business_question": (
            "¿Qué reglas e interacciones segmentan el problema y cuánto mejora la "
            "decisión al combinar múltiples modelos?"
        ),
        "duration": "4 encuentros",
        "prerequisites": "Módulos 04, 06 y 08",
        "objectives": [
            "Interpretar particiones, impureza, hojas y profundidad.",
            "Controlar sobreajuste mediante poda y restricciones.",
            "Explicar bagging, Random Forest y boosting.",
            "Evaluar importancia con métodos que respeten validación.",
        ],
        "theory": [
            {
                "title": "Particiones recursivas",
                "text": (
                    "Un árbol divide el espacio mediante preguntas simples para "
                    "homogeneizar la respuesta en hojas. Captura umbrales e "
                    "interacciones sin especificarlos de antemano."
                ),
            },
            {
                "title": "Complejidad y poda",
                "text": (
                    "Profundidad, tamaño mínimo de hoja y poda costo-complejidad "
                    "regulan la varianza. Un árbol profundo puede memorizar detalles."
                ),
            },
            {
                "title": "Bagging y bosque",
                "text": (
                    "Random Forest promedia árboles entrenados con muestras y "
                    "subconjuntos de variables diferentes. La decorrelación reduce "
                    "varianza y estabiliza predicciones."
                ),
            },
            {
                "title": "Boosting y explicación",
                "text": (
                    "Gradient boosting construye árboles secuenciales que corrigen "
                    "errores previos. Importancias internas pueden sesgarse; permutation "
                    "importance y SHAP requieren un diseño de validación coherente."
                ),
            },
        ],
        "case": (
            "Una aseguradora necesita priorizar siniestros para revisión. Requiere "
            "desempeño, reglas comunicables y control de falsos positivos."
        ),
        "deliverable": (
            "Comparación entre árbol podado, Random Forest y boosting, con curvas de "
            "aprendizaje, métricas y explicación validada."
        ),
        "lab_steps": [
            "Visualizar un árbol pequeño y traducir hojas a reglas.",
            "Explorar profundidad y tamaño mínimo de hoja.",
            "Comparar árbol, bosque y boosting bajo los mismos folds.",
            "Calcular permutation importance fuera de muestra.",
        ],
        "simulation_title": "Bosque de decisiones",
        "simulation_instruction": (
            "Ajustá profundidad, cantidad de árboles y ruido; compará fronteras, "
            "estabilidad y diferencia entre un árbol y el voto del bosque."
        ),
        "glossary": [
            ("Nodo", "Subconjunto de observaciones dentro de un árbol."),
            ("Split", "Regla que divide un nodo en ramas."),
            ("Hoja", "Nodo terminal que produce una predicción."),
            ("Impureza Gini", "Medida de mezcla de clases usada para evaluar divisiones."),
            ("Profundidad", "Cantidad máxima de divisiones desde raíz a hoja."),
            ("Poda", "Reducción controlada de ramas para limitar complejidad."),
            ("Bagging", "Promedio de modelos ajustados sobre muestras re-muestreadas."),
            ("Random Forest", "Ensemble de árboles con muestreo de filas y variables."),
            ("Boosting", "Construcción secuencial de modelos que corrigen errores."),
            ("Permutation importance", "Pérdida de desempeño al permutar una variable fuera de muestra."),
        ],
        "quiz": [
            q(
                "Un árbol muy profundo tiende a:",
                ["Reducir siempre la varianza", "Sobreajustar", "Volverse lineal", "Eliminar interacciones"],
                1,
                "Muchas hojas pueden memorizar pequeñas regiones del entrenamiento.",
            ),
            q(
                "Random Forest reduce varianza principalmente al:",
                ["Promediar árboles diversos", "Usar un único árbol", "Eliminar test", "Ordenar la variable objetivo"],
                0,
                "El promedio de errores parcialmente independientes es más estable.",
            ),
            q(
                "¿Qué diferencia central tiene boosting?",
                ["Los modelos se construyen secuencialmente", "No usa árboles nunca", "No necesita validación", "Solo predice medias"],
                0,
                "Cada etapa busca corregir errores acumulados.",
            ),
            q(
                "¿Qué parámetro limita directamente la complejidad?",
                ["Profundidad máxima", "Nombre de la columna", "Color de nodos", "Orden de importación"],
                0,
                "Restringe la cantidad de decisiones encadenadas.",
            ),
            q(
                "La importancia interna de un árbol demuestra causalidad.",
                ["Sí", "No", "Solo si es grande", "Solo en bosques"],
                1,
                "Describe uso predictivo dentro del modelo, no efectos causales.",
            ),
            q(
                "Permutation importance debería medirse preferentemente:",
                ["Fuera de muestra", "En los datos usados para memorizar", "Sin variable objetivo", "Antes de ajustar"],
                0,
                "Así refleja la pérdida de capacidad de generalización.",
            ),
        ],
    },
    {
        "id": "10",
        "slug": "10-clustering",
        "unit": "III",
        "title": "PCA, K-Means y clustering jerárquico",
        "short_title": "Clustering",
        "summary": (
            "Descubrir estructuras no supervisadas con escala, distancia, estabilidad "
            "e interpretación orientada a acciones."
        ),
        "business_question": (
            "¿Existen grupos útiles, estables y accionables o el algoritmo está "
            "forzando segmentos donde no los hay?"
        ),
        "duration": "2 encuentros",
        "prerequisites": "Módulos 01 y 04",
        "objectives": [
            "Preparar variables y distancias para segmentación.",
            "Explicar asignación y convergencia de K-Means.",
            "Leer dendrogramas, linkage y cortes jerárquicos.",
            "Usar PCA, silhouette, estabilidad y DBSCAN como diagnóstico.",
        ],
        "theory": [
            {
                "title": "Distancia con significado",
                "text": (
                    "Clustering aprende de la representación. Escala, variables "
                    "redundantes y codificación alteran distancias; por eso la "
                    "preparación es parte del modelo."
                ),
            },
            {
                "title": "K-Means",
                "text": (
                    "Alterna asignación al centroide más cercano y actualización de "
                    "centroides. Favorece grupos compactos, aproximadamente esféricos "
                    "y de escala comparable."
                ),
            },
            {
                "title": "Jerarquía y densidad",
                "text": (
                    "El clustering jerárquico construye un dendrograma según distancia "
                    "y linkage. DBSCAN identifica regiones densas y ruido sin fijar "
                    "de antemano la cantidad de grupos."
                ),
            },
            {
                "title": "Validar sin etiquetas",
                "text": (
                    "Silhouette, inercia, estabilidad por remuestreo, perfiles y "
                    "utilidad operacional aportan evidencia complementaria. PCA ayuda "
                    "a visualizar y reducir redundancia, no certifica segmentos."
                ),
            },
        ],
        "case": (
            "Marketing busca segmentos de clientes para diseñar propuestas distintas. "
            "Un grupo estadístico solo es útil si puede describirse, alcanzarse y tratarse."
        ),
        "deliverable": (
            "Segmentación comparada con K-Means y jerárquico, diagnóstico de escala, "
            "estabilidad, perfiles y acciones propuestas."
        ),
        "lab_steps": [
            "Seleccionar variables alineadas con el uso del segmento.",
            "Escalar y revisar correlaciones o aplicar PCA.",
            "Comparar K, linkage y sensibilidad a inicialización.",
            "Nombrar perfiles con evidencia y proponer acciones.",
        ],
        "simulation_title": "Centroides, jerarquía y convergencia",
        "simulation_instruction": (
            "Modificá K, escala e iteraciones; observá asignaciones, centroides, "
            "inercia y cuándo el algoritmo fuerza particiones."
        ),
        "glossary": [
            ("Clustering", "Agrupamiento no supervisado basado en similitud."),
            ("Distancia euclídea", "Longitud recta entre puntos en un espacio de variables."),
            ("Centroide", "Media vectorial de los puntos asignados a un cluster."),
            ("Inercia", "Suma de distancias cuadradas de puntos a sus centroides."),
            ("Silhouette", "Comparación de cohesión interna y separación externa."),
            ("Dendrograma", "Árbol que representa fusiones jerárquicas y sus distancias."),
            ("Linkage", "Regla para calcular distancia entre grupos."),
            ("PCA", "Proyección lineal que concentra varianza en componentes ortogonales."),
            ("DBSCAN", "Clustering por densidad capaz de marcar ruido."),
            ("Estabilidad", "Persistencia de la estructura ante cambios razonables de muestra o parámetros."),
        ],
        "quiz": [
            q(
                "¿Por qué escalar antes de K-Means?",
                ["Para que una variable grande no domine distancias", "Para crear etiquetas", "Para eliminar centroides", "Para garantizar causalidad"],
                0,
                "La distancia euclídea depende directamente de la magnitud.",
            ),
            q(
                "K-Means requiere definir:",
                ["Cantidad K", "Clase positiva", "Horizonte temporal siempre", "Coeficiente causal"],
                0,
                "El algoritmo optimiza una partición para un número elegido de centroides.",
            ),
            q(
                "¿Qué representa la altura de una fusión en un dendrograma?",
                ["La distancia según el linkage", "La cantidad de columnas", "El promedio objetivo", "La fecha de creación"],
                0,
                "El eje vertical registra la disimilitud al unir grupos.",
            ),
            q(
                "PCA garantiza clusters correctos.",
                ["Sí", "No", "Solo con dos componentes", "Solo sin escalar"],
                1,
                "PCA preserva varianza bajo una proyección, no validez de segmentos.",
            ),
            q(
                "¿Qué ventaja aporta DBSCAN?",
                ["Detecta formas por densidad y ruido", "Siempre produce grupos iguales", "No usa parámetros", "Supervisa con etiquetas"],
                0,
                "Puede capturar geometrías no esféricas y marcar puntos aislados.",
            ),
            q(
                "Un segmento accionable debe:",
                ["Ser solo visualmente atractivo", "Poder describirse, alcanzarse y tratarse", "Tener siempre igual tamaño", "Maximizar únicamente inercia"],
                1,
                "La utilidad de negocio completa la validación estadística.",
            ),
        ],
    },
    {
        "id": "11",
        "slug": "11-redes-neuronales",
        "unit": "III",
        "title": "Redes neuronales y arquitecturas modernas",
        "short_title": "Redes neuronales",
        "summary": (
            "Comprender neuronas, activaciones, backpropagation y regularización, "
            "con un mapa responsable de arquitecturas actuales."
        ),
        "business_question": (
            "¿Cuándo la capacidad de aprender representaciones justifica mayor "
            "complejidad, datos y costo computacional?"
        ),
        "duration": "3 encuentros más TensorFlow Playground",
        "prerequisites": "Módulos 04 a 06",
        "objectives": [
            "Explicar neurona, capa, activación, pérdida y gradiente.",
            "Relacionar capacidad, sobreajuste y regularización.",
            "Experimentar con fronteras no lineales en TensorFlow Playground.",
            "Distinguir CNN, RNN/LSTM/GRU, Transformers y autoencoders.",
        ],
        "theory": [
            {
                "title": "Composición de funciones",
                "text": (
                    "Cada neurona combina entradas, pesos y sesgo, y aplica una "
                    "activación. Capas sucesivas forman representaciones que pueden "
                    "aproximar relaciones no lineales complejas."
                ),
            },
            {
                "title": "Aprendizaje por gradiente",
                "text": (
                    "Backpropagation calcula cómo cambia la pérdida respecto de cada "
                    "parámetro. El optimizador actualiza pesos con una tasa de aprendizaje."
                ),
            },
            {
                "title": "Generalización",
                "text": (
                    "Arquitectura, regularización L1/L2, dropout, early stopping, "
                    "normalización y datos determinan el equilibrio entre sesgo y varianza."
                ),
            },
            {
                "title": "Mapa de arquitecturas",
                "text": (
                    "CNN explotan estructura espacial; RNN, LSTM y GRU procesan "
                    "secuencias; Transformers usan atención; autoencoders comprimen "
                    "representaciones. Los modelos generativos requieren evaluación "
                    "específica de veracidad, seguridad y costo."
                ),
            },
        ],
        "case": (
            "Un centro de atención quiere clasificar mensajes y resumir motivos. "
            "Debe comparar una referencia simple con modelos complejos y evaluar errores."
        ),
        "deliverable": (
            "Experimento controlado de arquitectura y regularización, comparación con "
            "baseline, curva de aprendizaje y ficha de riesgos."
        ),
        "lab_steps": [
            "Construir una neurona y observar su frontera.",
            "Comparar activaciones y cantidad de capas.",
            "Registrar pérdida de entrenamiento y validación.",
            "Documentar por qué una arquitectura es adecuada al tipo de dato.",
        ],
        "simulation_title": "Laboratorio de neuronas y activaciones",
        "simulation_instruction": (
            "Ajustá pesos, sesgo y activación; observá salidas y frontera de decisión "
            "antes de explorar redes multicapa."
        ),
        "glossary": [
            ("Neurona artificial", "Combinación ponderada de entradas seguida de una activación."),
            ("Peso", "Parámetro que regula la contribución de una entrada."),
            ("Sesgo", "Parámetro aditivo que desplaza la activación."),
            ("Función de activación", "Transformación, generalmente no lineal, aplicada a una neurona."),
            ("Pérdida", "Función escalar que cuantifica el error a optimizar."),
            ("Backpropagation", "Cálculo eficiente de gradientes mediante regla de la cadena."),
            ("Tasa de aprendizaje", "Tamaño de cada actualización de parámetros."),
            ("Epoch", "Recorrido completo por el conjunto de entrenamiento."),
            ("Dropout", "Regularización que desactiva unidades aleatoriamente durante entrenamiento."),
            ("Atención", "Mecanismo que pondera relaciones entre elementos de una secuencia."),
        ],
        "quiz": [
            q(
                "Sin activaciones no lineales, muchas capas densas equivalen a:",
                ["Una transformación lineal", "Un bosque aleatorio", "K-Means", "Un dendrograma"],
                0,
                "La composición de transformaciones lineales sigue siendo lineal.",
            ),
            q(
                "Backpropagation calcula:",
                ["Gradientes de la pérdida", "Clusters", "Fechas futuras", "Reglas de calidad"],
                0,
                "Usa la regla de la cadena a través de las capas.",
            ),
            q(
                "¿Qué señal clásica sugiere sobreajuste?",
                ["Bajan pérdida de train y sube la de validación", "Ambas pérdidas bajan juntas", "No hay parámetros", "La muestra crece"],
                0,
                "El modelo continúa adaptándose al entrenamiento mientras generaliza peor.",
            ),
            q(
                "¿Qué arquitectura se asocia con estructura espacial en imágenes?",
                ["CNN", "K-Means", "Regresión lineal", "Programación lineal"],
                0,
                "Las convoluciones explotan vecindad y patrones compartidos.",
            ),
            q(
                "¿Qué mecanismo caracteriza a Transformers?",
                ["Atención", "Poda de árboles", "IQR", "One-hot obligatorio"],
                0,
                "La atención modela dependencias entre posiciones.",
            ),
            q(
                "Mayor complejidad neuronal siempre mejora la decisión.",
                ["Sí", "No; debe superar baselines y justificar costo", "Solo con dropout", "Solo con texto"],
                1,
                "Datos, generalización, latencia, explicabilidad y mantenimiento también importan.",
            ),
        ],
    },
    {
        "id": "12",
        "slug": "12-optimizacion",
        "unit": "IV",
        "title": "Programación lineal y analítica prescriptiva",
        "short_title": "Optimización",
        "summary": (
            "Convertir pronósticos y costos en decisiones óptimas bajo restricciones "
            "de capacidad, presupuesto y operación."
        ),
        "business_question": (
            "¿Qué combinación de acciones maximiza valor respetando recursos, reglas "
            "y compromisos del sistema?"
        ),
        "duration": "2 encuentros",
        "prerequisites": "Módulos 00 y 05; recomendado 07 u 08",
        "objectives": [
            "Definir variables de decisión, objetivo y restricciones.",
            "Interpretar región factible, solución óptima y holguras.",
            "Distinguir modelos lineales continuos y enteros.",
            "Integrar predicción, escenarios y optimización.",
        ],
        "theory": [
            {
                "title": "Modelo de decisión",
                "text": (
                    "La variable de decisión representa lo controlable; la función "
                    "objetivo cuantifica preferencia; las restricciones codifican "
                    "límites físicos, contractuales o de política."
                ),
            },
            {
                "title": "Factibilidad y óptimo",
                "text": (
                    "Las restricciones definen una región factible. En un problema "
                    "lineal continuo, si existe un óptimo finito, aparece en un punto "
                    "extremo o en una cara equivalente."
                ),
            },
            {
                "title": "Enteros y decisiones discretas",
                "text": (
                    "Abrir una planta, asignar una persona o seleccionar una campaña "
                    "exige variables binarias o enteras. La solución deja de ser una "
                    "simple geometría continua."
                ),
            },
            {
                "title": "Predicción más prescripción",
                "text": (
                    "Los parámetros de demanda o riesgo pueden provenir de modelos. "
                    "Escenarios, sensibilidad y optimización robusta ayudan a no tratar "
                    "estimaciones inciertas como verdades."
                ),
            },
        ],
        "case": (
            "Una fábrica elige cantidades de dos productos con horas de máquina y "
            "materia prima limitadas, demanda máxima y márgenes diferentes."
        ),
        "deliverable": (
            "Modelo matemático, solución reproducible, análisis de holguras y dos "
            "escenarios de sensibilidad."
        ),
        "lab_steps": [
            "Identificar decisiones, unidades y parámetros.",
            "Escribir objetivo y restricciones antes de programar.",
            "Resolver y validar factibilidad de la solución.",
            "Variar márgenes o capacidades y explicar el cambio.",
        ],
        "simulation_title": "Frontera factible y mezcla óptima",
        "simulation_instruction": (
            "Modificá margen y capacidades; explorá la región factible, el punto "
            "óptimo y el valor de recursos adicionales."
        ),
        "glossary": [
            ("Variable de decisión", "Cantidad controlable que el modelo debe determinar."),
            ("Función objetivo", "Expresión que se maximiza o minimiza."),
            ("Restricción", "Condición que limita combinaciones permitidas."),
            ("Región factible", "Conjunto de soluciones que satisface todas las restricciones."),
            ("Óptimo", "Mejor solución factible según el objetivo."),
            ("Holgura", "Recurso no utilizado en una restricción."),
            ("Restricción vinculante", "Condición activa sin holgura en la solución."),
            ("Variable binaria", "Decisión restringida a cero o uno."),
            ("Programación entera", "Optimización con algunas o todas las variables discretas."),
            ("Análisis de sensibilidad", "Estudio del efecto de cambiar parámetros del modelo."),
        ],
        "quiz": [
            q(
                "¿Qué representa una variable de decisión?",
                ["Algo controlable", "Un error histórico", "Solo una visualización", "Una clase observada siempre"],
                0,
                "Es la acción o cantidad que la optimización debe elegir.",
            ),
            q(
                "Una solución fuera de una restricción es:",
                ["Óptima", "No factible", "Un baseline", "Un cluster"],
                1,
                "Viola al menos una condición del sistema.",
            ),
            q(
                "¿Cuándo usar una variable binaria?",
                ["Para decidir abrir o no una instalación", "Para cualquier promedio", "Para medir temperatura", "Para calcular correlación"],
                0,
                "Representa decisiones sí/no indivisibles.",
            ),
            q(
                "Una restricción con holgura cero en el óptimo es:",
                ["Vinculante", "Aleatoria", "Faltante", "Calibrada"],
                0,
                "El recurso o límite se usa completamente.",
            ),
            q(
                "¿Por qué analizar escenarios si la demanda es predicha?",
                ["Porque la predicción es incierta", "Porque no existe objetivo", "Para eliminar restricciones", "Para crear leakage"],
                0,
                "La decisión debe resistir errores plausibles en los parámetros.",
            ),
            q(
                "¿Qué debe verificarse luego de resolver?",
                ["Factibilidad y sentido operacional", "Solo el tiempo de cómputo", "El color de la salida", "La cantidad de comentarios"],
                0,
                "Una solución matemática puede revelar errores de formulación o ser impracticable.",
            ),
        ],
    },
    {
        "id": "13",
        "slug": "13-ia-responsable",
        "unit": "IV",
        "title": "Interpretabilidad, equidad y ciclo de vida",
        "short_title": "IA responsable",
        "summary": (
            "Evaluar explicaciones, equidad, privacidad, causalidad, monitoreo y "
            "gobernanza durante todo el ciclo analítico."
        ),
        "business_question": (
            "¿Podemos justificar, controlar y monitorear una decisión algorítmica "
            "frente a personas afectadas y responsables del negocio?"
        ),
        "duration": "2 encuentros",
        "prerequisites": "Módulos 06, 08 y 09",
        "objectives": [
            "Distinguir explicación global, local y causal.",
            "Medir desempeño y errores por grupos relevantes.",
            "Documentar datos, modelo, usos previstos y límites.",
            "Diseñar monitoreo de calidad, drift, valor y daño.",
        ],
        "theory": [
            {
                "title": "Explicar con alcance",
                "text": (
                    "Coeficientes, permutation importance, PDP y SHAP describen "
                    "relaciones del modelo bajo supuestos distintos. Una explicación "
                    "predictiva no prueba qué ocurriría al intervenir."
                ),
            },
            {
                "title": "Equidad como decisión",
                "text": (
                    "Comparar tasas de error, selección y calibración por grupo revela "
                    "impactos. Algunas definiciones son incompatibles cuando las tasas "
                    "base difieren; elegir requiere contexto normativo y operativo."
                ),
            },
            {
                "title": "Experimentación y causalidad",
                "text": (
                    "Una prueba A/B aleatorizada estima efectos de una intervención "
                    "bajo cumplimiento y medición adecuados. Los modelos predictivos "
                    "ordenan riesgo, pero no necesariamente efecto de tratamiento."
                ),
            },
            {
                "title": "Operación y gobernanza",
                "text": (
                    "Data cards, model cards, registro de experimentos, pruebas, "
                    "monitoreo de drift y planes de respuesta convierten un modelo "
                    "en un sistema gobernable."
                ),
            },
        ],
        "case": (
            "Un modelo prioriza solicitudes para revisión. La organización debe medir "
            "errores por grupo, explicar casos, registrar cambios y definir apelación."
        ),
        "deliverable": (
            "Ficha de modelo con propósito, métricas globales y por grupo, explicación, "
            "riesgos, monitoreo y protocolo de intervención humana."
        ),
        "lab_steps": [
            "Identificar partes afectadas y daños plausibles.",
            "Comparar métricas globales y segmentadas.",
            "Generar una explicación global y una local con límites.",
            "Diseñar indicadores, alertas y responsable de respuesta.",
        ],
        "simulation_title": "Umbrales, grupos y compromisos de equidad",
        "simulation_instruction": (
            "Ajustá umbrales por grupo y observá selección, falsos negativos, "
            "precision y utilidad; documentá el compromiso elegido."
        ),
        "glossary": [
            ("Interpretabilidad", "Grado en que una persona comprende el mecanismo o comportamiento de un modelo."),
            ("Explicación local", "Descripción de factores asociados con una predicción particular."),
            ("Explicación global", "Resumen del comportamiento general del modelo."),
            ("Equidad", "Conjunto contextual de criterios sobre distribución de beneficios, errores y oportunidades."),
            ("Tasa de selección", "Proporción de personas de un grupo que recibe una decisión positiva."),
            ("Drift", "Cambio en datos, relaciones o desempeño a lo largo del tiempo."),
            ("Model card", "Documento de propósito, evaluación, usos y límites de un modelo."),
            ("Data card", "Documento sobre origen, composición, calidad y límites de datos."),
            ("A/B test", "Experimento aleatorizado que compara intervenciones."),
            ("Supervisión humana", "Mecanismo de revisión con autoridad, información y responsabilidad reales."),
        ],
        "quiz": [
            q(
                "SHAP o permutation importance demuestran causalidad.",
                ["Sí", "No", "Solo en árboles", "Solo con test"],
                1,
                "Explican dependencias del modelo, no resultados de una intervención.",
            ),
            q(
                "¿Por qué reportar métricas por grupo?",
                ["Un promedio puede ocultar daños concentrados", "Para eliminar test", "Para duplicar filas", "Para garantizar igualdad total"],
                0,
                "El desempeño agregado puede ser aceptable y muy desigual.",
            ),
            q(
                "¿Qué estima mejor un A/B test bien ejecutado?",
                ["Efecto de una intervención asignada", "Solo correlación histórica", "La cantidad de clusters", "La varianza del código"],
                0,
                "La aleatorización equilibra confusores en expectativa.",
            ),
            q(
                "¿Qué debería incluir una model card?",
                ["Propósito, métricas, usos y límites", "Solo el nombre del algoritmo", "Credenciales", "Capturas sin contexto"],
                0,
                "La ficha permite evaluar adecuación y responsabilidad.",
            ),
            q(
                "Detectar drift requiere monitorear:",
                ["Datos y desempeño en el tiempo", "Solo commits", "Únicamente entrenamiento", "El color del dashboard"],
                0,
                "Las distribuciones y relaciones pueden cambiar después del despliegue.",
            ),
            q(
                "Supervisión humana efectiva significa:",
                ["Una firma automática", "Capacidad real de comprender, intervenir y escalar", "Ocultar el puntaje", "No registrar decisiones"],
                1,
                "La persona necesita autoridad, contexto y un procedimiento.",
            ),
        ],
    },
    {
        "id": "14",
        "slug": "14-proyecto-integrador",
        "unit": "V",
        "title": "Proyecto integrador de decisión",
        "short_title": "Proyecto integrador",
        "summary": (
            "Integrar problema, datos, modelado, evaluación, decisión, comunicación "
            "y reproducibilidad en un producto analítico defendible."
        ),
        "business_question": (
            "¿Qué decisión concreta recomendamos, con qué evidencia, valor esperado, "
            "riesgos y plan de seguimiento?"
        ),
        "duration": "Trabajo transversal con entrega parcial, final y exposición",
        "prerequisites": "Módulos 00 a 13 según el problema",
        "objectives": [
            "Formular un caso con decisión, unidad, horizonte y métrica.",
            "Construir una línea reproducible desde datos hasta evaluación.",
            "Comparar baseline y alternativas con un protocolo honesto.",
            "Comunicar recomendación, incertidumbre, límites y monitoreo.",
        ],
        "theory": [
            {
                "title": "Problema antes que algoritmo",
                "text": (
                    "El proyecto comienza con quién decide, qué acción cambia, sobre "
                    "qué unidad, cuándo y con qué costo. El algoritmo se elige después."
                ),
            },
            {
                "title": "Evidencia trazable",
                "text": (
                    "Diccionario, controles de calidad, pipeline, semillas, particiones "
                    "y registro de experimentos permiten reconstruir cada resultado."
                ),
            },
            {
                "title": "Evaluación multicriterio",
                "text": (
                    "Calidad predictiva, valor, estabilidad, equidad, interpretabilidad, "
                    "latencia y mantenimiento conforman un tablero de decisión."
                ),
            },
            {
                "title": "Narrativa ejecutiva",
                "text": (
                    "La exposición conecta contexto, evidencia, alternativa, recomendación, "
                    "impacto y próximos pasos. Los límites se presentan como condiciones "
                    "para actuar responsablemente."
                ),
            },
        ],
        "case": (
            "Cada equipo selecciona un problema de regresión, clasificación, series, "
            "segmentación u optimización con una decisión real y una audiencia definida."
        ),
        "deliverable": (
            "Repositorio reproducible, informe ejecutivo, notebook final, ficha de "
            "modelo, presentación y defensa oral."
        ),
        "lab_steps": [
            "Completar canvas de decisión y contrato de datos.",
            "Entregar EDA, baseline y protocolo en el hito parcial.",
            "Cerrar pipeline, evaluación, valor y riesgos.",
            "Ensayar una exposición centrada en la recomendación.",
        ],
        "simulation_title": "Canvas de valor y alcance",
        "simulation_instruction": (
            "Ajustá beneficio, costo, adopción y desempeño; observá valor esperado, "
            "punto de equilibrio y estado de los hitos."
        ),
        "glossary": [
            ("Decisión", "Elección concreta que el producto analítico busca mejorar."),
            ("Stakeholder", "Persona o grupo que decide, usa, mantiene o recibe impacto."),
            ("Alcance", "Límite explícito de población, tiempo, datos y funcionalidades."),
            ("Baseline", "Referencia mínima contra la cual se mide la propuesta."),
            ("Criterio de aceptación", "Condición observable que debe cumplir un entregable."),
            ("Trazabilidad", "Capacidad de vincular una conclusión con datos, código y supuestos."),
            ("Riesgo", "Evento incierto que puede afectar valor, personas u operación."),
            ("Valor esperado", "Promedio ponderado de beneficios y costos bajo probabilidades."),
            ("Plan de monitoreo", "Indicadores, umbrales, frecuencia y responsables posteriores."),
            ("Defensa", "Argumentación oral que responde evidencia, decisiones y límites."),
        ],
        "quiz": [
            q(
                "¿Qué debería definirse primero?",
                ["La decisión y el problema", "El algoritmo más complejo", "El color del dashboard", "La cantidad de capas"],
                0,
                "El método debe responder a una necesidad y una acción concreta.",
            ),
            q(
                "¿Qué demuestra que un modelo agrega valor?",
                ["Superar un baseline relevante bajo la métrica de decisión", "Tener más líneas", "Usar IA", "Incluir muchos gráficos"],
                0,
                "La mejora debe ser fuera de muestra y material para la decisión.",
            ),
            q(
                "¿Cuál es un entregable reproducible?",
                ["Notebook que ejecuta desde cero con dependencias y datos claros", "Solo una captura", "Código sin instrucciones", "Resultados pegados manualmente"],
                0,
                "Otra persona debe poder regenerar la evidencia.",
            ),
            q(
                "¿Por qué declarar límites?",
                ["Para definir cuándo la recomendación es válida", "Para debilitar el proyecto", "Para ocultar resultados", "Para evitar métricas"],
                0,
                "Toda evidencia tiene un dominio de aplicación.",
            ),
            q(
                "Una exposición ejecutiva debe comenzar por:",
                ["Contexto, decisión y recomendación", "Lista de imports", "Todos los hiperparámetros", "Historia completa del lenguaje"],
                0,
                "La audiencia necesita entender primero qué está en juego.",
            ),
            q(
                "¿Qué completa el ciclo después de entregar?",
                ["Monitoreo y responsables de respuesta", "Eliminar el repositorio", "Ignorar nuevos datos", "Congelar toda decisión"],
                0,
                "El desempeño y el contexto cambian durante el uso.",
            ),
        ],
    },
]


MODULES_BY_ID = {module["id"]: module for module in MODULES}
