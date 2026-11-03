# Inventario y diagnóstico previo

Auditoría del 03/11/2026. Base Git: `06286cbf2a25b32853e4c01f51f3b5ad19e0338a`. Los originales se conservan en el ZIP de entrada y la historia Git. No se modifica ningún otro módulo.

| Archivo de entrada | Rigor y fortalezas | Ausencias / observaciones | Destino |
|---|---|---|---|
| UCA_Redes_Neuronales_fundamentos.pdf | 28 slides, fórmulas básicas correctas, separación inferencia/entrenamiento | Sin cálculo completo de backprop, derivadas por activación, dimensiones ni matriz de confusión. Pregunta genérica repetida. Cajas reiteradas y diagramas pequeños. | ppt-1-fundamentos: 51 slides, PDF, visor y laboratorios |
| UCA_Redes_Neuronales_secuencias.pdf | 13 slides, recurrencia y memoria simplificada coherentes | Faltan ecuaciones completas de gates, BPTT y ejemplo numérico. Comparación de arquitecturas demasiado breve. | ppt-2-rnn-lstm: 34 slides, PDF y visor |
| UCA_Redes_Neuronales_fundamentos.pptx | 28 slides, fórmulas básicas correctas, separación inferencia/entrenamiento | Sin cálculo completo de backprop, derivadas por activación, dimensiones ni matriz de confusión. Pregunta genérica repetida. Cajas reiteradas y diagramas pequeños. | ppt-1-fundamentos: 51 slides, PDF, visor y laboratorios |
| UCA_Redes_Neuronales_secuencias.pptx | 13 slides, recurrencia y memoria simplificada coherentes | Faltan ecuaciones completas de gates, BPTT y ejemplo numérico. Comparación de arquitecturas demasiado breve. | ppt-2-rnn-lstm: 34 slides, PDF y visor |
| 01_perceptron.html | Frontera y actualización de perceptrón funcionales | XOR usa cuadrantes, no tabla canónica. Recorta pesos. Sin autoplay/temas/velocidad. | labs/01_perceptron.html |
| 02_activaciones.html | Activaciones y derivadas correctas, kink de ReLU explicitado | Ejes sin escala numérica suficiente. Sin recorridos automáticos/temas. | labs/02_activaciones.html |
| 03_gradiente.html | BCE y gradientes logísticos promedio correctos | Pesos no editables, sin escenarios ni autoplay, eje de pasos poco explícito. | labs/03_gradiente.html |
| 04_umbral.html | Semilla fija y matriz de confusión | Utilidad TP·valor−FP·costo omite contacto de TP y efectividad causal. Población poco desbalanceada. Se reemplaza por proxy explícito TP·q·B−(TP+FP)·C. | labs/04_umbral.html |
| 05_memoria_lstm.html | c y h correctos con gates fijos | Modelo didáctico, no LSTM entrenada. Trayectoria completa visible desde inicio, sin animación temporal. | labs/05_memoria_lstm.html |
| Enlaces_de_videos.html | 6 URLs de 3Blue1Brown/StatQuest | Sin estado de verificación por video, sin objetivos ni preguntas específicas | videos.json y videos.html en ambos decks |

## Recursos existentes y decisiones

- `docs/modulos/11-redes-neuronales/index.html`: índice del programa muestra Módulo 12. Se conserva esa numeración visible y el slug 11. Se renueva la entrada principal.
- `simulacion.html`: entrada histórica genérica. Se transforma en índice compatible de laboratorios nuevos, manteniendo la URL.
- `cuestionario.html`, `glosario.html`, `nlp-lab.html`, recursos Transformer y JS asociados: se conservan sin cambios.
- `notebooks/11-redes-neuronales.ipynb`: incluye tabla ordinal arbitraria de calidad/costo. Se sustituye esa evidencia por experimentos sintéticos reproducibles, métricas medidas y baseline.
- `docs/index.html`, `docs/programa.html`: solo descripción del módulo. `course-manifest.json`: extensión de recursos, sin alterar conteos globales históricos.

## Reutilización y referencia

Se inspeccionaron index/reader/reader.js/data/catalog/lab/guide/videos y directorios slides/downloads de China, commit `8f79241ef24381210489d6db58132f9b3f498f5e`. Se adopta integración por catálogo, notas, recursos asociados y visor. Se mejora eliminación de límites de slide codificados y errores silenciosos de Fullscreen.

Repositorio previo: se revisaron perceptrón, activaciones, gradiente, forward/backprop v11, regularización ampliada y RNN_LSTM. Se aprovechan progresión didáctica y ecuaciones, con enlaces a materiales ampliados. No se copian motores completos ni dependencias CDN redundantes. Se retienen de los HTML del ZIP sigmoide estable, gradientes logísticos, actualización de perceptrón y recurrencia escalar de LSTM, con pruebas independientes.

## Integridad de entrada

- `UCA_Redes_Neuronales_fundamentos.pdf` SHA256 `a8e1d7533945f344509927f29164cbd1abb035d3a44f0ffce8f313ba4bf067e2`
- `UCA_Redes_Neuronales_secuencias.pdf` SHA256 `9cf33cfa7e715bcb81d59f2e43f9771fac83e21ee0f29093c778492f82725d3c`
- `UCA_Redes_Neuronales_fundamentos.pptx` SHA256 `0af5418a4712970fe3356330085f3fc2921f29607fa7835b894387e2d08ac7b2`
- `UCA_Redes_Neuronales_secuencias.pptx` SHA256 `1e35f3372c97e11305d4eaeb388dcbfe2456377639d293409abdcb34cfd40c33`
- `01_perceptron.html` SHA256 `e54fcde7dff1e966d24369c55e0e60352f3b6e4ae218cb3a480d8266e682da5e`
- `02_activaciones.html` SHA256 `31b04ce8409045e8bd31159110312a395eab4e3698cec83ae52d2f22a6202689`
- `03_gradiente.html` SHA256 `0280d7b98e9270e195b95377082830eb88399664d21298a9612db98fb3c687c1`
- `04_umbral.html` SHA256 `2158d406812b1481e1f4d971ba9a730847a9de46aaac00773bdf0d80653b9d34`
- `05_memoria_lstm.html` SHA256 `4c66e86f6b2c893f85e93cda14020832be144b650ce3a5c72bf019f4a373e844`
- `Enlaces_de_videos.html` SHA256 `5454968cfbd85c742d608a168dc60ba62bb793e84db1aab5b21894073b44ba93`