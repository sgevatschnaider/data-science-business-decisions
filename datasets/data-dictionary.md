
# Diccionario de datos

## clientes.csv

| Variable | Tipo | Descripción |
|---|---|---|
| cliente_id | entero | Identificador sintético único |
| segmento | categoría | Perfil comercial inicial |
| zona_operativa | categoría | Zona sintética para análisis de segmentos y cobertura |
| canal_preferido | categoría | Canal principal de interacción |
| antiguedad_meses | entero | Meses desde el alta |
| compras_90d | entero | Compras en los últimos noventa días |
| ticket_promedio | decimal anulable | Importe medio por compra; incluye faltantes didácticos |
| reclamos_180d | entero | Reclamos en los últimos ciento ochenta días |
| costo_contacto | decimal | Costo sintético de intervenir por el canal elegido |
| valor_cliente_12m | decimal | Valor sintético observado en doce meses |
| abandono_30d | binaria | Evento sintético en los treinta días siguientes |

## ventas-mensuales.csv

| Variable | Tipo | Descripción |
|---|---|---|
| fecha | fecha | Primer día del mes |
| ventas | decimal | Nivel sintético mensual |
| promocion | binaria | Mes con promoción planificada |
| feriado | binaria | Indicador de período festivo |
| inversion_marketing | decimal | Inversión sintética mensual |
| indice_precio | decimal | Índice sintético de precio |

## operaciones.csv

| Variable | Tipo | Descripción |
|---|---|---|
| orden_id | entero | Identificador sintético |
| producto | categoría | Familia A, B o C |
| turno | categoría | Franja operativa sintética |
| horas_maquina | decimal | Consumo estimado de capacidad |
| materia_prima | decimal | Consumo estimado de insumo |
| margen | decimal | Contribución sintética |
| demanda | entero | Unidades solicitadas en la orden |
| retraso_horas | decimal | Demora operativa sintética |

## experimentos.csv

| Variable | Tipo | Descripción |
|---|---|---|
| observacion_id | entero | Identificador sintético de exposición |
| variante | categoría | Asignación aleatoria A o B |
| segmento | categoría | Segmento previo al tratamiento |
| conversion | binaria | Resultado principal observado |
| margen | decimal | Contribución observada después de la exposición |
| tiempo_respuesta_ms | decimal | Latencia del flujo asignado |
