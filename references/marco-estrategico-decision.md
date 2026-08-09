
# Marco estratégico de decisión

Este marco organiza el recorrido analítico según el tipo de pregunta que una organización necesita responder. No reemplaza la validación técnica: ayuda a ubicarla dentro de una decisión real.

| Nivel | Pregunta rectora | Evidencia mínima | Riesgo frecuente |
|---|---|---|---|
| Observar | ¿Qué ocurre y cómo se genera el dato? | Calidad, distribución, segmentos y trazabilidad | Confundir el registro con el proceso real |
| Predecir | ¿Qué resultado es probable? | Baseline, validación fuera de muestra, calibración e incertidumbre | Optimizar una métrica sin política de uso |
| Intervenir | ¿Qué cambiaría si actuamos? | Supuestos causales, comparación válida y heterogeneidad | Interpretar correlación como efecto |
| Decidir | ¿Qué acción crea más valor? | Costos de error, capacidad, restricciones y análisis de sensibilidad | Usar el umbral por defecto o ignorar límites |
| Escalar | ¿Cómo se ejecuta de forma controlada? | Permisos mínimos, aprobación, trazas, monitoreo y reversión | Automatizar sin dueño ni criterio de detención |

## Tres distinciones esenciales

1. **Precisión no equivale a valor.** Una mejora predictiva importa cuando cambia una acción y su beneficio supera los costos y riesgos.
2. **Predicción no equivale a intervención.** Estimar quién presenta un resultado no demuestra qué acción lo modificará.
3. **Automatización no equivale a autonomía ilimitada.** Un agente responsable opera dentro de permisos explícitos, conserva evidencia y escala excepciones a una persona.

## Uso didáctico

Antes de elegir una técnica, documentá el nivel actual, la pregunta rectora, la evidencia disponible, la acción propuesta y el criterio que impediría avanzar. Volvé a este registro después de validar el modelo: una decisión puede ser técnicamente posible y aun así no ser económica, responsable u operable.

## Procedencia conceptual

La síntesis adapta la visión “From Prediction to Action” del [repositorio original](https://github.com/sgevatschnaider/data-science-for-business-models) a la arquitectura verificable de este curso. La redacción y la tabla fueron elaboradas específicamente para este material.

Material elaborado por el profesor Sergio Gevatschnaider.
